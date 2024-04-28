from pydantic import BaseModel


class NewsletterGaleryPreview(BaseModel):
    id: int
    topic: str
    title: str
    short_content: str
    img: str
