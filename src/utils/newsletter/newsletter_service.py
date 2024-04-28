from typing import List

from database.models import DailyNews
from src.database import session
from sqlalchemy import select, desc, text, delete

from utils.newsletter.schema.newsletter import NewsletterGaleryPreview


class NewsletterService:
    @staticmethod
    async def get_newsletter(newsletter_id: int):
        query = select(DailyNews).where(DailyNews.id == newsletter_id)
        result = await session.execute(query)
        newsletter = result.scalars().first()
        return newsletter

    @staticmethod
    async def get_user_newsletters_previews(
            tg_id: str,
            limit: int = 10) -> List[NewsletterGaleryPreview]:
        query = select(DailyNews)
        query = query.limit(limit)
        result = await session.execute(query)

        result = result.scalars()
        results = [
            NewsletterGaleryPreview(
                id=row.id,
                topic=row.topic,
                title=row.title,
                short_content=row.message[:len(row.message) if len(row.message) < 101 else 100],
                img=row.path_to_data
            ) for row in result]

        return results
