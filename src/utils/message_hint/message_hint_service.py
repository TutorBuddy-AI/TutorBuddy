from src.database import Transactional
from src.database.models import MessageHint
from sqlalchemy import delete
from src.database import session
from src.utils.message.schema import MessageHelperInfo


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

    @Transactional()
    async def delete_user_message_hints(self, tg_id: str) -> None:
        await session.execute(delete(MessageHint).where(MessageHint.tg_id == tg_id))
