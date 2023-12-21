from database import Transactional
from database.models import MessageHint
from src.database import session
from utils.message.schema import MessageHelperInfo


class MessageHintService:
    @Transactional()
    async def create_message_hint(
            self,
            new_message_hint: MessageHelperInfo
    ) -> None:
        hint = MessageHint(
            tg_id=new_message_hint["tg_id"],
            user_message_id=new_message_hint["user_message_id"],
            bot_message_id=new_message_hint["bot_message_id"],
            message=new_message_hint["message"]
        )

        session.add(hint)
