from database import Transactional
from src.database import session
from utils.message.schema import MessageHelperInfo


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
            role=user_translation_info["role"],
            type=user_translation_info["type"],
        )

        session.add(mistakes)
