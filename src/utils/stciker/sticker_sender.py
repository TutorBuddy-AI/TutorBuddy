from src.utils.stciker.sticker_pack import pack_map
from src.utils.answer.answer_renderer import AnswerRenderer


class StickerSender:
    def __init__(self, bot, chat_id, speaker):
        self.bot = bot
        self.chat_id = chat_id
        self.pack = pack_map[speaker]

    async def send_problem_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["problem"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("problem")
        )

    async def send_miss_you_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["miss_you"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("miss_you")
        )

    async def send_you_rock_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["you_rock"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("you_rock")
        )

    async def send_fabulous(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["fabulous"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("fabulous")
        )

    async def send_yas_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["yas"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("yas")
        )

    async def send_how_you_doin_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["how_you_doin"],
            reply_to_message_id=reply_to,
            reply_markup=AnswerRenderer.get_markup_sticker_translation("how_you_doin")
        )

    # ---------------------------------------------------------
    # Use for first time send

    # async def first_send_problem_sticker(self, reply_to=None):
    #     await self.send_problem_sticker(reply_to)
    #     text = sticker_text[self.pack["problem"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'😧{text}\n<span class="tg-spoiler">{"😧" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
    #
    # async def first_send_miss_you_sticker(self, reply_to=None):
    #     await self.send_miss_you_sticker(reply_to)
    #     text = sticker_text[self.pack["miss_you"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'😓{text}\n<span class="tg-spoiler">{"😓" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
    #
    # async def first_send_you_rock_sticker(self, reply_to=None):
    #     await self.send_you_rock_sticker(reply_to)
    #     text = sticker_text[self.pack["you_rock"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'😎{text}\n<span class="tg-spoiler">{"😎" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
    #
    # async def first_send_fabulous(self, reply_to=None):
    #     await self.send_fabulous(reply_to)
    #     text = sticker_text[self.pack["fabulous"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'👏{text}\n<span class="tg-spoiler">{"👏" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
    #
    # async def first_send_yas_sticker(self, reply_to=None):
    #     await self.send_yas_sticker(reply_to)
    #     text = sticker_text[self.pack["yas"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'👍{text}\n<span class="tg-spoiler">{"👍" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
    #
    # async def first_send_how_you_doin_sticker(self, reply_to=None):
    #     await self.send_how_you_doin_sticker(reply_to)
    #     text = sticker_text[self.pack["how_you_doin"]]
    #     await self.bot.send_message(chat_id=self.chat_id,
    #                                 text=f'✌🏻{text}\n<span class="tg-spoiler">{"✌🏻" + sticker_text_translate[text]}</span>',
    #                                 parse_mode=ParseMode.HTML)
