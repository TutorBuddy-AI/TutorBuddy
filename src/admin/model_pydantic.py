from pydantic import BaseModel
from typing import List

class NewsletterData(BaseModel):
    topic: str
    url: str
    message: str
    image: bytes
    publisher: str = ''
    publication_date: str = ''
    title: str

class MessageData(BaseModel):
    message: str
    image: bytes


class SendNewsletterDatetime(BaseModel):
    newsletter_id: int
    datetime_iso: str

class ChangeNewsletter(BaseModel):
    newsletter_id: int
    column: str
    changed_text: str

class SummaryFromParsing(BaseModel):
    message: str
    topic: str
    url: str
    publisher: str
    publication_date: str
    path_to_data: str
    title: str

class MessageToSelected(BaseModel):
    tg_ids: List[str]
    message: str

class MessageToAll(BaseModel):
    message: str

class MessageToAOne(BaseModel):
    tg_id: str
    message: str

class MessageDayToAOne(BaseModel):
    tg_id: str
    msg_type: str
    message: str

class UserForMessage(BaseModel):
    tg_id: str
    tg_firstName: str
