from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey


class MessageMistakes(Base, TimestampMixin):
    __tablename__ = "message_mistakes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))

    user_message_id = Column(Integer, ForeignKey("message_history.id"))
    bot_message_id = Column(Integer, ForeignKey("message_history.id"))

    message = Column(String, nullable=False)
    role = Column(String, nullable=False)
    type = Column(String, nullable=False)
