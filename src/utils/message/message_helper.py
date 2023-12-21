from typing import List

from aiogram.dispatcher import FSMContext
from database.models import MessageHistory
from utils.message.schema import MessageHelperInfo, ConversationStateInfo
from aiogram.types import Message


class MessageHelper:
    def __init__(self):
        ...

    async def group_message_helper_info(
            self, state_message_info: ConversationStateInfo, message: Message, hint: str) -> MessageHelperInfo:
        helper_info = {
            "tg_id": str(message.chat.id),
            "user_message_id": state_message_info["user_message_id"],
            "bot_message_id": state_message_info["bot_message_id"],
            "message": hint,
        }
        return helper_info

    async def group_conversation_info_to_state(self, state: FSMContext,  messages: List[MessageHistory]) -> None:
        await state.update_data(type_message=messages[0].type)
        await state.update_data(user_message_id=messages[0].id)
        await state.update_data(user_message_text=messages[0].message)
        await state.update_data(bot_message_id=messages[1].id)
        await state.update_data(bot_message_text=messages[1].message)
