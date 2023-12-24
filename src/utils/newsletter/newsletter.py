import asyncio
from src.database.models import DailyNews,User
from src.database import session, Transactional
from src.database.models.enums.daily_news import DailyNewsEnum
from sqlalchemy import select, delete
from utils.daily_news.daily_news_history import GetUserDailyNewsHistory
from src.config.initialize import bot




class Newsletter:
    def __init__(self):
        ...

    async def send_newsletter(self) -> None:
        query = select(DailyNews)
        result_news = await session.execute(query)
        all_news = result_news.scalars().all()

        for daily_news in all_news:
            query = select(User).where(User.topic == daily_news.topic)
            result = await session.execute(query)
            user_topic_all = result.scalars().all()

            if user_topic_all:
                for user in user_topic_all:
                    try:
                        await bot.send_message(user.tg_id, daily_news.message)
                    except Exception as e:
                        pass
