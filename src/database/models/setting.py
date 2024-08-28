from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    Table,
    Unicode
)


class Setting(Base, TimestampMixin):
    __tablename__ = "setting"
    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))
    summary_on = Column(Boolean, default=True)
    summary_answered = Column(Boolean, default=False)
    newsletter_good_morning= Column(Boolean, default=True)
    newsletter_daily_plans = Column(Boolean, default=True)
    newsletter_good_evening = Column(Boolean, default=True)
