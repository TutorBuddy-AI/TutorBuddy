from typing import List

from sqlalchemy import select

from src.config.initialize import bot
from src.database import session
from src.database.models import DailyNews, User


class Newsletter:
    def __init__(self):
        ...

    async def send_newsletter(self) -> None:
        query_news = select(DailyNews)
        result_news = await session.execute(query_news)
        all_news = result_news.scalars().all()

        for daily_news in all_news:
            tg_ids = await self.user_topic(daily_news.topic)
            print(tg_ids)

            string = daily_news.message.replace("<p>", "").replace("</p>", "")

            for tg_id in tg_ids:
                try:
                    await bot.send_message(tg_id, string)
                except:
                    pass
    async def user_topic(self, topic) -> List[int]:
        print(f"Searching for topic: {topic}")

        query = select(User).where(User.topic == topic)
        result = await session.execute(query)
        users_for_news = result.scalars().all()

        tg_ids = [user_for_news.tg_id for user_for_news in users_for_news]

        if tg_ids:
            print(f"Found users for topic {topic}: {tg_ids}")
            return tg_ids
        else:
            print(f"No users found for topic: {topic}")
            return []
