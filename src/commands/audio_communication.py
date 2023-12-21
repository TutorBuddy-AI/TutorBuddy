from src.config import dp, bot
from src.utils.user import UserCreateMessage
from utils.generate.communication import CommunicationGenerate
from src.utils.transcriber import SpeechToText, TextToSpeech
from aiogram import types, md


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action='record_audio')

    user_text = await SpeechToText(file_id=message.voice.file_id).get_text()

    user_service = UserCreateMessage(
        tg_id=str(message.chat.id),
        prompt=user_text,
        type_message="audio"
    )

    generated_text = await CommunicationGenerate(
        tg_id=str(message.chat.id),
        prompt=user_text,
        user_message_history=await user_service.get_user_message_history()).generate_message()

    audio = await TextToSpeech(prompt=generated_text, tg_id=str(message.from_user.id)).get_speech()

    await bot.send_audio(message.chat.id, audio)
