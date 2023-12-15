from typing import List
from pydantic import BaseModel
from src.database.models.enums.daily_news import DailyNewsEnum

class HistoryDailyNews(BaseModel):
    topic: str | None
    message: str | None
    type: DailyNewsEnum | None
    path_to_data: str | None

class GetUserDailyNewsHistory(BaseModel):
    user_questions_history: List[HistoryDailyNews] | None
