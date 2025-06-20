from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from src.texts.texts import get_pin_message
from aiogram import types

from src.utils.audio_converter.audio_converter import AudioConverter
from src.utils.transcriber.text_to_speech import TextToSpeech


async def send_pin_message(bot, chat_id, speaker, message_history):
    """after 7 messages from user send post_message"""
    if message_history == 7:
        match speaker:
            case "Anastasia":
                file_path_img = "./files/pin_message_nastya.jpg"
                file_path_voice = "./files/pin_message_nastya.opus"
            case "AA_Lingua":
                file_path_img = "./files/pin_message_aa_linqua.png"
                file_path_voice = "./files/pin_message_aa_linqua.ogg"
            case "Oksana":
                file_path_img = "./files/pin_message_oksana.png"
                file_path_voice = "./files/pin_message_oksana.ogg"
            case "Victoria":
                file_path_img = "./files/pin_message_victoria.jpg"
                file_path_voice = "./files/pin_message_victoria.ogg"
            case "Katya":
                file_path_img = "./files/pin_message_katya.png"
                file_path_voice = "./files/pin_message_katya.ogg"
            case _:  # TutorBuddy default variables.
                file_path_img = "./files/pin_message_bot.jpg"
                file_path_voice = "./files/pin_message_bot.opus"

        await bot.send_photo(chat_id,
                             photo=FSInputFile(file_path_img),
                             caption=get_pin_message(),
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [InlineKeyboardButton(text='📖 Translate', callback_data='pin_message_translate')]]
                             ))

        await bot.send_voice(chat_id, FSInputFile(file_path_voice))
    else:
        pass
