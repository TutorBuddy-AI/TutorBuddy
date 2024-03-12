from pydantic import BaseModel

class NewsletterData(BaseModel):
    topic: str
    url: str
    message: str
    image: bytes

