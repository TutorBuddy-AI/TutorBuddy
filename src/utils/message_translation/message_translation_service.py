from src.database import Transactional
from src.database.models import MessageTranslation
from sqlalchemy import delete
from src.database import session
from src.utils.message.schema import MessageHelperInfo


class MessageTranslationService:
    def __init__(self):
        ...

    @Transactional()
    async def create_translation(
            self, user_translation_info: MessageHelperInfo
    ) -> None:
        mistakes = MessageTranslation(
            tg_id=user_translation_info["tg_id"],
            user_message_id=user_translation_info["user_message_id"],
            bot_message_id=user_translation_info["bot_message_id"],
            message=user_translation_info["message"],
        )

        session.add(mistakes)

    @Transactional()
    async def delete_user_message_translations(self, tg_id: str) -> None:
        await session.execute(delete(MessageTranslation).where(MessageTranslation.tg_id == tg_id))
