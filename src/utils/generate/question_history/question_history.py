from src.database.models import QuestionsHistory
from sqlalchemy import select, delete
from src.database import session, Transactional
from src.utils.generate.question_history.user_questions_history import GetUserQuestionsHistory


class SupportHistory:
    def __init__(self):
        ...

    @Transactional()
    async def add_questions(self, tg_id: str, message: str) -> None:
        questions_history = QuestionsHistory(
            tg_id=tg_id,
            message=message
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

        return results

    @Transactional()
    async def delete_user_questions_history(self, tg_id: str) -> None:
        delete_query = delete(QuestionsHistory).where(QuestionsHistory.tg_id == str(tg_id))
        await session.execute(delete_query)

