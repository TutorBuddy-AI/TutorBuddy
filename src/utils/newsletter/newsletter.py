import traceback

from sqlalchemy import select
from src.config import bot, dp
from src.database import session, Transactional
from src.database.models import DailyNews, User
import os
import logging
from logging.handlers import RotatingFileHandler
from aiogram import types
from src.database.models.message_history import MessageHistory
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.transcriber.text_to_speech import TextToSpeech
from aiogram.types import ParseMode
from src.utils.answer.answer_renderer import AnswerRenderer
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import asyncio
from src.utils.generate import GenerateAI
from src.utils.user.user_service import UserService
from markdownify import markdownify as md
# log_directory = '/home/ubuntu/AI-TutorBuddy-bot/src/utils/newsletter/logs'
# log_file_path = os.path.join(log_directory, 'newsletter.log')
# if not os.path.exists(log_directory):
#     os.makedirs(log_directory)
# logging.basicConfig(level=logging.ERROR)
# file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)
# file_handler.setLevel(logging.ERROR)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# logging.getLogger('').addHandler(file_handler)


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
            path_img = url_img

            # Вызов метода, передавая topic, ожидаем лист из tg_id в str
            tg_id_list = await self.user_topic(daily_news.topic)

            # Предварительно убрал с текста любые HTML теги, так как starlette сохраняет с ними
            # Вывести текст с <p> и <br> просто ?возможно? (не проверял еще), но в caption точно не принимает их
            post_text = md(daily_news.message)
                #          .replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace(
                # "</strong>", "").replace("<br>", "").replace("<div>", "").replace("</div>", ""))
            for tgid in tg_id_list:
                try:
                    post_message = MessageHistory(
                        tg_id=tgid,
                        message=post_text,
                        role='assistant',
                        type='text'
                    )
                    # Сохранение в MessageHistory текст поста
                    session.add(post_message)
                    voice = await self.get_voice(tgid)
                    audio = await TextToSpeech.get_speech_by_voice(voice, post_text)
                    post_translate_button = AnswerRenderer.get_button_caption_translation(
                        bot_message_id=post_message.id, user_message_id="")
                    # Отправка фото с текстом newsletter под ним
                    text_photo = await bot.send_photo(
                        chat_id=int(tgid),
                        photo=types.InputFile(path_img),
                        caption=post_text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=InlineKeyboardMarkup().row(
                            InlineKeyboardButton(
                                text='Original article ➡️📃',
                                web_app=WebAppInfo(),
                                url=daily_news.url)
                        ).row(post_translate_button)
                    )
                    # Удаляю файл ogg который мы отправили как войс месседж
                    # (думаю можно сделать без сохранение в проекте,а сразу передать но не получилось)
                    # Отправка голосового сообщение. Озвучка newsletter
                    # Написал метод get_tranlate_markup где только кнопка translate, она пока не работает,
                    # хотя callback тот же что и у обычной
                    with AudioConverter(audio) as ogg_file:
                        await bot.send_voice(int(tgid), types.InputFile(ogg_file))
                    # Задержка перед вопросом user
                    await asyncio.sleep(2)

                    voice = await self.get_voice(tgid)

                    payload = await self.get_payload(tgid, post_text)

                    generated_text = await GenerateAI(
                        request_url="https://api.openai.com/v1/chat/completions").send_request(payload=payload)

                    answer = generated_text["choices"][0]["message"]["content"]

                    talk_message = MessageHistory(
                        tg_id=tgid,
                        message=answer,
                        role='assistant',
                        type='text'
                    )
                    # Сохранение в MessageHistory текст поста
                    session.add(talk_message)
                    voice = await self.get_voice(tgid)
                    audio = await TextToSpeech.get_speech_by_voice(voice, answer)
                    markup = AnswerRenderer.get_markup_caption_translation(
                        bot_message_id=talk_message.id, user_message_id="")
                    with AudioConverter(audio) as ogg_file:
                        # Отправка вопроса юзера по поводу newsletter голосовое сообщение
                        await bot.send_voice(int(tgid),
                                             types.InputFile(ogg_file),
                                             caption=f'<span class="tg-spoiler">{answer}</span>',
                                             parse_mode=ParseMode.HTML,
                                             reply_markup=markup,
                                             reply_to_message_id=text_photo.message_id)
                    # Удаляю файл ogg который мы отправили как войс месседж
                    # (думаю можно сделать без сохранение в проекте,а сразу передать но не получилось)

                except Exception as e:
                   traceback.print_exc()

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
