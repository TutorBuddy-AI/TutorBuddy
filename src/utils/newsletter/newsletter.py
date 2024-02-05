from typing import List

from sqlalchemy import select

from src.config.initialize import bot
from src.database import session
from src.database.models import DailyNews, User
import os
import logging
from logging.handlers import RotatingFileHandler

from aiogram import types

from utils.transcriber.text_to_speech import TextToSpeech

log_directory = '/home/ubuntu/AI-TutorBuddy-bot/src/utils/newsletter/logs'
log_file_path = os.path.join(log_directory, 'newsletter.log')

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(level=logging.ERROR)


file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=5)
file_handler.setLevel(logging.ERROR)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


logging.getLogger('').addHandler(file_handler)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Newsletter:
    '''Рассылка'''
    def __init__(self):
        '''Класс не принимает аргументов'''
        ...

    async def send_newsletter(self) -> None:
        '''Отправка поста с текстом и фото (если img указан) по topic + voice'''
        query_news = select(DailyNews)
        result_news = await session.execute(query_news)
        all_news = result_news.scalars().all()

        for daily_news in all_news:
            img_list = daily_news.image
            url_img = img_list[0]['url']
            path_img = '/home/ubuntu/AI-TutorBuddy-bot/'+url_img

            tg_id_list = await self.user_topic(daily_news.topic)
            # Предварительно убрал с текста любые HTML теги так как starlette сохраняет с ними
            string = daily_news.message.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br>", "").replace("<div>", "").replace("</div>", "")

            for tgid in tg_id_list:
                try:
                    audio = await TextToSpeech(prompt=string,tg_id=tgid).get_speech()
                    #await bot.send_photo(int(tgid), types.InputFile(path_img), caption=string) #Фото и текст
                    await bot.send_photo(int(tgid), types.InputFile(path_img), caption=string,
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text="Translate", callback_data="translate_button")]
                     ]))
                    await bot.send_audio(int(tgid), audio) # Аудио по текстом
                except Exception as e:
                    logging.error(e)

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