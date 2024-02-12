from src.database import Transactional
from src.database.models import MessageHistory, MessageMistakes
from sqlalchemy import select, delete
from sqlalchemy.orm import aliased
from src.database import session
from src.utils.message_history_mistakes.schemas import GetUserMessageHistoryMistakes, MessageMistakesInfo,\
    GetUserMessageHistoryMistakesWithContext


class MessageMistakesService:
    def __init__(self):
        ...

    @Transactional()
    async def create_mistakes(
            self, user_mistakes_info: MessageMistakesInfo
    ) -> None:
        mistakes = MessageMistakes(
            tg_id=user_mistakes_info["tg_id"],
            user_message_id=user_mistakes_info["user_message_id"],
            bot_message_id=user_mistakes_info["bot_message_id"],
            message=user_mistakes_info["message"],
            role=user_mistakes_info["role"],
            type=user_mistakes_info["type"],
        )

        session.add(mistakes)

    async def get_user_message_history_mistakes(
            self,
            tg_id: str,
            limit: int = 50
    ) -> GetUserMessageHistoryMistakes:
        query = select(MessageMistakes).where(MessageMistakes.tg_id == str(tg_id))

        query = query.limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'message': row.message} for row in result]

        return results

    async def get_user_message_history_mistakes_with_context(
            self,
            tg_id: str,
            limit: int = 50
    ) -> GetUserMessageHistoryMistakesWithContext:
        bot_messages = aliased(MessageHistory)
        user_messages = aliased(MessageHistory)
        query = (
            select(
                MessageMistakes.role,
                MessageMistakes.message,
                bot_messages.message.label('bot_message'),
                user_messages.message.label('user_message')
            )
            .join(bot_messages, MessageMistakes.bot_message_id == bot_messages.id)
            .join(user_messages, MessageMistakes.user_message_id == user_messages.id)
            .where(MessageMistakes.tg_id == tg_id)
        )

        query = query.limit(limit)
        result = await session.execute(query)

        query_result = result
        results = [{
            'role': row.role,
            'message': row.message,
            'bot_message': row.bot_message,
            'user_message': row.user_message} for row in query_result]

        return results

    @Transactional()
    async def delete_user_message_mistakes(self, tg_id: str) -> None:
        await session.execute(delete(MessageMistakes).where(MessageMistakes.tg_id == tg_id))

    @Transactional()
    async def delete_message_mistakes(self, mistake_id: int) -> None:
        await session.execute(delete(MessageMistakes).where(MessageMistakes.id == mistake_id))
