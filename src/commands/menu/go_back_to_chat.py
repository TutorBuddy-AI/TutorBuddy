from src.config import dp, bot

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import md


@dp.callback_query_handler(text="go_back", state="*")
async def go_back_query_handler(query: CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 1)
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id - 2)
    except:
        pass

    await bot.send_message(query.message.chat.id, md.escape_md("Great!\nSend me message below ⬇"))

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

