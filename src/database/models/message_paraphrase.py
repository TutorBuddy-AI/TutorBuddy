from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey


class MessageParaphrase(Base, TimestampMixin):
    __tablename__ = "message_paraphrase"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))

    user_message_id = Column(Integer, ForeignKey("message_history.id"), nullable=True)
    bot_message_id = Column(Integer, ForeignKey("message_history.id"), nullable=True)

    message = Column(String, nullable=False)
