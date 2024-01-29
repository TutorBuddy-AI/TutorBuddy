from aiogram.types import InlineKeyboardMarkup


class Render:
    """Class that combines all info, that needed to be presented in bot's messages"""
    def __init__(
        self, answer_text: str, message_text: str, message_type: str, is_generation_successful: bool,
        user_message_markup: InlineKeyboardMarkup=None, bot_message_markup: InlineKeyboardMarkup=None
    ):
        self.answer_text = answer_text
        self.is_generation_successful = is_generation_successful
        self.user_message_markup = user_message_markup
        self.bot_message_markup = bot_message_markup
        self.message_text = message_text
        self.message_type = message_type
