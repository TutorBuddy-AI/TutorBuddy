from src.config import dp, bot
from src.utils.user import UserCreateMessage

from aiogram import types, md

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_get_text_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

    generated_text = await UserCreateMessage().create_message_user(
        tg_id=str(message.from_user.id),
        prompt=message.text,
        type_message="text"
    )

    await bot.send_message(message.from_user.id, md.escape_md(generated_text))


