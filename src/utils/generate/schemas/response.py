from typing import List
from pydantic import BaseModel

class _History(BaseModel):
    role: str | None
    message: str | None

class GetGeneratedTextAndUserMessageHistory(BaseModel):
    generated_text: str | None
    message: List[_History] | None
