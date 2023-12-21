from aiogram import types, md
from aiogram.dispatcher import FSMContext

from src.config import dp, bot
from src.keyboards import get_go_back_inline_keyboard

@dp.message_handler(commands=["all_mistakes"])
async def get_mistakes(message: types.Message):
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

    await bot.send_message(message.from_user.id, "До 25 будет готово",
                           reply_markup=await get_go_back_inline_keyboard())
