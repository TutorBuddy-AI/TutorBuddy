from typing import List
from pydantic import BaseModel


class _History(BaseModel):
    message: str | None


class GetUserMessageHistoryMistakes(BaseModel):
    user_message_history_mistakes: List[_History] | None
