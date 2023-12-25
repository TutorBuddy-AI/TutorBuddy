from src.config import dp, bot
from src.utils.user import UserService

from aiogram import types, md


@dp.callback_query_handler(text="talk_show_scenario")
async def start_talk_show_scenario(query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
    except:
        pass
