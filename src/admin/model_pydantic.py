from pydantic import BaseModel

class NewsletterData(BaseModel):
    topic: str
    url: str
    message: str
    image: bytes
    edition: str = ''
    publication_date: str = ''
    title: str

class ChangePassword(BaseModel):
    username: str
    new_password: str
    confirm_password: str


