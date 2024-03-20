from sqlalchemy import Column, Integer, String, Unicode, Boolean
from src.database import Base
from src.database.mixins import TimestampMixin


class MessageForUsers(Base, TimestampMixin):
    __tablename__ = "message_for_users"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=True)
    path_to_data = Column(String, nullable=True)

