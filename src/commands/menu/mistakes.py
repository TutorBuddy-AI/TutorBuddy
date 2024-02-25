from aiogram import types, md
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.config import dp, bot
from src.filters import IsNotRegister
from src.filters.is_not_register_filter import IsRegister
from src.utils.answer import AnswerRenderer
from src.utils.message_history_mistakes import MessageMistakesService


@dp.message_handler(IsRegister(), commands=["all_mistakes"])
async def get_mistakes(message: types.Message, state: FSMContext):

    data = await MessageMistakesService().get_user_message_history_mistakes(tg_id=str(message.chat.id))

    current_index = 0
    if len(data) != 0:
        await state.update_data(mistakes=data)
        await state.update_data(current_index=current_index)
        await state.update_data(id_mistakes=message.message_id + 1)

        await send_data(message.chat.id, data[current_index], create_inline_keyboard(current_index, len(data)),
                        message.message_id)
    else:
        await bot.send_message(message.chat.id,
                               md.escape_md("You haven't ever requested to find mistakes in your messages."))


@dp.message_handler(IsNotRegister(), commands=["feedback"])
async def edit_profile_handler(message: types.Message):
    translate_markup = AnswerRenderer.get_markup_text_translation_standalone(for_user=False)
    await bot.send_message(message.chat.id, text=md.escape_md("Please, register first"), reply_markup=translate_markup)


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
    try:
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id)
    except:
        pass


async def send_data(chat_id, data_element, keyboard, message_id):
    if data_element is None:
        await bot.send_message(chat_id=chat_id, text=md.escape_md("You don't have any mistakes"), reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=chat_id, text=md.escape_md(data_element['message']), reply_markup=keyboard)
