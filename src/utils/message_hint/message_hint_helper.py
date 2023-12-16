from utils.message_hint.schema.message_hint_info import MessageHintInfo
from utils.message_history_mistakes.schemas import MessageStateInfo
from aiogram.types import Message


class MessageHintHelper:
    def __init__(self):
        ...

    async def group_message_hint_info(self, state_message_info: MessageStateInfo, message: Message, hint: str) -> MessageHintInfo:
        hint_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": None,  # ToDo change when state is available state_message_info.user_message.id,
            "bot_message_id": None,  # ToDo change when state is available state_message_info.bot_message.id,

            "message": hint,
            "role": "assistant",
            "type": "",  # ToDo change when state is available state_message_info.user_message.id,
        }
        return hint_info
