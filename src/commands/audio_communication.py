from aiogram.fsm.context import FSMContext

from src.commands.communication_handler import CommunicationHandler
from src.config import bot
from aiogram import types, F, Router

from src.filters.is_not_register_filter import IsRegister

audio_comm_router = Router(name=__name__)


@audio_comm_router.message(IsRegister(), F.voice)
async def handle_get_voice_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)
    await handler.init()
    await handler.handle_audio_message()
