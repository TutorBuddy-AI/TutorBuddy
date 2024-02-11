from typing import List, Optional

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import md
from aiogram import types
from aiogram.types import ParseMode

from database.models import MessageHistory
from utils.answer import AnswerRenderer
from utils.answer.answer import Answer
from utils.answer.render import Render
from utils.answer.render_helper import RenderHelper
from utils.generate.communication import CommunicationGenerate
from utils.generate.complex_answer_generator.answer_mistakes_generator import AnswerMistakesGenerator
from utils.message import MessageHelper
from utils.message_history_mistakes import MessageMistakesHelper, MessageMistakesService
from utils.transcriber import TextToSpeechEleven, SpeechToText
from utils.transcriber.text_to_speech_openia import TextToSpeechOpenAI
from utils.user import UserCreateMessage, UserService
from utils.stciker.sticker_sender import StickerSender
from utils.transcriber import SpeechToText
from utils.user import UserCreateMessage, UserService
from utils.newsletter.newsletter import convert_bytes_to_ogg
import datetime
import os

class CommunicationHandler:
    def __init__(self, message: Message, state: FSMContext, bot: Bot):
        self.message = message
        self.state = state
        self.bot = bot

        self.message_text = message.text
        self.chat_id = message.chat.id
        self.speaker: Optional[str] = None
        self.sticker_sender: Optional[StickerSender] = None

    async def init(self):
        user_service = UserService()
        user_info = await user_service.get_user_info(tg_id=self.chat_id)
        self.speaker = user_info["speaker"] if user_info["speaker"] else "Tutor Bot"

        self.sticker_sender = StickerSender(self.bot, self.chat_id, self.speaker)


    async def handle_audio_message(self):
        wait_message = await self.bot.send_message(self.chat_id, f"⏳ {self.speaker} thinks… Please wait")

        await self.bot.send_chat_action(chat_id=self.chat_id, action='record_audio')
        message_text = await SpeechToText(file_id=self.message.voice.file_id).get_text()
        answer = await self.prepare_answer(message_text, "audio")
        if answer.answer_text is not None:
            written_messages = await self.save_generated_text(message_text, answer.answer_text, "audio")
            await MessageHelper().group_conversation_info_to_state(self.state, written_messages)

        if answer.are_mistakes_provided:
            concat_mistakes = "\n".join(list(answer.mistakes))

            mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
                await self.state.get_data(), self.message, concat_mistakes)

            await MessageMistakesService().create_mistakes(mistakes_info)

        render = AnswerRenderer(answer, message_text, self.message.message_id, "audio").render()

        await self.render_audio_answer(render)
        await self.bot.delete_message(self.chat_id, wait_message.message_id)
        await self.save_render_in_context(render)

    async def handle_text_message(self):
        wait_message = await self.bot.send_message(self.chat_id, f"⏳ {self.speaker} thinks… Please wait")
        await self.bot.send_chat_action(chat_id=self.chat_id, action='typing')

        answer = await self.prepare_answer(self.message_text, "text")
        if answer.answer_text is not None:
            written_messages = await self.save_generated_text(self.message_text, answer.answer_text, "text")
            await MessageHelper().group_conversation_info_to_state(self.state, written_messages)
        render = AnswerRenderer(answer, self.message_text, self.message.message_id,"text").render()

        await self.render_text_answer(render)
        await self.bot.delete_message(self.chat_id, wait_message.message_id)
        await self.save_render_in_context(render)

    async def save_render_in_context(self, render):
        await RenderHelper(self.state).save_render_info(render)

    async def load_render_from_context(self) -> Render:
        return await RenderHelper(self.state).group_render_info()

    async def render_answer(self, render: Render):
        if render.message_type == "text":
            await self.render_text_answer(render)
        else:
            await self.copy_audio_message(render)

    async def copy_audio_message(self, render: Render):
        state_data = await self.state.get_data()
        additional_menu_message = await self.bot.send_message(
            self.chat_id, md.escape_md(f"Transcript: {render.message_text}"), reply_markup=render.user_message_markup,
            reply_to_message_id = render.reply_to_message_id
        )
        answer_message = await self.bot.copy_message(
            self.chat_id, from_chat_id=self.chat_id, message_id=state_data["answer_message_id"],
            reply_markup=render.bot_message_markup, reply_to_message_id = render.reply_to_message_id)
        await self.clear_old_menus()
        await self.regsiter_menu(answer_message.message_id, additional_menu_message.message_id)

    async def render_text_answer(self, render: Render):
        user_info = await UserService().get_user_info(self.chat_id)
        user_speaker = user_info['speaker']

        if user_speaker == 'Anastasia':
            audio = await TextToSpeechEleven(prompt=render.answer_text, tg_id=str(self.chat_id)).get_speech()
        elif user_speaker == "Tutor Bot":
            audio = await TextToSpeechOpenAI(prompt=render.answer_text, tg_id=str(self.chat_id)).get_speech()
        else:
            raise Exception("Unknown speaker")

        if render.is_generation_successful:
            file_ogg = f'{datetime.datetime.now()}{self.chat_id}.ogg'
            await convert_bytes_to_ogg(audio,file_ogg)
            audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')

            answer_message = await self.bot.send_voice(
                                   self.chat_id,
                                   audio_input_file,
                                   caption=f'<span class="tg-spoiler">{render.answer_text}</span>',
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=render.bot_message_markup,
                                   reply_to_message_id=render.reply_to_message_id)

            await self.clear_old_menus()
            await self.regsiter_menu(answer_message.message_id, additional_menu_message.message_id)
        else:
            file_ogg = f'{datetime.datetime.now()}{self.chat_id}.ogg'
            await convert_bytes_to_ogg(audio,file_ogg)
            audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')

            await self.bot.send_voice(self.chat_id,
                                      audio_input_file,
                                      caption=f'<span class="tg-spoiler">{render.answer_text}</span>',
                                      parse_mode=ParseMode.HTML,
                                      reply_to_message_id=render.reply_to_message_id)
            await self.sticker_sender.send_problem_sticker(render.reply_to_message_id)

        os.remove(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')

    async def render_audio_answer(self, render: Render):
        user_info = await UserService().get_user_info(self.chat_id)
        user_speaker = user_info['speaker']

        if user_speaker == 'Anastasia':
            audio = await TextToSpeechEleven(prompt=render.answer_text, tg_id=str(self.chat_id)).get_speech()
        elif user_speaker == "Tutor Bot":
            audio = await TextToSpeechOpenAI(prompt=render.answer_text, tg_id=str(self.chat_id)).get_speech()
        else:
            raise Exception("Unknown speaker")

        if render.is_generation_successful:
            additional_menu_message = await self.bot.send_message(
                self.chat_id, f"<i>🎙 Transcript</i>:\n<code>{render.message_text}</code>", parse_mode=ParseMode.HTML,
                reply_to_message_id=render.reply_to_message_id)

            file_ogg = f'{datetime.datetime.now()}{self.chat_id}.ogg'
            await convert_bytes_to_ogg(audio,file_ogg)
            audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')
            answer_message = await self.bot.send_voice(
                                   self.chat_id,
                                   audio_input_file,
                                   caption=f'<span class="tg-spoiler">{render.answer_text}</span>',
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=render.bot_message_markup,
                                   reply_to_message_id=render.reply_to_message_id
                                  )

            await self.clear_old_menus()
            await self.regsiter_menu(answer_message.message_id, additional_menu_message.message_id)
        else:
            file_ogg = f'{datetime.datetime.now()}{self.chat_id}.ogg'
            await convert_bytes_to_ogg(audio,file_ogg)
            audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')
            await self.bot.send_voice(self.chat_id, audio_input_file,
                reply_to_message_id=render.reply_to_message_id)
            await self.sticker_sender.send_problem_sticker(render.reply_to_message_id)

        os.remove(f'/home/ubuntu/AI-TutorBuddy-bot/{file_ogg}')

    async def regsiter_menu(self, answer_message_id, additional_menu_message_id):
        state_data = await self.state.get_data()
        state_data["additional_menu_message_id"] = additional_menu_message_id
        state_data["answer_message_id"] = answer_message_id
        await self.state.update_data(state_data)

    async def clear_old_menus(self):
        state_data = await self.state.get_data()
        if ("answer_message_id" in state_data) and state_data["answer_message_id"]:
            await self.bot.edit_message_reply_markup(
                chat_id=self.chat_id, message_id=state_data["answer_message_id"], reply_markup=None)
            state_data["answer_message_id"] = None
            await self.bot.edit_message_reply_markup(
                chat_id=self.chat_id, message_id=state_data["additional_menu_message_id"], reply_markup=None)
            state_data["additional_menu_message_id"] = None
        await self.state.update_data(state_data)

    async def send_missed_you_sticker(self, reply_to):
        await self.sticker_sender.send_miss_you_sticker(reply_to)
        state_data = await self.state.get_data()
        state_data["sticker_sent"] = True
        await self.state.update_data(state_data)

    async def save_generated_text(self, message_text: str, answer_text: str, message_type: str) -> List[MessageHistory]:
        user_service = UserCreateMessage(
            tg_id=str(self.chat_id),
            prompt=message_text,
            type_message=message_type)
        written_messages = await user_service.create_communication_message_text(answer_text)
        return written_messages

    async def generate_answer(self, user_service: UserCreateMessage, user_message_text: str) -> Answer:
        # try to generate AI's answer combined with the list of mistakes
        generated_json = await AnswerMistakesGenerator(
            tg_id=str(self.chat_id),
            prompt=user_message_text,
            user_message_history=await user_service.get_user_message_history()).generate_message()
        if generated_json:
            answer = Answer(answer_text=generated_json["answer"], mistakes=generated_json["mistakes"])
        else:
            # json wasn't successfully generated - regenerate answer separately
            generated_text = await CommunicationGenerate(
                tg_id=str(self.chat_id),
                prompt=user_message_text,
                user_message_history=await user_service.get_user_message_history()).generate_message()

            if generated_text is not None:
                answer = Answer(answer_text=generated_text, mistakes=None)
            else:
                answer = Answer(answer_text=None, mistakes=None)
        return answer

    async def prepare_answer(self, message_text: str, message_type: str) -> Answer:
        """
        Common part of handling for messages of both types
        """
        user_service = UserCreateMessage(
            tg_id=str(self.chat_id),
            prompt=message_text,
            type_message=message_type)

        if await user_service.was_last_message_sent_two_days_ago():
            await self.send_missed_you_sticker(self.message.message_id)
        return await self.generate_answer(user_service, message_text)
