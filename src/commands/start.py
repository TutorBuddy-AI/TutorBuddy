from src.config import dp, bot

from aiogram import types, md


@dp.message_handler(commands=["start"])
async def menu_handler(message: types.Message):
    await bot.send_message(message.chat.id, md.escape_md("Let's go!\n"
                                                         "Send me message below ⬇️"))
