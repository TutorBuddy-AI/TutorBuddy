import asyncio
from src.database.models import FeedbacksHistory
from sqlalchemy import select, delete
from src.database import session, Transactional

class FeedbackHistory:
    def __init__(self):
        ...

    @Transactional()
    async def add_feedback(self, tg_id: str, message: str) -> None:
        feedback_history = FeedbacksHistory(
            tg_id=tg_id,
            message=message
        )
        session.add(feedback_history)

    @Transactional()
    async def get_feedbacks_history(
            self,
            tg_id: str,
            limit: int = 20
    ) -> list[dict[str, str]]:
        query = select(FeedbacksHistory).where(FeedbacksHistory.tg_id == str(tg_id)).limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'tg_id': row.tg_id, 'content': row.message} for row in result]

        return results

    @Transactional()
    async def delete_user_feedbacks_history(self, tg_id: str) -> None:
        delete_query = delete(FeedbacksHistory).where(FeedbacksHistory.tg_id == str(tg_id))
        await session.execute(delete_query)

