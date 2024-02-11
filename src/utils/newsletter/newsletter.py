from typing import List
from sqlalchemy import select
import io
from src.config.initialize import bot
from src.database import session, Transactional
from src.database.models import DailyNews, User
import os
import logging
from logging.handlers import RotatingFileHandler
from aiogram import types
from src.database.models.message_history import MessageHistory
from utils.transcriber.text_to_speech import TextToSpeech
from aiogram.utils.markdown import spoiler, text
from aiogram.types import ParseMode
import subprocess
from io import BytesIO
from src.utils.answer.answer_renderer import AnswerRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import asyncio
from src.utils.generate import GenerateAI
from src.utils.user.user_service import UserService

log_directory = '/home/ubuntu/AI-TutorBuddy-bot/src/utils/newsletter/logs'
log_file_path = os.path.join(log_directory, 'newsletter.log')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
logging.basicConfig(level=logging.ERROR)
file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logging.getLogger('').addHandler(file_handler)


async def convert_bytes_to_ogg(audio_bytes, name_file):
    '''На самом деле возвращать булевое значение не нужно, сделал для проверки себя'''
    try:
        logging.error(f'Приняли файл {name_file}')
        # Создаем файлоподобный объект BytesIO из байтов аудио
        audio_stream = BytesIO(audio_bytes)
        # Вызываем ffmpeg, передавая байты аудио через stdin
        subprocess.run(['ffmpeg', '-i', 'pipe:0', '-c:a', 'libopus', name_file], input=audio_bytes, check=True)
        return True
    except Exception as e:
        logging.error(f"ERROR CONVERTER OGG: {e}")
        return False


class Newsletter:
    '''Рассылка'''

    def __init__(self):
        '''Класс не принимает аргументов'''
        ...

    @Transactional()
    async def send_newsletter(self) -> None:
        '''Отправка поста с текстом и фото (если img указан) по topic + voice'''
        query_news = select(DailyNews)
        result_news = await session.execute(query_news)
        all_news = result_news.scalars().all()

        for daily_news in all_news:
            img_list = daily_news.image
            url_img = img_list[0]['url']
            # Вытаскиваем img куда мы сохранили его в admin панеле
            path_img = '/home/ubuntu/AI-TutorBuddy-bot/' + url_img

            # Вызов метода, передавая topic, ожидаем лист из tg_id в str
            tg_id_list = await self.user_topic(daily_news.topic)

            # Предварительно убрал с текста любые HTML теги, так как starlette сохраняет с ними
            # Вывести текст с <p> и <br> просто ?возможно? (не проверял еще), но в caption точно не принимает их
            string = daily_news.message.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace(
                "</strong>", "").replace("<br>", "").replace("<div>", "").replace("</div>", "")
            for tgid in tg_id_list:
                try:
                    save_db = MessageHistory(
                        tg_id=tgid,
                        message=string,
                        role='assistant',
                        type='text'
                    )
                    # Сохранение в MessageHistory текст поста
                    session.add(save_db)
                    file_name_post = 'output.ogg'
                    voice = await self.get_voice(tgid)
                    audio = await TextToSpeech.get_speech_by_voice(voice, string)
                    await convert_bytes_to_ogg(audio, file_name_post)
                    audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_name_post}')
                    # Написал метод get_tranlate_markup где только кнопка translate, она пока не работает, хотя callback тот же что и у обычной
                    markup = AnswerRenderer.get_translate_markup()
                    # Отправка фото с текстом newsletter под ним
                    text_photo = await bot.send_photo(int(tgid),
                                                      types.InputFile(path_img),
                                                      caption=string,
                                                      reply_markup=InlineKeyboardMarkup().add(
                                                          InlineKeyboardButton(text='Original article ➡️📃',
                                                                               web_app=WebAppInfo(
                                                                               url="https://tutorbuddyai.tech"))))
                    # Удаляю файл ogg который мы отправили как войс месседж (думаю можно сделать без сохранение в проекте,а сразу передать но не получилось)
                    os.remove(f'/home/ubuntu/AI-TutorBuddy-bot/{file_name_post}')
                    # Отправка голосового сообщение. Озвучка newsletter
                    await bot.send_voice(int(tgid), audio_input_file, reply_markup=markup)
                    # Задержка перед вопросом user
                    await asyncio.sleep(2)
                    file_name_reply = 'output3.ogg'

                    voice = await self.get_voice(tgid)

                    payload = await self.get_payload(tgid, string)

                    generated_text = await GenerateAI(
                        request_url="https://api.openai.com/v1/chat/completions").send_request(payload=payload)

                    answer = generated_text["choices"][0]["message"]["content"]

                    audio = await TextToSpeech.get_speech_by_voice(voice, answer)
                    await convert_bytes_to_ogg(audio, file_name_reply)
                    audio_input_file = types.InputFile(f'/home/ubuntu/AI-TutorBuddy-bot/{file_name_reply}')
                    # Отправка вопроса юзера по поводу newsletter голосовое сообщение
                    await bot.send_voice(int(tgid),
                                         audio_input_file,
                                         caption=f'<span class="tg-spoiler">{answer}</span>',
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=markup,
                                         reply_to_message_id=text_photo.message_id)
                    # Удаляю файл ogg который мы отправили как войс месседж (думаю можно сделать без сохранение в проекте,а сразу передать но не получилось)
                    os.remove(f'/home/ubuntu/AI-TutorBuddy-bot/{file_name_reply}')

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
                f"{string}. In line 1, briefly express your complimentary opinion about this article based on the main ideas from it, and in line 2, ask your interlocutor about his/her opinion about this article. Continue discussing this article with him/her, briefly respond to his/her messages and always ask a logical question to continue the dialogue."
        }
        logging.error(translate_request)

        extended_history = [service_request]
        extended_history.append(translate_request)

        return {
            "model": "gpt-3.5-turbo",
            "messages": extended_history,
            "max_tokens": 100
        }
