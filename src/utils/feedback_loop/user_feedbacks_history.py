from typing import List
from pydantic import BaseModel


class HistoryFeedbacks(BaseModel):
    tg_id: str | None
    message: str | None


class GetUserFeedbacksHistory(BaseModel):
    user_feedbacks_history: List[HistoryFeedbacks] | None
