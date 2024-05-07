from typing import List

from pydantic import BaseModel


class NewsletterGaleryPreview(BaseModel):
    id: int
    topic: str
    title: str
    short_content: str
    img: str


class UserNewsSummary(BaseModel):
    tg_id: str
    topics: List[str]
    num_newsletters: int
