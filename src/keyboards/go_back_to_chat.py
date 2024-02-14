from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.utils.answer import AnswerRenderer


async def get_go_back_inline_keyboard() -> InlineKeyboardMarkup:
    go_back_kb = InlineKeyboardMarkup(row_width=1)

    go_back_btn = InlineKeyboardButton(text='Go back to chat 💬', callback_data='go_back')
    translate_button = AnswerRenderer.get_button_text_translation_standalone(for_user=True)

    go_back_kb.add(go_back_btn, translate_button)

    return go_back_kb
