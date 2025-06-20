from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    Table,
    Unicode,
    DateTime
)


class Setting(Base, TimestampMixin):
    __tablename__ = "setting"
    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))
    summary_on = Column(Boolean, default=True)
    summary_answered = Column(Boolean, default=False)
    subscription_good_morning= Column(Boolean, default=True)
    subscription_daily_plans = Column(Boolean, default=True)
    subscription_good_evening = Column(Boolean, default=True)
    subscription_sent_counter = Column(Integer, nullable=True)
    subscription_sent_at = Column(DateTime(timezone=True), nullable=True)
