from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard
from src.utils.message_history_mistakes import MessageMistakesService

@dp.message_handler(commands=["all_mistakes"])
async def get_mistakes(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    data = await MessageMistakesService().get_user_message_history_mistakes(tg_id=str(message.chat.id))

    current_index = 0

    await state.update_data(mistakes=data)
    await state.update_data(current_index=current_index)
    await state.update_data(id_mistakes=message.message_id + 1)

    await send_data(message.chat.id, data[current_index], create_inline_keyboard(current_index, len(data)),
                    message.message_id)

def create_inline_keyboard(current_index, total_elements):
    keyboard = InlineKeyboardMarkup(row_width=3)
    prev_button = InlineKeyboardButton("⬅️", callback_data="prev")

    index_button = InlineKeyboardButton(f"{current_index + 1} / {total_elements}", callback_data="...........")

    next_button = InlineKeyboardButton("➡️", callback_data="next")

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    keyboard.row(prev_button, index_button, next_button).add(go_back_btn)

    return keyboard

@dp.callback_query_handler(lambda query: query.data in ["prev", "next"])
async def handle_inline_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    storage = await state.get_data()

    current_index = storage["current_index"]
    data = storage["mistakes"]

    if callback_query.data == "prev":
        current_index = (current_index - 1) % len(data)
    elif callback_query.data == "next":
        current_index = (current_index + 1) % len(data)

    await state.update_data(current_index=current_index)

    await state.update_data(id_mistakes=callback_query.message.message_id + 1)
    message_id = storage["id_mistakes"]

    await send_data(callback_query.message.chat.id, data[current_index],
                    create_inline_keyboard(current_index, len(data)), message_id)


async def send_data(chat_id, data_element, keyboard, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass
    await bot.send_message(chat_id=chat_id, text=md.escape_md(data_element['message']), reply_markup=keyboard)
