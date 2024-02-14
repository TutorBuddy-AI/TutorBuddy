from sqlalchemy import select

from src.database import session
from src.database.models import MessageHistory


class MessageService:
    def __init__(self):
        pass

    async def get_message(self, tg_id: str, message_id: int) -> MessageHistory:
        query = select(MessageHistory).where((MessageHistory.tg_id == str(tg_id)) & (MessageHistory.id == message_id))

        result = await session.execute(query)

        result = result.scalars().first()

        return result
