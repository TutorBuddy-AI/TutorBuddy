from aiogram.dispatcher import FSMContext
from src.config import dp, bot
from src.utils.user import UserCreateMessage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, \
    CallbackQuery
from utils.message import MessageHelper
from utils.message_history_mistakes import MessageMistakesService, MessageMistakesHelper, MessageMistakesCreator
from utils.message_hint import MessageHintCreator, MessageHintService, MessageHintHelper
from utils.message_translation import MessageTranslationService, MessageTranslationHelper, MessageTranslationCreator
from utils.paraphrasing import MessageParaphraseCreator, MessageParaphraseService

from aiogram import types, md


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_get_text_message(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    generated_text = await UserCreateMessage(
        tg_id=str(message.from_user.id),
        prompt=message.text,
        type_message="text"
    ).create_communication_message_text()

    await set_message_menu(message, generated_text)


async def set_message_menu(message: types.Message, generated_text: str):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    markup = InlineKeyboardMarkup(row_width=2)

    get_mistakes_btn = InlineKeyboardButton(
        "🔴 My mistakes",
        callback_data="get_mistakes")
    get_paraphrase_btn = InlineKeyboardButton(
        '📈 Make my text better',
        callback_data="get_paraphrase")
    get_hint_btn = InlineKeyboardButton(
        '💡 Hint',
        callback_data="get_hint")
    get_translation_btn = InlineKeyboardButton(
        '📖 Translate',
        callback_data="get_translation")

    markup.row(get_mistakes_btn, get_paraphrase_btn).row(get_hint_btn, get_translation_btn)

    await bot.send_message(message.from_user.id, md.escape_md(generated_text), reply_markup=markup)
    await set_message_menu(message, generated_text)


@dp.callback_query_handler(text="get_hint")
async def handle_get_hint(query: CallbackQuery, state: FSMContext):
    message = query.message
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageHintCreator(
        tg_id=str(message.from_user.id)
    ).create_communication_message_text()
    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)
    await MessageHintService().create_message_hint(helper_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    await set_message_menu(message, bot_answer_text)


@dp.callback_query_handler(text="get_mistakes")
async def handle_get_mistakes(query: CallbackQuery, state: FSMContext):
    message = query.message
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageMistakesCreator(
        tg_id=str(message.from_user.id)
    ).create_communication_message_text()
    mistakes_info = await MessageHelper().group_message_helper_info(
        state_data, message, generated_text)
    await MessageMistakesService().create_mistakes(mistakes_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    await set_message_menu(message, bot_answer_text)


@dp.callback_query_handler(text="get_translation")
async def handle_get_translation(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message = query.message
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageTranslationCreator(
        tg_id=str(message.from_user.id),
        message=state_data["bot_message_text"]
    ).create_communication_message_text()
    helper_info = await MessageHelper().group_message_helper_info(
        state_data, message, generated_text)
    await MessageTranslationService().create_translation(helper_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    await set_message_menu(message, state_data["bot_message_text"])


@dp.message_handler(commands=["get_paraphrase"])
async def handle_get_paraphrase(query: CallbackQuery, state: FSMContext):
    message = query.message
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    state_data = await state.get_data()

    generated_text = await MessageParaphraseCreator(
        tg_id=str(message.from_user.id)
    ).create_communication_message_text()
    helper_info = await MessageHelper().group_message_helper_info(state_data, message, generated_text)
    await MessageParaphraseService().create_message_paraphrase(helper_info)
    await bot.send_message(message.from_user.id, md.escape_md(generated_text))
    await set_message_menu(message, bot_answer_text)
