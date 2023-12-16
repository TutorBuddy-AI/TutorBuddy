from pydantic import BaseModel


class MessageHintInfo(BaseModel):
    tg_id: str
    user_message_id: int | None
    bot_message_id: int | None
    message: str | None
    role: str | None
    type: str | None
