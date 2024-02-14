from typing import List

from aiogram.dispatcher import FSMContext
from src.database.models import MessageHistory
from src.utils.message.schema import MessageHelperInfo, ConversationStateInfo
from aiogram.types import Message


class MessageHelper:
    def __init__(self):
        ...

    async def group_message_helper_info(
            self, bot_message_id: int, user_message_id: int, message: Message, hint: str) -> MessageHelperInfo:
        helper_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": user_message_id,
            "bot_message_id": bot_message_id,
            "message": hint,
        }
        return helper_info

    async def group_conversation_info_to_state(self, state: FSMContext,  messages: List[MessageHistory]) -> None:
        state_data = await state.get_data()
        state_data["type_message"] = messages[0].type
        state_data["user_message_id"] = messages[0].id
        state_data["user_message_text"] = messages[0].message
        state_data["bot_message_id"] = messages[1].id
        state_data["bot_message_text"] = messages[1].message
        await state.update_data(state_data)
