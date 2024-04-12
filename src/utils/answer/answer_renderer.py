import json

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from src.utils.answer.answer import Answer
from src.utils.answer.render import Render


class TranslationData(CallbackData, prefix="translate"):
    action: str
    bot_message_id: str
    user_message_id: str


class MistakesData(CallbackData, prefix="mistakes"):
    action: str
    bot_message_id: str
    user_message_id: str
    user_message_tgid: str


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
            text=f"🔴 My mistakes",
            callback_data="request_mistakes")

    def get_user_message_markup(self, num_mistakes: int = 0) -> InlineKeyboardMarkup:
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

        return InlineKeyboardMarkup(inline_keyboard=[buttons_list])

    def get_answer_markup(self) -> InlineKeyboardMarkup:

        # get_hint_btn = InlineKeyboardButton(
        #     '💡 Hint',
        #     callback_data="request_hint")
        get_mistake_btn = InlineKeyboardButton(
            text='🔴 Mistakes',
            callback_data=MistakesData(
                action="request_mistakes",
                bot_message_id=str(self.bot_message_id),
                user_message_id=str(self.user_message_id),
                user_message_tgid=str(self.reply_to_message_id)
            ).pack()
        )
        get_translation_btn = InlineKeyboardButton(
            text='📖 Translate',
            callback_data=TranslationData(
                action="request_caption_translation",
                bot_message_id=str(self.bot_message_id),
                user_message_id=str(self.user_message_id)
            ).pack()
        )
        return InlineKeyboardMarkup(inline_keyboard=[[get_translation_btn, get_mistake_btn]])

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
            text='📖 Translate',
            callback_data=TranslationData(
                action="request_caption_translation",
                bot_message_id=str(bot_message_id),
                user_message_id=str(user_message_id)
            ).pack()
        )

        return get_translation_btn

    @staticmethod
    def get_markup_caption_translation(bot_message_id: str, user_message_id: str) -> InlineKeyboardMarkup:

        get_translation_btn = InlineKeyboardButton(
            text='📖 Translate',
            callback_data=TranslationData(
                action="request_caption_translation",
                bot_message_id=str(bot_message_id),
                user_message_id=str(user_message_id)
            ).pack())

        return InlineKeyboardMarkup(inline_keyboard=[[get_translation_btn]])

    @staticmethod
    def get_button_text_translation_standalone(for_user=False):
        return InlineKeyboardButton(
            text='📖 Translate',
            callback_data=f"""request_text_translation_standalone{"_for_user" if for_user else ""}""")

    @staticmethod
    def get_button_caption_translation_standalone(for_user=False):
        return InlineKeyboardButton(
            text='📖 Translate',
            callback_data=f"""request_caption_translation_standalone{"_for_user" if for_user else ""}""")

    @staticmethod
    def get_markup_text_translation_standalone(for_user=False) -> InlineKeyboardMarkup:
        get_translation_btn = AnswerRenderer.get_button_text_translation_standalone(for_user)

        return InlineKeyboardMarkup(inline_keyboard=[[get_translation_btn]])

    @staticmethod
    def get_markup_caption_translation_standalone(for_user=False) -> InlineKeyboardMarkup:
        get_translation_btn = AnswerRenderer.get_button_caption_translation_standalone(for_user)

        return InlineKeyboardMarkup(inline_keyboard=[[get_translation_btn]])

    @staticmethod
    def get_start_talk_markup_with_ids(bot_message_id) -> InlineKeyboardMarkup:
        get_translation_btn = InlineKeyboardButton(
            text='📖 Translate',
            callback_data=TranslationData(
                action="request_caption_translation",
                bot_message_id=str(bot_message_id),
                user_message_id=""
            ).pack()
        )
        bot_message_markup = InlineKeyboardMarkup(inline_keyboard=[[get_translation_btn]])
        return bot_message_markup
