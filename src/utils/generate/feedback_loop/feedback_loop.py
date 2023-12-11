import asyncio
from src.database.models import FeedbacksHistory
from sqlalchemy import select, delete
from src.database import session, Transactional
from utils.user.schemas.user_message_history import GetUserFeedbacksHistory

class FeedbackHistory:
    def __init__(self):
        ...

    @Transactional()
    async def add_feedback(self, tg_id, message, role, type, created_at, updated_at):
        feedback_history = FeedbacksHistory(
            tg_id=tg_id,
            message=message,
            role=role,
            type=type,
            created_at=created_at,
            updated_at=updated_at
        )
        session.add(feedback_history)

    @Transactional()
    async def get_feedbacks_history(
            self,
            tg_id: str,
            limit: int = 20
    ) -> GetUserFeedbacksHistory:
        query = select(FeedbacksHistory).where(FeedbacksHistory.tg_id == str(tg_id)).limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'tg_id': row.tg_id, 'content': row.message} for row in result]

        if not results:
            for i in range(2):
                results.append({'tg_id': 0, 'content': 'No feedback found'})
        return results

    @Transactional()
    async def delete_user_feedbacks(self, tg_id: str) -> None:
        delete_query = delete(FeedbacksHistory).where(FeedbacksHistory.tg_id == str(tg_id))
        await session.execute(delete_query)
        await session.commit()

