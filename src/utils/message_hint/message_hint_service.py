from database import Transactional
from database.models import MessageHint
from src.database import session
from utils.message_hint.schema.message_hint_info import MessageHintInfo


class MessageHintService:
    @Transactional()
    async def create_message_hint(
            self,
            new_message_hint: MessageHintInfo
    ) -> None:
        mistakes = MessageHint(
            tg_id=new_message_hint["tg_id"],
            user_message_id=new_message_hint["user_message_id"],
            bot_message_id=new_message_hint["bot_message_id"],
            message=new_message_hint["message"],
            role=new_message_hint["role"],
            type=new_message_hint["type"],
        )

        session.add(mistakes)
