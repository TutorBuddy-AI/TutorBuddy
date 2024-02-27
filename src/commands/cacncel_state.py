from aiogram import types, md, F, Router
from aiogram.fsm.context import FSMContext

from src.config import bot
from src.keyboards import get_keyboard_remove

cancel_router = Router(name=__name__)


@cancel_router.message(F.state == "*", F.commands == "cancel")
@cancel_router.message(F.text.lower() == "cancel", F.state == "*")
async def process_cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()

    await bot.send_message(message.chat.id, md.escape_md('Cancelled'), reply_markup=await get_keyboard_remove())