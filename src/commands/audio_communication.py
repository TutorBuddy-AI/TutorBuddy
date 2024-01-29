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
    user_service = UserService()
    user_info = await user_service.get_user_info(tg_id=message.chat.id)
    if user_info:
        speaker = user.speaker
    else:
        speaker = "Anastasia"

    query_speaker = select(User).where(User.speaker == speaker)
    result_speaker = await session.execute(query_speaker)
    speaker_data = result_speaker.scalar()
    speaker_name = speaker_data.speaker if speaker_data else "Anastasia"

    wait_message = await bot.send_message(message.chat.id, f"⏳ {speaker_name} thinks… Please wait")
    handler = CommunicationHandler(message, state, bot)

    await handler.handle_audio_message()
    await bot.delete_message(message.chat.id, wait_message.message_id)

