from typing import List, Optional

from pydantic import BaseModel


class NewsletterGaleryPreview(BaseModel):
    id: int
    topic: str
    title: str
    publisher: Optional[str]
    publication_date: Optional[str]
    short_content: str
    img: str


class UserNewsSummary(BaseModel):
    tg_id: str
    topics: List[str]
    num_newsletters: int
