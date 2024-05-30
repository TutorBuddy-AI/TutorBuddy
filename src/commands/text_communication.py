import asyncio
import logging

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from src.commands.communication_handler import CommunicationHandler
from src.config import bot
from aiogram.types import CallbackQuery, Message

from src.filters.is_not_register_filter import IsRegister
from src.utils.answer.answer_renderer import TranslationData, MistakesData, AnswerRenderer, StickerTranslate
from src.utils.message import MessageHelper
from src.utils.message.message_service import MessageService
from src.utils.message_hint.message_hint_creator import MessageHintCreator
from src.utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from src.utils.message_hint.message_hint_service import MessageHintService
from src.utils.message_history_mistakes.message_mistakes_creator import MessageMistakesCreator
from src.utils.message_translation import MessageTranslationService
from src.utils.message_translation.message_translation_creator import MessageTranslationCreator
from src.utils.paraphrasing import MessageParaphraseService
from aiogram import types, md, Router, F
from src.utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator
from src.utils.stciker.sticker_sender import StickerSender
from src.utils.message.message_validator import get_text_token_size, get_caption_token_size, get_text_size_valid, \
    get_caption_size_valid
from src.utils.stciker.sticker_pack import pack_map, sticker_text, sticker_text_translate

from src.utils.user import UserService
from src.texts.texts import get_translation_text
from utils.audio_converter.audio_converter import AudioConverter
from utils.transcriber.text_to_speech import TextToSpeech

text_comm_router = Router(name=__name__)


@text_comm_router.message(IsRegister(), F.text)
async def handle_get_text_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    await handler.handle_text_message()


@text_comm_router.callback_query(F.data == "request_hint")
async def handle_get_hint(query: CallbackQuery, state: FSMContext):
    message: Message = query.message
    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    state_data = await state.get_data()

    generated_text = await MessageHintCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)

    await MessageHintService().create_message_hint(helper_info)

    await bot.send_message(message.chat.id, generated_text, parse_mode=ParseMode.HTML)
    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@text_comm_router.callback_query(MistakesData.filter())
async def handle_get_mistakes(query: CallbackQuery, callback_data: MistakesData):
    message = query.message

    user_message = await MessageService().get_message(str(message.chat.id), int(callback_data.user_message_id))
    generated_text = await MessageMistakesCreator(
        tg_id=str(message.chat.id),
        message_text=user_message.message
    ).create_communication_message_text()

    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
        int(callback_data.user_message_id), int(callback_data.bot_message_id),
        user_message.type, message, generated_text)

    await MessageMistakesService().create_mistakes(mistakes_info)

    await bot.send_message(message.chat.id, generated_text,
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True),
                           parse_mode=ParseMode.HTML,
                           reply_to_message_id=callback_data.user_message_tgid)


