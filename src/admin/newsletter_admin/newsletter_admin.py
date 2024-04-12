import traceback
from typing import Optional

from sqlalchemy import select
from src.config import bot, dp
from src.database import session, Transactional
from src.database.models import DailyNews, User
import os
import logging
from aiogram import types
from src.database.models.message_history import MessageHistory
from src.database.models.setting import Setting
from src.keyboards.form_keyboard.form_keyboard import get_keyboard_summary_choice
from src.texts.texts import get_first_summary
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.audio_converter.audio_converter_cache import AudioConverterCache
from src.utils.setting.setting_service import SettingService
from src.utils.transcriber.text_to_speech import TextToSpeech
from aiogram.enums import ParseMode
from src.utils.answer.answer_renderer import AnswerRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import asyncio
from src.utils.generate import GenerateAI
from src.utils.user.user_service import UserService
from markdownify import markdownify as md
import html
import re

class Newsletter:
    '''Рассылка'''

    def __init__(self):
        '''Класс не принимает аргументов'''
        ...

    async def send_newsletter(self, newsletter) -> None:
        '''Отправка поста с текстом и фото (если img указан) по topic + voice'''
        await self.send_single_article(newsletter)

    async def send_single_article(self, daily_news):
        # Вызов метода, передавая topic, ожидаем лист из tg_id в str
        tg_id_list = await self.user_topic(daily_news.topic)
        post_text = await self.formatting_post_text(daily_news)
        cleaned_post_text = await self.remove_html_tags(post_text)

        audio_files = {
            'Anastasia': await TextToSpeech.get_speech_by_voice('Anastasia', cleaned_post_text),
            'Bot': await TextToSpeech.get_speech_by_voice('Bot', cleaned_post_text)
        }

        converted_files = AudioConverterCache(audio_files).convert_files_to_ogg()

        for tg_id in tg_id_list:
            try:
                if await SettingService.is_summary_on(tg_id):
                    post_message = await self.send_summary(tg_id, daily_news, converted_files)
                    await asyncio.sleep(3)

                    await self.send_opinion(tg_id, post_text, post_message.message_id)
                    await asyncio.sleep(3)
                    # if self.is_summary_answered(tg_id):
                    #     await self.summaries_choice(tg_id)

            except Exception as e:
                traceback.print_exc()

        await self.delete_audio_files(converted_files)

    async def delete_audio_files(self, converted_files):
        for file_path in converted_files:
            if os.path.exists(file_path):
                os.unlink(file_path)

    async def remove_html_tags(self,post_text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', post_text)

    async def formatting_post_text(self,daily_news):
        post_text = f"{daily_news.title}"

        if daily_news.edition:
            post_text += f"\n{daily_news.edition}"
        if daily_news.publication_date:
            post_text += f"\n{daily_news.publication_date}"

        post_text += f"\n{daily_news.message}"
        # Заменяем <br> на \n
        formatting_post_text = html.unescape(post_text.replace('<br>', '\n'))
        return formatting_post_text

    async def send_summary(self, tg_id, daily_news, post_audio_files):
        path_img = daily_news.path_to_data
        post_text = await self.formatting_post_text(daily_news)
        cleaned_post_text = await self.remove_html_tags(post_text)

        post_message = MessageHistory(
            tg_id=tg_id,
            message=cleaned_post_text,
            role='assistant',
            type='text'
        )
        # Сохранение в MessageHistory текст поста
        session.add(post_message)
        voice = await self.get_voice(tg_id)

        post_translate_button = AnswerRenderer.get_button_caption_translation(
            bot_message_id=post_message.id, user_message_id="")
        # Отправка фото с текстом newsletter под ним
        post_message = await bot.send_photo(
            chat_id=int(tg_id),
            photo=types.InputFile(path_img),
            caption=post_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton(
                    text='Original article ➡️📃',
                    web_app=WebAppInfo(),
                    url=daily_news.url)
            ).row(post_translate_button)
        )

        if voice == "Anastasia":
            file_path = post_audio_files[0]
        else:
            file_path = post_audio_files[1]

        await bot.send_voice(int(tg_id), types.InputFile(file_path))
        return post_message

    async def send_opinion(self, tg_id, post_text, post_message_id):
        payload = await self.get_payload(tg_id, post_text)

        generated_text = await GenerateAI(
            request_url="https://api.openai.com/v1/chat/completions").request_gpt(payload=payload)

        answer = generated_text["choices"][0]["message"]["content"]

        talk_message = MessageHistory(
            tg_id=tg_id,
            message=answer,
            role='assistant',
            type='text'
        )
        # Сохранение в MessageHistory текст поста
        session.add(talk_message)
        voice = await self.get_voice(tg_id)
        audio = await TextToSpeech.get_speech_by_voice(voice, answer)
        markup = AnswerRenderer.get_markup_caption_translation(
            bot_message_id=talk_message.id, user_message_id="")
        with AudioConverter(audio) as ogg_file:
            # Отправка вопроса юзера по поводу newsletter голосовое сообщение
            await bot.send_voice(int(tg_id),
                                 types.InputFile(ogg_file),
                                 caption=f'<span class="tg-spoiler">{answer}</span>',
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=markup,
                                 reply_to_message_id=post_message_id)

    async def user_topic(self, topic) -> list:
        '''Выборка из тех кому надо отправить рассылку по topic пользователя'''
        query = select(User)
        result = await session.execute(query)
        user_for_news = result.scalars().unique().all()

        matching_tg_ids = []

        for user_topic in user_for_news:
            topics_list = str(user_topic.topic).split()
            # Если указано несколько topic у пользователя, мы ищем из них topic который указали в admin.
            # Сейчас указываем в admin только 1 topic
            if topic.lower().strip() in map(str.lower, topics_list):
                matching_tg_ids.append(user_topic.tg_id)

        return matching_tg_ids

    async def get_voice(self, tg_id) -> str:
        '''По tg_id ищем его спикера и возвращаем его '''
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if user:
            return user.speaker
        else:
            logging.error("ERROR FROM GET_VOICE")

    async def get_payload(self, tgid, string):
        user_info = await UserService().get_user_info(tgid)
        service_request = {
            "role": "system",
            "content": f"Your student {user_info['name'] if user_info['name'] is not None else 'didnt say name'}."
                       f" His English level is {user_info['english_level']}, where 1 is the worst level of"
                       f" English, and 4 is a good level of English. His goal is to study the English"
                       f" {user_info['goal']}, and his topics of interest are {user_info['topic']}."
                       f"You are {user_info['speaker']}. You are developed by AI TutorBuddy."
                       f"You are English teacher and you need assist user to increase english level. "
        }
        translate_request = {
            "role": "system",
            "content":
                f"{string}. In line 1, briefly express your complimentary opinion about this article "
                f"based on the main ideas from it, and in line 2, "
                f"ask your interlocutor about his/her opinion about this article. "
                f"Continue discussing this article with him/her, "
                f"briefly respond to his/her messages and always ask a logical question to continue the dialogue."
        }
        logging.error(translate_request)

        extended_history = [service_request]
        extended_history.append(translate_request)

        return {
            "model": "gpt-3.5-turbo",
            "messages": extended_history,
            "max_tokens": 100
        }

    @staticmethod
    async def summaries_choice(tg_id):
        user_service = UserService()
        user_info = await user_service.get_user_info(tg_id=tg_id)
        name = user_info["name"]

        await bot.send_photo(int(tg_id), photo=types.InputFile('./files/summary.jpg'),
                             caption=get_first_summary(name),
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=await get_keyboard_summary_choice(menu=False))

        talk_message = MessageHistory(
            tg_id=tg_id,
            message=get_first_summary("name"),
            role='assistant',
            type='text'
        )

        session.add(talk_message)
        await session.commit()
        await session.close()

        markup = AnswerRenderer.get_markup_caption_translation(
            bot_message_id=talk_message.id, user_message_id="")

        file_voice = './files/summary_choice_bot.opus'

        if user_info["speaker"] == "Anastasia":
            file_voice = './files/summary_choice_nastya.opus'

        await bot.send_voice(
            tg_id,
            types.InputFile(file_voice),
            parse_mode=ParseMode.HTML,
            reply_markup=markup
        )

