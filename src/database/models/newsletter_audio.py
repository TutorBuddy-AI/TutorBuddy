from sqlalchemy import Column, Integer, String, Unicode, Boolean, ForeignKey
from src.database import Base
from src.database.mixins import TimestampMixin


class NewsletterAudio(Base, TimestampMixin):
    __tablename__ = "newsletter_audio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    newsletter_id = Column(Integer, ForeignKey("newsletter.id"), nullable=False)
    speaker_id = Column(String, ForeignKey("person.id"), nullable=False)
    file_path = Column(String, nullable=False)
