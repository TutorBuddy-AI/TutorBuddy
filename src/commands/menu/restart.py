from src.config import bot
from src.utils.answer import AnswerRenderer
from src.utils.user import UserService

from aiogram import types, md, F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

restart_router = Router(name=__name__)


@restart_router.message(F.commands == ["restart"])
async def restart_handler(message: types.Message):
    btn_yes = InlineKeyboardButton(text='Yes, restart the bot ⚙️', callback_data='restart')
    btn_no = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    restart_kb = InlineKeyboardMarkup(
        inline_keyboard=[[btn_yes, btn_no], [AnswerRenderer.get_button_text_translation_standalone(for_user=True)]])

    await bot.send_message(message.chat.id, md.escape_md("Are you sure you want to lose your progress"
                                                         " and clear the chat?"),
                           reply_markup=restart_kb)


@restart_router.callback_query(F.query.data == "restart")
async def restart_query_handler(query: CallbackQuery):
    await UserService().delete_user_info(tg_id=str(query.message.chat.id))

    await bot.send_message(
        query.message.chat.id, md.escape_md("Great, your profile is completely cleared."
                                            " Click /start to log in again"))
