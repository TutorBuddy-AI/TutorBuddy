from database import Transactional
from database.models import MessageParaphrase
from sqlalchemy import delete
from src.database import session
from utils.message.schema import MessageHelperInfo


class MessageParaphraseService:
    @Transactional()
    async def create_message_paraphrase(
            self,
            new_message_hint: MessageHelperInfo
    ) -> None:
        mistakes = MessageParaphrase(
            tg_id=new_message_hint["tg_id"],
            user_message_id=new_message_hint["user_message_id"],
            bot_message_id=new_message_hint["bot_message_id"],
            message=new_message_hint["message"]
        )

        session.add(mistakes)

    @Transactional()
    async def delete_user_message_paraphrases(self, tg_id: str) -> None:
        await session.execute(delete(MessageParaphrase).where(MessageParaphrase.tg_id == tg_id))