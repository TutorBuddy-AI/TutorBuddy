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
from sqlalchemy.orm import relationship
from starlette.requests import Request
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(Base, TimestampMixin):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=True)

    def get_password_hash(self, password):
        return pwd_context.hash(password)
