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
    dispatch_summary = Column(Boolean, default=True)
