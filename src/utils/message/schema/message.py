from pydantic import BaseModel


class MessageStateInfo(BaseModel):
    user_message_id: int | None
    bot_message_id: int | None
    type_message: str | None


class ConversationStateInfo(BaseModel):
    user_message_id: int | None
    bot_message_id: int | None
    type_message: str | None
    user_message_text: int | None
    bot_message_text: int | None


class MessageHelperInfo(BaseModel):
    tg_id: str
    user_message_id: int | None
    bot_message_id: int | None
    message: str | None
