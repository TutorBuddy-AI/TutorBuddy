from src.texts.texts import get_pin_message
from aiogram import types


async def send_pin_message(bot, chat_id, speaker, message_history):
    """after 7 messages from user send post_message"""
    if message_history:
        markup_translate = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text='📖 Translate', callback_data='pin_message_translate')]]
        )

        file_path_img = "./files/pin_message_bot.jpg"
        file_path_voice = "./files/bot_pin_message.opus"
        if speaker == "Anastasia":
            file_path_img = "./files/pin_message_nastya.jpg"
            file_path_voice = "./files/nastya_pin_message.opus"

        await bot.send_photo(chat_id, photo=types.InputFile(file_path_img),
                             caption=get_pin_message(translate=False), reply_markup=markup_translate)
        await bot.send_voice(chat_id, types.InputFile(file_path_voice))
    else:
        pass
