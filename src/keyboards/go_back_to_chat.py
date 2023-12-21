from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_go_back_inline_keyboard() -> InlineKeyboardMarkup:
    go_back_kb = InlineKeyboardMarkup(row_width=1)

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')

    go_back_kb.add(go_back_btn)

    return go_back_kb
