import traceback
from typing import Optional

from sqlalchemy import select
from src.config import bot, dp
from src.database import session, Transactional
from src.database.models import Newsletter, User
import os
from config import config
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

from utils.newsletter.newsletter_service import NewsletterService


class NewsletterPublisher:
    '''Рассылка'''

    def __init__(self):
        '''Класс не принимает аргументов'''
        ...

    async def send_newsletter(self, newsletter) -> None:
        '''Отправка поста с текстом и фото (если img указан) по topic + voice'''
        await self.send_single_article(newsletter)

    async def send_single_article(self, newsletter):
        # Вызов метода, передавая topic, ожидаем лист из tg_id в str
        tg_id_list = await self.user_topic(newsletter.topic)
        newsletter_audio_files = await NewsletterService.get_newsletter_audio_files(newsletter.id)

        for tg_id in tg_id_list:
            try:
                if await SettingService.is_summary_on(tg_id):
                    await self.send_summary_and_opinion_to_chat(tg_id, newsletter, newsletter_audio_files)

            except Exception as e:
                traceback.print_exc()

    async def send_summary_and_opinion_to_chat(self, tg_id: str, newsletter, newsletter_audio_files):
        newsletter_message = await self.send_summary(tg_id, newsletter, newsletter_audio_files)
        await asyncio.sleep(3)

        post_text = await NewsletterPublisher.formatting_post_text(newsletter)
        await self.send_opinion(tg_id, post_text, newsletter_message.message_id)
        await asyncio.sleep(3)

    async def send_summary(self, tg_id: str, newsletter, post_audio_files: dict[str, str]):
        newsletter_message = await NewsletterPublisher.send_newsletter_text_to_chat(newsletter, tg_id)

        voice = await self.get_voice(tg_id)

        file_path = post_audio_files[voice]

        await bot.send_voice(int(tg_id), types.FSInputFile(file_path))
        return newsletter_message

    @staticmethod
    async def send_newsletter_text_to_chat(newsletter, tg_id: str):
        path_img = newsletter.path_to_data
        post_text = await NewsletterPublisher.formatting_post_text(newsletter)
        cleaned_post_text = await NewsletterPublisher.remove_html_tags(post_text)

        newsletter_message_hist = MessageHistory(
            tg_id=tg_id,
            message=cleaned_post_text,
            role='assistant',
            type='text'
        )
        # Сохранение в MessageHistory текст поста
        session.add(newsletter_message_hist)
        await session.commit()

        post_translate_button = AnswerRenderer.get_button_caption_translation(
            bot_message_id=newsletter_message_hist.id, user_message_id="")
        newsletter_message = await bot.send_photo(
            chat_id=int(tg_id),
            photo=types.FSInputFile(path_img),
            caption=post_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text='Original article ➡️📃',
                    web_app=WebAppInfo(url=newsletter.url))
            ],
                [post_translate_button]])
        )
        return newsletter_message

    async def delete_audio_files(self, converted_files):
        for file_path in converted_files:
            if os.path.exists(file_path):
                os.unlink(file_path)

    @staticmethod
    async def remove_html_tags(post_text: str):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', post_text)

    @staticmethod
    async def formatting_post_text(newsletter):
        post_text = f"#{newsletter.topic}\n\n"
        post_text += f"<b>{newsletter.title}</b>"

        if newsletter.publisher:
            post_text += f"\n{newsletter.publisher}"
        if newsletter.publication_date:
            post_text += f"\n{newsletter.publication_date}"

        post_text += "\n\n<u>Article summary:</u>"
        post_text += f"\n{newsletter.message}"
        # Заменяем <br> на \n
        formatting_post_text = html.unescape(post_text.replace('<br>', ''))
        return formatting_post_text

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
        await session.commit()
        # audio = await TextToSpeech.get_speech_by_voice(voice, answer)
        audio = await TextToSpeech(str(tg_id), answer).get_speech()
        markup = AnswerRenderer.get_markup_caption_translation(
            bot_message_id=talk_message.id, user_message_id="")
        with AudioConverter(audio) as ogg_file:
            # Отправка вопроса юзера по поводу newsletter голосовое сообщение
            await bot.send_voice(int(tg_id),
                                 types.FSInputFile(ogg_file),
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

    async def send_newsletter_to_chat(self, newsletter, tg_id: str):
        newsletter_audio_files = await NewsletterService.get_newsletter_audio_files(newsletter.id)
        await self.send_summary(tg_id, newsletter, newsletter_audio_files)
