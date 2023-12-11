from typing import List
from pydantic import BaseModel

class _History(BaseModel):
    role: str | None
    message: str | None

class GetUserMessageHistory(BaseModel):
    user_message_history: List[_History] | None

class GetNewUserMessageHistory(BaseModel):
    user_message_history: List[_History] | None

class GetUserFeedbacksHistory(BaseModel):
    feedbacks_history: List[_History] | None

class GetUserQuestionsHistory(BaseModel):
    questions_history: List[_History] | None