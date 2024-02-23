from aiogram import types


async def get_keyboard_languages_markup():
    keyboard_languages_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard_languages_markup.add("Русский", "Английский")
    return keyboard_languages_markup


async def get_keyboard_remove():
    return types.ReplyKeyboardRemove()