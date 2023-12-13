from typing import List
from pydantic import BaseModel


class HistoryQuestions(BaseModel):
    tg_id: str | None
    message: str | None


class GetUserQuestionsHistory(BaseModel):
    user_questions_history: List[HistoryQuestions] | None
