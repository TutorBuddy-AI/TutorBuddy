from aiogram import types, md, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.config import bot
from src.keyboards import get_keyboard_remove

cancel_router = Router(name=__name__)


@cancel_router.message(Command("cancel"))
@cancel_router.message(F.text.lower() == "cancel")
async def process_cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.clear()

    await bot.send_message(message.chat.id, 'Cancelled', parse_mode=ParseMode.HTML, reply_markup=await get_keyboard_remove())
