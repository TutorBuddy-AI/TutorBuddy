import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from src.utils.answer.answer import Answer
from src.utils.answer.render import Render

translation_data = CallbackData("translate", 'action', 'bot_message_id', "user_message_id")
mistakes_data = CallbackData("mistakes", 'action', 'bot_message_id', "user_message_id")


class AnswerRenderer:
    """Class to present generation results in messages"""
    def __init__(
        self, answer: Answer, message_text: str, reply_to_message_id, message_type: str,
        bot_message_id: str, user_message_id: str
    ):
        self.answer = answer
        self.answer_text = answer.answer_text
        self.reply_to_message_id = reply_to_message_id
        self.are_mistakes_provided = answer.are_mistakes_provided
        self.mistakes = answer.mistakes
        self.message_text = message_text
        self.message_type = message_type

        self.bot_message_id = bot_message_id
        self.user_message_id = user_message_id

    @staticmethod
    def get_mistakes_button(are_mistakes_provided: bool, num_mistakes: int = 0) -> InlineKeyboardButton:
        """
        Function provides button to generate mistakes if they were not provided and button to get them if they were
        """
        # ToDo fix if misttakes in json are ok
        # if are_mistakes_provided:
        #     return InlineKeyboardButton(
        #         f"""🔴 My mistakes [{num_mistakes}]""", callback_data="get_mistakes")
        # else:
        #     return InlineKeyboardButton(
        #         f"🔴 My mistakes",
        #         callback_data="request_mistakes")
        return InlineKeyboardButton(
            f"🔴 My mistakes",
            callback_data="request_mistakes")

    def get_user_message_markup(self, num_mistakes: int = 0) -> InlineKeyboardMarkup:
        user_message_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

        buttons_list = list([
            # InlineKeyboardButton(
            # '📈 Say it better',
            # callback_data="request_paraphrase")
        ])
        # ToDo fix if misttakes in json are ok
        # mistakes button won't be provided only if mistakes were provided as empty list
        # if (self.are_mistakes_provided and (num_mistakes != 0)) or (not self.are_mistakes_provided):
        #     buttons_list.append(self.get_mistakes_button(self.are_mistakes_provided, num_mistakes))
        buttons_list.append(self.get_mistakes_button(self.are_mistakes_provided, num_mistakes))

        return user_message_markup.row(*buttons_list)

    def get_answer_markup(self) -> InlineKeyboardMarkup:
        bot_message_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

        # get_hint_btn = InlineKeyboardButton(
        #     '💡 Hint',
        #     callback_data="request_hint")
        get_mistake_btn = InlineKeyboardButton(
            '🔴 Mistakes',
            callback_data=mistakes_data.new(
                action="request_mistakes",
                bot_message_id=self.bot_message_id,
                user_message_id=self.user_message_id
            )
        )
        get_translation_btn = InlineKeyboardButton(
            '📖 Translate',
            callback_data=translation_data.new(
                action="request_caption_translation",
                bot_message_id=self.bot_message_id,
                user_message_id=self.user_message_id
            )
        )
        bot_message_markup.row(get_translation_btn, get_mistake_btn)
        return bot_message_markup

    def render(self) -> Render:
        match self.answer:
            case Answer(answer_text=None):
                return Render(
                    "Oooops, something wrong. Try request again later...",
                    self.message_text, self.reply_to_message_id, self.message_type, False)
            case Answer(answer_text=answ_text, are_mistakes_provided=False):
                user_message_markup = self.get_user_message_markup(0)
                bot_message_markup = self.get_answer_markup()
                return Render(
                    self.answer_text, self.message_text, self.reply_to_message_id,
                    self.message_type, True, user_message_markup, bot_message_markup
                )
            case _:
                user_message_markup = self.get_user_message_markup(len(self.mistakes))
                bot_message_markup = self.get_answer_markup()
                return Render(
                    self.answer_text, self.message_text, self.reply_to_message_id,
                    self.message_type, True, user_message_markup, bot_message_markup
                )

    @staticmethod
    def get_button_caption_translation(bot_message_id: str, user_message_id: str):
        get_translation_btn = InlineKeyboardButton(
            '📖 Translate',
            callback_data=translation_data.new(
                action="request_caption_translation",
                bot_message_id=bot_message_id,
                user_message_id=user_message_id
            )
        )

        return get_translation_btn

    @staticmethod
    def get_markup_caption_translation(bot_message_id: str, user_message_id: str) -> InlineKeyboardMarkup:
        bot_message_markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        get_translation_btn = InlineKeyboardButton(
            '📖 Translate',
            callback_data=translation_data.new(
                action="request_caption_translation",
                bot_message_id=bot_message_id,
                user_message_id=user_message_id
            ))

        bot_message_markup.row(get_translation_btn)
        return bot_message_markup

    @staticmethod
    def get_button_text_translation_standalone(for_user=False):
        return InlineKeyboardButton(
            '📖 Translate',
            callback_data=f"""request_text_translation_standalone{"_for_user" if for_user else ""}""")

    @staticmethod
    def get_button_caption_translation_standalone(for_user=False):
        return InlineKeyboardButton(
            '📖 Translate',
            callback_data=f"""request_caption_translation_standalone{"_for_user" if for_user else ""}""")

    @staticmethod
    def get_markup_text_translation_standalone(for_user=False) -> InlineKeyboardMarkup:
        bot_message_markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        get_translation_btn = AnswerRenderer.get_button_text_translation_standalone(for_user)

        bot_message_markup.row(get_translation_btn)
        return bot_message_markup

    @staticmethod
    def get_markup_caption_translation_standalone(for_user=False) -> InlineKeyboardMarkup:
        bot_message_markup = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        get_translation_btn = AnswerRenderer.get_button_caption_translation_standalone(for_user)

        bot_message_markup.row(get_translation_btn)
        return bot_message_markup

    @staticmethod
    def get_start_talk_markup_with_ids(bot_message_id) -> InlineKeyboardMarkup:
        bot_message_markup = InlineKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)

        get_translation_btn = InlineKeyboardButton(
            '📖 Translate',
            callback_data=translation_data.new(
                action="request_caption_translation",
                bot_message_id=bot_message_id,
                user_message_id=""
            )
        )
        bot_message_markup.row(get_translation_btn)
        return bot_message_markup
