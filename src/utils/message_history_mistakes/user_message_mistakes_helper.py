from src.utils.message.schema.message import MessageStateInfo
from src.utils.message_history_mistakes.schemas import MessageMistakesInfo
from aiogram.types import Message


class MessageMistakesHelper:
    def __init__(self):
        ...

    async def group_message_mistakes_info(
            self, bot_message_id: int, user_message_id: int, type_message: str, message: Message, mistakes: str) -> MessageMistakesInfo:
        user_mistakes_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": user_message_id,
            "bot_message_id": bot_message_id,

            "message": mistakes,
            "role": "assistant",
            "type": type_message
        }
        return user_mistakes_info
