import asyncio
from sqlalchemy import select
from src.config import dp, bot
from src.utils.user import UserCreateMessage
from utils.generate.communication import CommunicationGenerate
from src.utils.transcriber import SpeechToText, TextToSpeech
from aiogram import types, md
from src.database import session
from src.database.models import User


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message):
    query_user = select(User).where(User.tg_id == str(message.chat.id))
    result_user = await session.execute(query_user)
    user = result_user.scalar()
    if user:
        speaker = user.speaker
    else:
        speaker = "Anastasia"

    query_speaker = select(User).where(User.speaker == speaker)
    result_speaker = await session.execute(query_speaker)
    speaker_data = result_speaker.scalar()
    speaker_name = speaker_data.speaker if speaker_data else "Anastasia"

    await bot.send_chat_action(chat_id=message.chat.id, action='record_audio')

    user_text = await SpeechToText(file_id=message.voice.file_id).get_text()

    user_service = UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=user_text,
        type_message="audio"
    )

    wait_message = await bot.send_message(message.chat.id, f"⏳ {speaker_name} thinks… Please wait")
    await asyncio.sleep(3)

    generated_text = await CommunicationGenerate(
        tg_id=str(message.chat.id),
        prompt=user_text,
        user_message_history=await user_service.get_user_message_history()
    ).generate_message()

    audio = await TextToSpeech(prompt=generated_text, tg_id=str(message.from_user.id)).get_speech()

    await bot.send_audio(message.chat.id, audio)
    await bot.delete_message(message.chat.id, wait_message.message_id)

