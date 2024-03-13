from pydantic import BaseModel

class NewsletterData(BaseModel):
    topic: str
    url: str
    message: str
    image: bytes

class ChangePassword(BaseModel):
    username: str
    new_password: str
    confirm_password: str


