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


class User_acces(Base, TimestampMixin):
    __tablename__ = "user_acces"
    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, unique=True)
    dispatch_summary = Column(Boolean, default=True)
