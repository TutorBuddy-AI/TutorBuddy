from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Unicode


class MessageHistory(Base, TimestampMixin):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))

    message = Column(String, nullable=False)
    role = Column(String, nullable=False)
    type = Column(String, nullable=False)



