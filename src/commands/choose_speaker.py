from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from src.config import dp, bot
from src.utils.answer import AnswerRenderer
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.user import UserService

from aiogram import types, md

from src.states.form import FormInitTalk
from src.texts.texts import get_choice_is_done, get_start_talk, get_greeting_anastasia
from src.utils.generate.talk_initializer.talk_initializer import TalkInitializer
from src.utils.transcriber.text_to_speech import TextToSpeech
from src.utils.user import UserCreateMessage

#
# @dp.callback_query_handler(text="continue_bot")
# async def continue_dialogue_with_bot(query: types.CallbackQuery, state: FSMContext):
#     tg_id = query.message.chat.id
#     user_service = UserService()
#     await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Tutor Bot")
#
#     markup = AnswerRenderer.get_markup_text_translation_standalone()
#
#     await bot.send_message(tg_id, get_choice_is_done(), reply_markup=markup)
#
#     user_info = await user_service.get_user_info(tg_id=str(tg_id))
#     check_text = get_start_talk(True, user_info["name"])
#     audio = await TextToSpeech(tg_id=tg_id, prompt=check_text).get_speech()
#     audio_markup = AnswerRenderer.get_markup_caption_translation_standalone()
#
#     with AudioConverter(audio) as ogg_file:
#         await bot.send_voice(
#             query.message.chat.id,
#             types.InputFile(ogg_file),
#             caption=f'<span class="tg-spoiler">{check_text + "💬"}</span>',
#             parse_mode=ParseMode.HTML,
#             reply_markup=audio_markup)
#     await state.set_state(FormInitTalk.init_user_message)
#
#
# @dp.callback_query_handler(text="continue_nastya")
# async def continue_dialogue_with_nastya(query: types.CallbackQuery, state: FSMContext):
#     tg_id = query.message.chat.id
#     user_service = UserService()
#     await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Anastasia")
#
#     markup = AnswerRenderer.get_markup_text_translation_standalone()
#     await bot.send_message(query.message.chat.id, get_choice_is_done(), reply_markup=markup)
#     user_info = await user_service.get_user_info(tg_id=str(tg_id))
#     name = user_info["name"]
#     caption_text = f"Hi, {name} 😌" + get_greeting_anastasia()
#     audio = await TextToSpeech(tg_id=tg_id, prompt=f"Hi, {name} " + get_greeting_anastasia()).get_speech()
#     audio_markup = AnswerRenderer.get_markup_caption_translation_standalone()
#
#     with AudioConverter(audio) as ogg_file:
#         await bot.send_voice(
#             query.message.chat.id,
#             types.InputFile(ogg_file),
#             caption=f'<span class="tg-spoiler">{caption_text}</span>',
#             parse_mode=ParseMode.HTML,
#             reply_markup=audio_markup
#         )
#
#     check_text = get_start_talk(False, name)
#     audio = await TextToSpeech(tg_id=tg_id, prompt=check_text).get_speech()
#     with AudioConverter(audio) as ogg_file:
#         await bot.send_voice(
#             query.message.chat.id,
#             types.InputFile(ogg_file),
#             caption=f'<span class="tg-spoiler">{check_text + "💬"}</span>',
#             parse_mode=ParseMode.HTML,
#             reply_markup=audio_markup)
#     await state.set_state(FormInitTalk.init_user_message)


@dp.callback_query_handler(text="continue_bot")
async def continue_dialogue_with_bot(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Tutor Bot")

    markup = AnswerRenderer.get_markup_text_translation_standalone()
    await bot.send_message(tg_id, get_choice_is_done(), reply_markup=markup)
    await start_small_talk(query.message, state)


@dp.callback_query_handler(text="continue_nastya")
async def continue_dialogue_with_nastya(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Anastasia")

    markup = AnswerRenderer.get_markup_text_translation_standalone()
    await bot.send_message(tg_id, get_choice_is_done(), reply_markup=markup)
    await start_small_talk(query.message, state)


@dp.message_handler(state=FormInitTalk.init_user_message)
async def start_talk(message: types.Message, state: FSMContext):
    await start_small_talk(message, state)


async def start_small_talk(message: types.Message, state: FSMContext):
    text = await TalkInitializer(message.chat.id).generate_message()

    saved_message = await UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=text,
        type_message="text").save_to_database_message_history(
        new_user_message_history=[
            {"role": "assistant", "content": text}
        ]
    )
    markup = AnswerRenderer.get_start_talk_markup_with_ids(saved_message[0].id)

    audio = await TextToSpeech(tg_id=message.chat.id, prompt=text).get_speech()
    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            types.InputFile(ogg_file),
            caption=f'<span class="tg-spoiler">{text}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=markup
        )
    await state.finish()

