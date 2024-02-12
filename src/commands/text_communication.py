import asyncio
import re

from aiogram.dispatcher import FSMContext
from src.commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from aiogram.types import CallbackQuery, Message
from src.utils.message import MessageHelper
from src.utils.message_hint.message_hint_creator import MessageHintCreator
from src.utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper
from src.utils.message_hint.message_hint_service import MessageHintService
from src.utils.message_history_mistakes.message_mistakes_creator import MessageMistakesCreator
from src.utils.message_translation import MessageTranslationService
from src.utils.message_translation.message_translation_creator import MessageTranslationCreator
from src.utils.paraphrasing import MessageParaphraseService
from aiogram import types, md
from src.utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator

from utils.paraphrasing.message_paraphrase_creator import MessageParaphraseCreator
from utils.user import UserService, UserCreateMessage
from utils.stciker.sticker_sender import StickerSender

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


@dp.callback_query_handler(text="request_mistakes")
async def handle_get_mistakes(query: CallbackQuery, state: FSMContext):
    message = query.message

    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    state_data = await state.get_data()

    generated_text = await MessageMistakesCreator(
        tg_id=str(message.chat.id),
        message_text=state_data["user_message_text"]
    ).create_communication_message_text()

    mistakes_info = await MessageMistakesHelper().group_message_mistakes_info(
        state_data, message, generated_text)

    await MessageMistakesService().create_mistakes(mistakes_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))


@dp.callback_query_handler(text="request_caption_translation")
async def handle_get_translation(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message

    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text(message.caption)

    helper_info = await MessageHelper().group_message_helper_info(
        state_data, message, generated_text)

    await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))


@dp.callback_query_handler(text="request_caption_translation_standalone")
async def handle_get_translation_standalone(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message

    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text(message.text)

    # helper_info = await MessageHelper().group_message_helper_info(
    #     state_data, message, generated_text)

    # await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))


@dp.callback_query_handler(lambda query: query.data.startswith("request_translation:"))
async def handle_get_translation_for_message(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message
    text = query.data.replace("request_translation:", "", 1)

    handler = CommunicationHandler(message, state, bot)
    await handler.init()

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.chat.id)
    ).create_communication_message_text(text)

    # helper_info = await MessageHelper().group_message_helper_info(
    #     state_data, message, generated_text)

    # await MessageTranslationService().create_translation(helper_info)

    await bot.send_message(message.chat.id, md.escape_md(generated_text))


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
