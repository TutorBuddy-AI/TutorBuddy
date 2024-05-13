import logging

from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import FSInputFile, Message

from config import config
from src.config import bot
from src.utils.answer import AnswerRenderer
from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.stciker.sticker_sender import StickerSender
from src.utils.transcriber import SpeechToText
from src.utils.user import UserService

from aiogram import types, F, Router

from src.states.form import FormInitTalk
from src.texts.texts import get_choice_is_done, get_start_talk, get_start_person_talk, get_check_text, \
    get_bot_waiting_message
from src.utils.generate.talk_initializer.talk_initializer import TalkInitializer
from src.utils.transcriber.text_to_speech import TextToSpeech
from src.utils.user import UserCreateMessage

choose_speaker_router = Router(name=__name__)


@choose_speaker_router.callback_query(F.data == "continue_bot")
async def continue_dialogue_with_bot(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(tg_id), new_speaker="TutorBuddy")

    markup = AnswerRenderer.get_markup_text_translation_standalone()

    await bot.send_message(
        tg_id, get_choice_is_done(), reply_markup=markup,
        parse_mode=ParseMode.HTML)

    sticker_sender = StickerSender(bot, query.message.chat.id, speaker="TutorBuddy")
    await sticker_sender.send_fabulous()

    user_info = await user_service.get_user_info(tg_id=str(tg_id))
    check_text = get_start_talk(True, user_info["name"])
    audio = await TextToSpeech(tg_id=str(tg_id), prompt=check_text).get_speech()
    audio_markup = AnswerRenderer.get_markup_caption_translation_standalone()

    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            query.message.chat.id,
            FSInputFile(ogg_file),
            caption=f'<span class="tg-spoiler">{check_text + "💬"}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=audio_markup)
    await state.set_state(FormInitTalk.init_user_message)


@choose_speaker_router.callback_query(F.data == "continue_nastya")
async def continue_dialogue_with_nastya(query: types.CallbackQuery, state: FSMContext):
    tg_id = query.message.chat.id
    user_service = UserService()
    await user_service.change_speaker(tg_id=str(tg_id), new_speaker="Anastasia")

    markup = AnswerRenderer.get_markup_text_translation_standalone()

    await bot.send_message(tg_id, get_choice_is_done(), reply_markup=markup,
                           parse_mode=ParseMode.HTML)

    sticker_sender = StickerSender(bot, query.message.chat.id, speaker="Anastasia")
    await sticker_sender.send_fabulous()

    user_info = await user_service.get_user_info(tg_id=str(tg_id))
    check_text = get_start_talk(True, user_info["name"])
    audio = await TextToSpeech(tg_id=str(tg_id), prompt=check_text).get_speech()
    audio_markup = AnswerRenderer.get_markup_caption_translation_standalone()

    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            query.message.chat.id,
            FSInputFile(ogg_file),
            caption=f'<span class="tg-spoiler">{check_text + "💬"}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=audio_markup)
    await state.set_state(FormInitTalk.init_user_message)


# TODO: Modify this function
async def continue_dialogue_with_person(message: Message, state: FSMContext):
    tg_id = message.chat.id

    user_service = UserService()

    user_info = await user_service.get_user_person(tg_id=str(tg_id))
    speaker = user_info["speaker_id"]
    speaker_short_name = user_info["speaker_short_name"]

    wait_message = await bot.send_message(message.chat.id, get_bot_waiting_message(speaker),
                                          parse_mode=ParseMode.HTML)

    welcome_text = get_start_person_talk(speaker, speaker_short_name)
    audio_markup = AnswerRenderer.get_markup_caption_translation_standalone()
    logging.info(f"./files/meet_{config.BOT_PERSON.lower()}.jpg")
    await bot.send_photo(
        message.chat.id,
        caption=welcome_text,
        photo=FSInputFile(f"./files/meet_{config.BOT_PERSON.lower()}.jpg"),
        parse_mode=ParseMode.HTML,
        reply_markup=audio_markup
    )

    await bot.send_voice(
        message.chat.id,
        FSInputFile(f"./files/meet_{speaker.lower()}.ogg"),
        parse_mode=ParseMode.HTML)

    await bot.delete_message(message.chat.id, wait_message.message_id)

    sticker_sender = StickerSender(bot, message.chat.id, speaker=speaker)
    await sticker_sender.send_fabulous()

    check_text = get_check_text()

    wait_message = await bot.send_message(message.chat.id, get_bot_waiting_message(speaker),
                                          parse_mode=ParseMode.HTML)

    await bot.send_voice(
        message.chat.id,
        FSInputFile(f"./files/check_{speaker.lower()}.ogg"),
        caption=f'<span class="tg-spoiler">{check_text + "💬"}</span>',
        parse_mode=ParseMode.HTML,
        reply_markup=audio_markup)
    await bot.delete_message(message.chat.id, wait_message.message_id)

    await state.set_state(FormInitTalk.init_user_message)


@choose_speaker_router.message(FormInitTalk.init_user_message, F.text)
async def start_talk(message: types.Message, state: FSMContext):
    user_service = UserService()
    user_info = await user_service.get_user_person(tg_id=str(message.chat.id))
    speaker = user_info["speaker_id"]
    #
    # wait_message = await bot.send_message(message.chat.id, f"⏳ {speaker} is thinking … Please wait",
    #                                       parse_mode=ParseMode.HTML)

    wait_message = await bot.send_message(message.chat.id, get_bot_waiting_message(speaker),
                                          parse_mode=ParseMode.HTML)

    await start_small_talk(message, state, wait_message, message_text=message.text)


@choose_speaker_router.message(FormInitTalk.init_user_message, F.voice)
async def start_talk_audio(message: types.Message, state: FSMContext):
    user_service = UserService()
    user_info = await user_service.get_user_person(tg_id=str(message.chat.id))
    speaker = user_info["speaker_id"]

    # wait_message = await bot.send_message(message.chat.id, f"⏳ {speaker} is thinking … Please wait",
    #                                       parse_mode=ParseMode.HTML)

    wait_message = await bot.send_message(message.chat.id, get_bot_waiting_message(speaker),
                                          parse_mode=ParseMode.HTML)

    message_text = await SpeechToText(file_id=message.voice.file_id).get_text()
    await bot.send_message(
        message.chat.id, f"🎙 Transcript:\n<code>{message_text}</code>", parse_mode=ParseMode.HTML,
        reply_to_message_id=message.message_id)
    await start_small_talk(message, state, wait_message, message_text)


async def start_small_talk(message: types.Message, state: FSMContext, wait_message: types.Message, message_text: str):
    text = await TalkInitializer(str(message.chat.id), message_text).generate_message()
    if not text:
        text = "Oooops, something wrong. Try request again later..."
    saved_message = await UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=text,
        type_message="text").save_to_database_message_history(
        new_user_message_history=[
            {"role": "assistant", "content": text}
        ]
    )
    markup = AnswerRenderer.get_start_talk_markup_with_ids(saved_message[0].id)

    audio = await TextToSpeech(tg_id=str(message.chat.id), prompt=text).get_speech()
    with AudioConverter(audio) as ogg_file:
        await bot.send_voice(
            message.chat.id,
            FSInputFile(ogg_file),
            caption=f'<span class="tg-spoiler">{text}</span>',
            parse_mode=ParseMode.HTML,
            reply_markup=markup,
            reply_to_message_id=message.message_id
        )
    await bot.delete_message(message.chat.id, wait_message.message_id)
    await state.clear()
