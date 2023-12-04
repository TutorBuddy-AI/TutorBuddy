from src.config import dp, bot
from src.utils.user import UserCreateMessage
from src.utils.transcriber import SpeechToText, TextToSpeech
from aiogram import types, md


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message):
    # gif_message = await bot.send_animation(message.chat.id, open("src/gifs/kotik.gif", 'rb'))
    await bot.send_chat_action(chat_id=message.chat.id, action='record_audio')

    user_text = await SpeechToText(file_id=message.voice.file_id).get_text()

    generated_text = await UserCreateMessage(
        tg_id=str(message.from_user.id),
        prompt=user_text,
        type_message="audio"
    ).create_communication_message_text()

    audio = await TextToSpeech(prompt=generated_text, tg_id=str(message.from_user.id)).get_speech()

    await bot.send_audio(message.chat.id, audio)
    # await bot.delete_message(message.chat.id, gif_message.message_id)