@text_comm_router.callback_query(TranslationData.filter())
async def handle_get_translation(query: CallbackQuery, callback_data: TranslationData):
    """
    Callback to translate message caption. Text is provided in query message,
    Message ids are provided in callback_data
    """
    message = query.message
    if not message.caption.count(" Translated text:\n"):
        user_info = await UserService().get_user_person(tg_id=str(message.chat.id))
        wait_message = await bot.send_message(message.chat.id,
                                              f"⏳ {user_info['speaker_id']}  is thinking … Please wait",
                                              parse_mode=ParseMode.HTML)
        lang = user_info['native_lang'].lower()

        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text(message.caption)

        user_message_id = int(callback_data.user_message_id) if callback_data.user_message_id else None
        bot_message_id = int(callback_data.bot_message_id) if callback_data.bot_message_id else None

        logging.error(f"User_mess_id: {user_message_id}")
        helper_info = await MessageHelper().group_message_helper_info(
            user_message_id, bot_message_id, message, generated_text)

        await MessageTranslationService().create_translation(helper_info)
        await bot.delete_message(message.chat.id, wait_message.message_id)
        if get_caption_size_valid(token):
            await bot.edit_message_caption(
                caption=message.caption + get_translation_text(lang) + generated_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(F.data == "request_text_translation_standalone")
async def handle_get_translation_text_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message text, when user is not logged in
    """
    state_data = await state.get_data()
    message = query.message
    if not message.text.count(" Translated text:\n"):
        lang = state_data["tg_language"] if "tg_language" in state_data else "RU"
        token = await get_text_token_size(len(message.text) + len(get_translation_text(lang.lower())))

        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text_standalone(message.text, lang, token)

        if get_text_size_valid(token):
            await bot.edit_message_text(
                text=message.text + get_translation_text(lang.lower()) + generated_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(F.data == "request_caption_translation_standalone")
async def handle_get_translation_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message caption, when user is not logged in
    """
    state_data = await state.get_data()
    message = query.message
    if not message.caption.count(" Translated text:\n"):
        lang = state_data["tg_language"] if "tg_language" in state_data else "RU"
        token = await get_caption_token_size(len(message.caption) + len(get_translation_text(lang.lower())))
        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text_standalone(message.caption, lang, token)
        if get_caption_size_valid(token):
            await bot.edit_message_caption(
                caption=message.caption + get_translation_text(lang.lower()) + generated_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(F.data == "request_text_translation_standalone_for_user")
async def handle_get_translation_text_standalone_for_user(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message text, when user is not logged in
    """
    message = query.message
    if not message.text.count(" Translated text:\n"):
        user_info = await UserService().get_user_info(str(message.chat.id))
        lang = user_info["native_lang"]
        token = await get_text_token_size(len(message.text) + len(get_translation_text(lang.lower())))

        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text_standalone(message.text, lang, token)

        if get_text_size_valid(token):
            await bot.edit_message_text(
                text=message.text + get_translation_text(lang.lower()) + generated_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(F.data == "request_caption_translation_standalone_for_user")
async def handle_get_translation_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message caption, when user is not logged in
    """
    message = query.message
    if not message.caption.count(" Translated text:\n"):
        user_info = await UserService().get_user_info(str(message.chat.id))
        lang = user_info["native_lang"]
        token = await get_caption_token_size(len(message.caption) + len(get_translation_text(lang.lower())))
        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text_standalone(message.caption, lang, token)

        if get_caption_size_valid(token):
            await bot.edit_message_caption(
                caption=message.caption + get_translation_text(lang.lower()) + generated_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(F.data == "pin_message_translate")
async def handle_get_translation_pin_message(query: CallbackQuery, state: FSMContext):
    message = query.message
    if not message.caption.count(" Translated text:\n"):
        user_info = await UserService().get_user_info(str(message.chat.id))
        lang = user_info["native_lang"]
        token = await get_caption_token_size(len(message.caption) + len(get_translation_text(lang.lower())))
        generated_text = await MessageTranslationCreator(
            tg_id=str(message.chat.id)
        ).create_communication_message_text_standalone(message.caption, lang, token)

        if get_caption_size_valid(token):
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.message_id,
                caption=message.caption + get_translation_text(
                    lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_markup=message.reply_markup)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=get_translation_text(lang.lower()) + generated_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id)


@text_comm_router.callback_query(StickerTranslate.filter())
async def handle_get_translation_sticker(query: CallbackQuery, state: FSMContext):
    message = query.message
    user_info = await UserService().get_user_info(str(message.chat.id))
    emoji_dict = {"problem": "😧", "miss_you": "😓", "yas": "👍", "you_rock": "😎", "how_you_doin": "✌🏻", "fabulous": "👏"}
    key_word = query.data.split(':')[-1]
    text = sticker_text[pack_map[user_info["speaker"]][key_word]]
    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text_standalone(text,
                                                   user_info["native_lang"])
    await bot.send_message(
        chat_id=message.chat.id,
        text=emoji_dict[key_word] + generated_text.rstrip(),
        parse_mode=ParseMode.HTML,
        reply_to_message_id=message.message_id)


# @dp.callback_query_handler(lambda query: query.data.startswith("request_translation:"))
# async def handle_get_translation_for_message(query: CallbackQuery, state: FSMContext):
#     """
#     Callback to translate text in callback data
#     Depricated?
#     """
#     state_data = await state.get_data()
#     message = query.message
#     text = query.data.replace("request_translation:", "", 1)
#
#     generated_text = await MessageTranslationCreator(
#         tg_id=str(message.chat.id)
#     ).create_communication_message_text(text)
#
#     helper_info = await MessageHelper().group_message_helper_info(
#         state_data, message, generated_text)
#
#     await MessageTranslationService().create_translation(helper_info)
#
#     await bot.send_message(message.chat.id, generated_text, parse_mode=ParseMode.HTML)


@text_comm_router.callback_query(F.data == "request_paraphrase")
async def handle_get_paraphrase(query: CallbackQuery, state: FSMContext):
    message = query.message

    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    state_data = await state.get_data()

    generated_text = await MessageParaphraseCreator(
        tg_id=str(message.chat.id),
        message_text=state_data["user_message_text"]
    ).create_communication_message_text()

    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)

    await MessageParaphraseService().create_message_paraphrase(helper_info)

    await bot.send_message(message.chat.id, generated_text, parse_mode=ParseMode.HTML)

    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@text_comm_router.message(IsRegister(), F.video)
async def handle_video_message(message: Message):
    user_info = await UserService().get_user_info(str(message.chat.id))
    sticker_sender = StickerSender(bot, message.chat.id, speaker=user_info["speaker"])
    await sticker_sender.send_you_rock_sticker()


@text_comm_router.message(IsRegister(), F.sticker)
async def handle_sticker_message(message: Message):
    user_info = await UserService().get_user_info(str(message.chat.id))
    sticker_sender = StickerSender(bot, message.chat.id, speaker=user_info["speaker"])
    await sticker_sender.send_you_rock_sticker()


@text_comm_router.message(IsRegister(), F.video_note)
async def handle_video_note_message(message: Message):
    user_info = await UserService().get_user_info(str(message.chat.id))
    sticker_sender = StickerSender(bot, message.chat.id, speaker=user_info["speaker"])
    await sticker_sender.send_you_rock_sticker()
