from src.database.models import DailyNews, User
from src.database import session, Transactional
from src.database.models.enums.daily_news import DailyNewsEnum
from sqlalchemy import select, delete, func
from src.config.initialize import bot


class Newsletter:
    def __init__(self):
        ...

    async def send_newsletter(self) -> None:
        query_news = select(DailyNews)
        result_news = await session.execute(query_news)
        all_news = result_news.scalars().all()

        for daily_news in all_news:

            tg_id_list = await self.user_topic(daily_news.topic)
            print(tg_id_list)
            string = daily_news.message.replace("<p>", "").replace("</p>", "")
            for tgid in tg_id_list:
                try:
                    await bot.send_message(int(tgid), string)
                except Exception as e:
                    pass

    async def user_topic(self, topic) -> list:
        query = select(User)
        result = await session.execute(query)
        user_for_news = result.scalars().unique().all()
        matching_tg_ids = []

        for user_topic in user_for_news:

            topics_list = str(user_topic.topic).split()

            if topic.lower().strip() in map(str.lower, topics_list):
                matching_tg_ids.append(user_topic.tg_id)

        return matching_tg_ids
