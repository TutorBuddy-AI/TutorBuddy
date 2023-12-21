from utils.message.schema.message import MessageStateInfo
from utils.message_history_mistakes.schemas import MessageMistakesInfo
from aiogram.types import Message


class MessageMistakesHelper:
    def __init__(self):
        ...

    async def group_message_mistakes_info(
            self, state_message_info: MessageStateInfo, message: Message, mistakes: str) -> MessageMistakesInfo:
        user_mistakes_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": None,  # ToDo state_message_info.user_message.id,
            "bot_message_id": None,  # ToDo state_message_info.bot_message.id,

            "message": mistakes,
            "role": "assistant",
            "type": ""  # ToDo state_message_info.type_message
        }
        return user_mistakes_info
