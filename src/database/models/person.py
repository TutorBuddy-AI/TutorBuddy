from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Unicode


class Person(Base):
    __tablename__ = "person"

    id = Column(String, primary_key=True)
    short_name = Column(String, nullable=False)

    full_name = Column(String, nullable=False)
