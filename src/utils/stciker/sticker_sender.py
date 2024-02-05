from utils.stciker.sticker_pack import anastasias_pack, tutorbots_pack


class StickerSender:
    def __init__(self, bot, chat_id, speaker):
        self.bot = bot
        self.chat_id = chat_id
        self.pack = anastasias_pack if speaker == "Anastasia" else tutorbots_pack

    async def send_problem_sticker(self, reply_to = None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["problem"],
            reply_to_message_id=reply_to
        )

    async def send_miss_you_sticker(self, reply_to = None):
        await self.bot.send_sticker(
            self.chat_id,
            self.pack["miss_you"],
            reply_to_message_id=reply_to
        )