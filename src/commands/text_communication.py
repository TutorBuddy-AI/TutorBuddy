import asyncio
import json
import re

from aiogram.dispatcher import FSMContext
from src.commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from aiogram.types import CallbackQuery, Message

from src.utils.answer.answer_renderer import translation_data, mistakes_data, AnswerRenderer
from src.utils.message import MessageHelper
from src.utils.message.message_service import MessageService
from src.utils.message_hint.message_hint_creator import MessageHintCreator
from src.utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from src.utils.message_hint.message_hint_service import MessageHintService
from src.utils.message_history_mistakes.message_mistakes_creator import MessageMistakesCreator
from src.utils.message_translation import MessageTranslationService
from src.utils.message_translation.message_translation_creator import MessageTranslationCreator
from src.utils.paraphrasing import MessageParaphraseService
from aiogram import types, md
from src.utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator
from src.utils.stciker.sticker_sender import StickerSender
from aiogram.utils.callback_data import CallbackData

from src.utils.user import UserService
from src.texts.texts import get_pin_message


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_get_text_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    await handler.handle_text_message()


@dp.callback_query_handler(text="request_hint")
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

    await bot.send_message(message.chat.id, md.escape_md(generated_text))
    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@dp.callback_query_handler(mistakes_data.filter())
async def handle_get_mistakes(query: CallbackQuery, callback_data: mistakes_data):
    message = query.message

    user_message = await MessageService().get_message(str(message.chat.id), int(callback_data["user_message_id"]))
    generated_text = await MessageMistakesCreator(
        tg_id=str(message.chat.id),
        message_text=user_message.message
    ).create_communication_message_text()

    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
        int(callback_data["user_message_id"]), int(callback_data["bot_message_id"]),
        user_message.type, message, generated_text)

    await MessageMistakesService().create_mistakes(mistakes_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text),
                           reply_markup=AnswerRenderer.get_markup_text_translation_standalone(for_user=True),
                           reply_to_message_id=callback_data["user_message_tgid"])


@dp.callback_query_handler(translation_data.filter())
async def handle_get_translation(query: CallbackQuery, callback_data: translation_data):
    """
    Callback to translate message caption. Text is provided in query message,
    Message ids are provided in callback_data
    """
    message = query.message

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text(message.caption)

    user_message_id = int(callback_data["user_message_id"]) if callback_data["user_message_id"] else None
    bot_message_id = int(callback_data["bot_message_id"]) if callback_data["bot_message_id"] else None
    helper_info = await MessageHelper().group_message_helper_info(
        user_message_id, bot_message_id, message, generated_text)

    await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text), reply_to_message_id=message.message_id)


@dp.callback_query_handler(text="request_text_translation_standalone", state="*")
async def handle_get_translation_text_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message text, when user is not logged in
    """
    state_data = await state.get_data()
    message = query.message
    lang = state_data["tg_language"] if "tg_language" in state_data else "RU"

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text_standalone(message.text, lang)

    await bot.send_message(message.chat.id, md.escape_md(generated_text), reply_to_message_id=message.message_id)


@dp.callback_query_handler(text="request_caption_translation_standalone", state="*")
async def handle_get_translation_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message caption, when user is not logged in
    """
    state_data = await state.get_data()
    message = query.message
    lang = state_data["tg_language"] if "tg_language" in state_data else "RU"

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text_standalone(message.caption, lang)

    await bot.send_message(message.chat.id, md.escape_md(generated_text), reply_to_message_id=message.message_id)


@dp.callback_query_handler(text="request_text_translation_standalone_for_user", state="*")
async def handle_get_translation_text_standalone_for_user(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message text, when user is not logged in
    """
    message = query.message
    user_info = await UserService().get_user_info(message.chat.id)
    lang = user_info["native_lang"]

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text_standalone(message.text, lang)

    await bot.send_message(message.chat.id, md.escape_md(generated_text), reply_to_message_id=message.message_id)


@dp.callback_query_handler(text="request_caption_translation_standalone_for_user", state="*")
async def handle_get_translation_standalone(query: CallbackQuery, state: FSMContext):
    """
    Callback to translate standalone message caption, when user is not logged in
    """
    message = query.message
    user_info = await UserService().get_user_info(message.chat.id)
    lang = user_info["native_lang"]

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text_standalone(message.caption, lang)

    await bot.send_message(message.chat.id, md.escape_md(generated_text), reply_to_message_id=message.message_id)

@dp.callback_query_handler(text="pin_message_translate", state="*")
async def handle_get_translation_pin_message(query: CallbackQuery, state: FSMContext):
    message = query.message
    await bot.send_message(message.chat.id, get_pin_message(translate=True), reply_to_message_id=message.message_id)

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
#     await bot.send_message(message.chat.id, md.escape_md(generated_text))


@dp.callback_query_handler(text="request_paraphrase")
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

    await bot.send_message(message.chat.id, md.escape_md(generated_text))

    await asyncio.sleep(3)

    await handler.render_answer(await handler.load_render_from_context())


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video_message(message: Message):
    sticker_sender = StickerSender(bot, message.chat.id, speaker="Anastasia")
    await sticker_sender.send_you_rock_sticker()


@dp.message_handler(content_types=types.ContentType.STICKER)
async def handle_sticker_message(message: Message):
    sticker_sender = StickerSender(bot, message.chat.id, speaker="Anastasia")
    await sticker_sender.send_you_rock_sticker()


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note_message(message: Message):
    sticker_sender = StickerSender(bot, message.chat.id, speaker="Anastasia")
    await sticker_sender.send_you_rock_sticker()
