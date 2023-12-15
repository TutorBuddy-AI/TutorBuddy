from typing import List
from pydantic import BaseModel


class HistoryDailyNews(BaseModel):
    topic: str | None
    message: str | None


class GetUserDailyNewsHistory(BaseModel):
    user_questions_history: List[HistoryDailyNews] | None
