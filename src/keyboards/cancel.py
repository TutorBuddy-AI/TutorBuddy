from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_cancel_keyboard_button() -> ReplyKeyboardMarkup:
    cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True)

    cancel_btn = KeyboardButton("Cancel")

    cancel_kb.add(cancel_btn)

    return cancel_kb
