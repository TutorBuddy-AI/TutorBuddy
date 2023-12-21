from aiogram import types, md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from src.config import dp, bot
from src.keyboards import get_keyboard_remove


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def process_cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await bot.send_message(message.chat.id, md.escape_md('Cancelled'), reply_markup=await get_keyboard_remove())