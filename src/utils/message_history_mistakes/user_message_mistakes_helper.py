from utils.message_history_mistakes.schemas import MessageMistakesInfo, MessageStateInfo
from aiogram.types import Message


class MessageMistakesHelper:
    def __init__(self):
        ...

    async def group_message_mistakes_info(self, state_message_info: MessageStateInfo, message: Message) -> MessageMistakesInfo:
        user_mistakes_info = {
            "tg_id": message.chat.id,
            "user_message_id": state_message_info.user_message.id,
            "bot_message_id": state_message_info.bot_message.id,

            "message": message.text,
            "role": "assistant",
            "type": state_message_info.type_message
        }
        return user_mistakes_info
