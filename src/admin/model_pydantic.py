from pydantic import BaseModel

class NewsletterData(BaseModel):
    topic: str
    url: str
    message: str
    image: bytes
    edition: str = ''
    publication_date: str = ''
    title: str


class ChangeNewsletter(BaseModel):
    newsletter_id: int
    column: str
    changed_text: str


