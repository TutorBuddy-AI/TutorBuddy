from sqlalchemy import Column, Integer, String, Unicode
from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy_file import FileField, ImageField
from sqlalchemy_file.validators import ContentTypeValidator, SizeValidator
from src.database.models.enums.daily_news import DailyNewsEnum
from pathlib import Path


class DailyNews(Base, TimestampMixin):
    __tablename__ = "daily_news"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    type = Column(Unicode, nullable=False, default=DailyNewsEnum)
    path_to_data = Column(String, nullable=True)

    image = Column(
        ImageField(
            multiple=True,
            upload_storage="images",
            validators=[SizeValidator("100k")],
        )
    )

    file = Column(
        FileField(
            multiple=True,
            upload_storage="other_files",
            validators=[SizeValidator("100k")],
        )
    )