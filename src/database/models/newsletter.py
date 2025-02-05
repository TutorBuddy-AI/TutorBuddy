from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime
from src.database import Base
from src.database.mixins import TimestampMixin


class Newsletter(Base, TimestampMixin):
    __tablename__ = "newsletter"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    url = Column(String, nullable=True)
    path_to_data = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    publication_date = Column(String, nullable=True)
    title = Column(String, nullable=False)
    shown_at = Column(DateTime(timezone=True), nullable=True)