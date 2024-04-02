from src.utils.stciker.sticker_pack import pack_map


class StickerSender:
    def __init__(self, bot, chat_id, speaker):
        self.bot = bot
        self.chat_id = chat_id
        self.pack = pack_map[speaker]

    async def send_problem_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["problem"],
            reply_to_message_id=reply_to
        )

    async def send_miss_you_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["miss_you"],
            reply_to_message_id=reply_to
        )

    async def send_you_rock_sticker(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["you_rock"],
            reply_to_message_id=reply_to
        )

    async def send_fabulous(self, reply_to=None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["fabulous"],
            reply_to_message_id=reply_to
        )
