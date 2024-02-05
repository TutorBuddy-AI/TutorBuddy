from aiogram.types import Message

from src.utils.user.schemas import UserInfo, StateUserInfo


class UserHelper:
    def __init__(self):
        ...

    async def group_user_info(self, state_user_info: StateUserInfo, message: Message) -> UserInfo:

        user_info = {
            "tg_id": message.chat.id,
            "phone_number": None,
            "tg_firstName": message.chat.first_name,
            "tg_lastName": message.chat.last_name,
            "tg_language": state_user_info["tg_language"],
            "tg_username": message.chat.username,
            "call_name": state_user_info["name"],
            "source": state_user_info["source"],
            "goal": state_user_info["goal"],
            "native_lang": state_user_info["native_language"],
            "topic": state_user_info["topic"],
            "additional_topic": state_user_info["additional_topic"],
            "english_level": state_user_info["english_level"]
        }
        return user_info
