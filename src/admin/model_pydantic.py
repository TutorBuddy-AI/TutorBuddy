from pydantic import BaseModel

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


