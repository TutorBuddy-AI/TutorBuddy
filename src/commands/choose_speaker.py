from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.utils.user import UserService

from aiogram import types, md

from states.form import FormInitTalk
from texts.texts import get_choice_is_done, get_start_talk, get_greeting_anastasia
from utils.generate.talk_initializer.talk_initializer import TalkInitializer
from utils.transcriber.text_to_speech import TextToSpeech
from utils.user import UserCreateMessage


@dp.callback_query_handler(text="continue_bot")
async def continue_dialogue_with_bot(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Tutor Bot")

    await bot.send_message(tg_id, get_choice_is_done())

    user_info = await user_service.get_user_info(tg_id=str(tg_id))
    check_text = get_start_talk(True, user_info["name"])
    await bot.send_message(query.message.chat.id, md.escape_md(check_text + "💬"))
    audio = await TextToSpeech(tg_id=tg_id, prompt=check_text).get_speech()
    await bot.send_audio(query.message.chat.id, audio)
    await state.set_state(FormInitTalk.init_user_message)

@dp.callback_query_handler(text="continue_nastya")
async def continue_dialogue_with_nastya(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(query.message.chat.id), new_speaker="Anastasia")

    await bot.send_message(query.message.chat.id, get_choice_is_done())

    greeting_nastya = get_greeting_anastasia()
    await bot.send_message(query.message.chat.id, get_greeting_anastasia())

    audio = await TextToSpeech(tg_id=tg_id, prompt=greeting_nastya).get_speech()
    await bot.send_audio(query.message.chat.id, audio)

    user_info = await user_service.get_user_info(tg_id=str(tg_id))
    check_text = get_start_talk(False, user_info["name"])
    await bot.send_message(query.message.chat.id, md.escape_md(check_text + "💬"))
    audio = await TextToSpeech(tg_id=tg_id, prompt=check_text).get_speech()
    await bot.send_audio(query.message.chat.id, audio)
    await state.set_state(FormInitTalk.init_user_message)

@dp.message_handler(state=FormInitTalk.init_user_message)
async def start_talk(message: types.Message, state: FSMContext):
    text = await TalkInitializer(message.chat.id).generate_message()

    user_service = UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=text,
        type_message="text").save_to_database_message_history(
        new_user_message_history=[
            {"role": "assistant", "content": text}
        ]
    )

    await bot.send_message(message.chat.id, md.escape_md(text))

