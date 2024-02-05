import asyncio
from sqlalchemy import select
from aiogram.dispatcher import FSMContext

from commands.communication_handler import CommunicationHandler
from src.config import dp, bot
from src.utils.user import UserCreateMessage
from utils.generate.communication import CommunicationGenerate
from src.utils.transcriber import SpeechToText, TextToSpeech
from aiogram import types, md
from src.database import session
from src.database.models import User
from aiogram import types


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message, state: FSMContext):
    handler = CommunicationHandler(message, state, bot)
    await handler.init()
    await handler.handle_audio_message()
