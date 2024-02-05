from src.config import dp, bot
from src.utils.user import UserService

from aiogram import types, md
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(commands=["restart"])
async def restart_handler(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    restart_kb = InlineKeyboardMarkup(row_width=2)

    btn_yes = InlineKeyboardButton(text='Yes, restart the bot ⚙️', callback_data='restart')
    btn_no = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    restart_kb.row(btn_yes, btn_no)

    await bot.send_message(message.chat.id, md.escape_md("Are you sure you want to lose your progress"
                                                         " and clear the chat?"),
                           reply_markup=restart_kb)


@dp.callback_query_handler(lambda query: query.data == "restart")
async def restart_query_handler(query: CallbackQuery):
    await UserService().delete_user_info(tg_id=str(query.message.chat.id))

    await bot.send_message(query.message.chat.id, md.escape_md("Great, your profile is completely cleared."
                                                               " Click /start to log in again"),
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/start")))
