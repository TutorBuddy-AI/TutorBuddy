from typing import List
from pydantic import BaseModel


class _MessageMistakes(BaseModel):
    role: str | None
    message: str | None


class GetUserMessageHistoryMistakes(BaseModel):
    user_message_history_mistakes: List[_MessageMistakes] | None


class _MessageMistakesWithContext(BaseModel):
    role: str | None
    message: str | None
    bot_message: str | None
    user_message: str | None


class GetUserMessageHistoryMistakesWithContext(BaseModel):
    user_message_history_mistakes: List[_MessageMistakesWithContext] | None