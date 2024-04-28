import asyncio

from aiogram.filters import Command

from filters.is_not_register_filter import IsRegister

from src.config import bot
import html

from aiogram.fsm.context import FSMContext
from aiogram import types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.enums.parse_mode import ParseMode

from utils.newsletter.newsletter_service import NewsletterService
from aiogram import Router

news_gallery_router = Router(name=__name__)


@news_gallery_router.message(IsRegister(), Command("news_gallery"))
async def get_news_gallery(message: types.Message, state: FSMContext):
    data = await NewsletterService().get_user_newsletters_previews(str(message.chat.id))

    current_index = 0
    if len(data) != 0:
        await state.update_data(news=data)
        await state.update_data(current_index=current_index)
        await state.update_data(id_news=message.message_id + 1)

        await send_data(message.chat.id, data[current_index], create_inline_keyboard(current_index, len(data)),
                        message.message_id, change=False)
    else:
        await bot.send_message(message.chat.id,
                               text="I don't have any news for you",
                               parse_mode=ParseMode.HTML)


def create_inline_keyboard(current_index, total_elements):
    prev_button = InlineKeyboardButton(text="⬅️", callback_data="prev")

    index_button = InlineKeyboardButton(text=f"{current_index + 1} / {total_elements}", callback_data="...........")

    next_button = InlineKeyboardButton(text="➡️", callback_data="next")

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[prev_button, index_button, next_button], [go_back_btn]])

    return keyboard


@news_gallery_router.callback_query(F.data.in_(["prev", "next"]))
async def handle_inline_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    storage = await state.get_data()

    current_index = storage["current_index"]
    data = storage["news"]

    if callback_query.data == "prev":
        current_index = (current_index - 1) % len(data)
    elif callback_query.data == "next":
        current_index = (current_index + 1) % len(data)

    await state.update_data(current_index=current_index)

    await state.update_data(id_news=callback_query.message.message_id)
    message_id = storage["id_news"]

    await send_data(callback_query.message.chat.id, data[current_index],
                    create_inline_keyboard(current_index, len(data)), message_id)


async def send_data(chat_id, data_element, keyboard, message_id, change=True):
    if data_element is None:
        await bot.send_message(chat_id=chat_id, text="I don't have any news for you", parse_mode=ParseMode.HTML)
    else:
        if change:
            await bot.edit_message_media(
                media=InputMediaPhoto(
                    media=types.FSInputFile(data_element.img),
                    caption=formatting_post_text(data_element),
                    parse_mode=ParseMode.HTML
                ),
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=keyboard,
            )
        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo=types.FSInputFile(data_element.img),
                caption=formatting_post_text(data_element),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard)


def formatting_post_text(daily_news) -> str:
    post_text = f"#{daily_news.topic}\n\n"
    post_text += f"<b>{daily_news.title}</b>"

    post_text += f"\n\n{daily_news.short_content}"
    # Заменяем <br> на \n
    formatting_post_text = html.unescape(post_text.replace('<br>', ''))
    return formatting_post_text
