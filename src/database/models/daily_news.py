from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Unicode, Text
from src.database.models.enums.daily_news import DailyNewsEnum


#  many-to-many relationship with users
# to check if user already get the message
# user, daily_news.id, is_sended (is_read)...
class DailyNews(Base, TimestampMixin):
    __tablename__ = "daily_news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=True)
    type = Column(Unicode, nullable=False, default=DailyNewsEnum.NEWS_TYPE__TEXT)
    topic = Column(String, nullable=True)
    path_to_data = Column(String, nullable=True)

    # we can use sqlalchemy-file to work with files in admin panel
    # from sqlalchemy_file import FileField, ImageField
    # file = Column(ImageField(upload_storage='daily-news'))
