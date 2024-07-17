from sqlalchemy import Column, Integer, String, Unicode, Boolean, Date
from src.database import Base
from src.database.mixins import TimestampMixin


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    tg_id = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)