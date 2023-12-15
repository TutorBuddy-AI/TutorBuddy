import asyncio
from src.database.models import DailyNews
from src.database import session, Transactional
from src.database.models.enums.daily_news import DailyNewsEnum
from sqlalchemy import select, delete

from utils.daily_news.daily_news_history import GetUserDailyNewsHistory


class DailyNew:
    def __init__(self):
        ...

    @Transactional()
    async def add_news(self, topic: str, message: str, new_types: DailyNewsEnum.NEWS_TYPE__TEXT,
                       path_to_data: str) -> None:
        daily_news = DailyNews(
            topic=topic,
            message=message,
            type=new_types.name,
            path_to_data=path_to_data
        )
        session.add(daily_news)

    @Transactional()
    async def get_daily_news(
            self,
            topic: str,
            limit: int = 25
    ) -> GetUserDailyNewsHistory:
        query = select(DailyNews).where(DailyNews.topic == str(topic)).limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'topic': row.topic, 'content': row.message, 'type': row.type, 'path to data': row.path_to_data} for row in result]
        return results

    @Transactional()
    async def delete_user_questions_history(self, topic: str) -> None:
        delete_query = delete(DailyNews).where(DailyNews.topic == topic)
        await session.execute(delete_query)

