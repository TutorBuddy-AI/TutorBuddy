from aiogram.fsm.context import FSMContext

from src.commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from aiogram import types


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)
    await handler.init()
    await handler.handle_audio_message()
