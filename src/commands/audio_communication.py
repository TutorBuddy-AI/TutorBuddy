from src.config import dp, bot
from src.utils.user import UserCreateMessage
from src.utils.transcriber import SpeechToText, TextToSpeech
from aiogram import types, md


@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_get_voice_message(message: types.Message):
    gif_message = await bot.send_animation(message.chat.id, open("src/gifs/kotik.gif", 'rb'))
    await bot.send_chat_action(chat_id=message.chat.id, action='record_audio')

    user_text = await SpeechToText().get_text(message.voice.file_id)

    generated_text = await UserCreateMessage().create_message_user(
        tg_id=str(message.from_user.id),
        prompt=user_text,
        type_message="audio"
    )
    audio = await TextToSpeech().get_speech(generated_text)

    await bot.send_audio(message.chat.id, audio)
    await bot.delete_message(message.chat.id, gif_message.message_id)
