from utils.message.schema import MessageHelperInfo, ConversationStateInfo
from aiogram.types import Message


class MessageHelper:
    def __init__(self):
        ...

    async def group_message_helper_info(
            self, state_message_info: ConversationStateInfo, message: Message, hint: str) -> MessageHelperInfo:
        helper_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": state_message_info.user_message_id,
            "bot_message_id": state_message_info.bot_message_id,

            "message": hint,
        }
        return helper_info
