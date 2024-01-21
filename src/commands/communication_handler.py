from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from utils.generate.complex_answer_generator.answer_mistakes_generator import AnswerMistakesGenerator
from utils.transcriber import TextToSpeech
from utils.user import UserCreateMessage

class CommunicationHandler:
    def __init__(self, message: Message, state: FSMContext, bot: Bot):
        self.message = message
        self.state = state
        self.bot = bot

        self.chat_id = message.chat.id

    def handle_audio_message(self, message_text: str):
        await self.bot.send_chat_action(chat_id=self.message_id, action='record_audio')
        self.handle_message(self.chat_id, message_text, "audio")

        audio = await TextToSpeech(prompt=generated_text, tg_id=str(self.message.from_user.id)).get_speech()

        await self.bot.send_audio(self.chat_id, audio)

    def handle_text_message(self, message: Message):
        await self.bot.send_chat_action(chat_id=message.chat.id, action='typing')
        self.handle_message(message.chat.id, message.text, "text")

    def send_missed_you_sticker(self):
        await self.bot.send_sticker(self.message.chat.id,
                               "CAACAgIAAxkBAAELCClliDpu7gUs1D7IY2VbH0lFGempgwACnUgAAlH1eEtz9YwiWRWyAAEzBA")
        state_data = await self.state.get_data()
        state_data["sticker_sent"] = True
        await self.state.update_data(state_data)

    def handle_message(self, message_text, message_type: str):
        """
        Common part of handling for messages of both types
        """
        user_service = UserCreateMessage(
            tg_id=str(self.chat_id),
            prompt=message_text,
            type_message=message_type)

        if await user_service.was_last_message_sent_two_days_ago():
            self.send_missed_you_sticker()

        # try to generate AI's answer combined with the list of mistakes
        generated_json = await AnswerMistakesGenerator(
            tg_id=str(self.chat_id),
            prompt=message_text,
            user_message_history=await user_service.get_user_message_history()).generate_message()
        if generated_json:
            self.save_generated_text()
