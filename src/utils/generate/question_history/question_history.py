import asyncio
from src.database.models import QuestionsHistory
from sqlalchemy import select, delete
from src.database import session, Transactional
from utils.user.schemas.user_message_history import GetUserQuestionsHistory


class QuestionsHistory:
    def __init__(self):
        ...

    @Transactional()
    async def add_questions(self, tg_id, message, role, type, created_at, updated_at):
        questions_history = QuestionsHistory(
            tg_id=tg_id,
            message=message,
            role=role,
            type=type,
            created_at=created_at,
            updated_at=updated_at
        )
        session.add(questions_history)

    @Transactional()
    async def get_questions_history(
            self,
            tg_id: str,
            limit: int = 20
    ) -> GetUserQuestionsHistory:
        query = select(QuestionsHistory).where(QuestionsHistory.tg_id == str(tg_id)).limit(limit)
        result = await session.execute(query)
        result = result.scalars()

        results = [{'tg_id': row.tg_id, 'content': row.message} for row in result]

        if not results:
            for i in range(2):
                results.append({'tg_id': 0, 'content': 'No questions found'})

        return results

    @Transactional()
    async def delete_user_history(self, tg_id: str) -> None:
        delete_query = delete(QuestionsHistory).where(QuestionsHistory.tg_id == str(tg_id))
        await session.execute(delete_query)
        await session.commit()
