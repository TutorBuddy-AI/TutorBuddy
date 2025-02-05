import os
from datetime import date, datetime
from typing import List, Optional, Tuple

from src.database.models import Newsletter, User
from src.database.models import NewsletterAudio
from src.database import session
from sqlalchemy import select, delete, update, desc, func
#from sqlalchemy.sql import func

from src.utils.newsletter.schema.newsletter import NewsletterGaleryPreview, UserNewsSummary


class NewsletterService:
    @staticmethod
    async def get_newsletter(newsletter_id: int):
        query = select(Newsletter).where(Newsletter.id == newsletter_id)
        result = await session.execute(query)
        newsletter = result.scalars().first()
        return newsletter

    @staticmethod
    async def get_user_newsletters_previews(tg_id: str) -> List[NewsletterGaleryPreview]:
        query = (
            select(Newsletter, User.tg_id).join(User, func.position(Newsletter.topic.in_(func.lower(User.topic))) != 0)
            .where(User.tg_id == tg_id)
            .where(User.tg_id.is_not(None))
            .distinct(Newsletter.id)
            .order_by(Newsletter.id)
        )
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

    @staticmethod
    async def get_fresh_user_topics_for_all_in_date(target_date: date) -> List[UserNewsSummary]:
        """
        Function to collect all users who have fresh news in their
        """
        query = (
            select(
                User.tg_id,
                func.array_agg(Newsletter.topic).over(partition_by=User.tg_id).label("topics"),
                func.count(Newsletter.id).over(partition_by=User.tg_id).label("num_newsletters"),
            )
            .join(Newsletter, onclause=func.position(Newsletter.topic.op('IN')(func.lower(User.topic))) != 0)
            .distinct(User.tg_id)
#            .filter(func.date(Newsletter.updated_at) >= target_date)
            .filter(func.date(Newsletter.shown_at) >= target_date)
        )
        result = await session.execute(query)

        user_topics = [
            UserNewsSummary(tg_id=row.tg_id, topics=row.topics, num_newsletters=row.num_newsletters)
            for row in result.all()]

        return user_topics

    @staticmethod
    async def get_fresh_user_topics_and_preview(target_date: date) -> List[Tuple[UserNewsSummary, NewsletterGaleryPreview]]:
        """
        Function to collect all users who have fresh news in their
        """
        query = (
            select(
                User.tg_id,
                func.array_agg(Newsletter.topic).over(partition_by=User.tg_id).label("topics"),
                func.count(Newsletter.id).over(partition_by=User.tg_id).label("num_newsletters"),
                func.first_value(Newsletter.id).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("id"),
                func.first_value(Newsletter.topic).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("topic"),
                func.first_value(Newsletter.title).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("title"),
                func.first_value(Newsletter.publisher).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("publisher"),
                func.first_value(Newsletter.publication_date).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("publication_date"),
                func.first_value(Newsletter.message).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("message"),
                func.first_value(Newsletter.path_to_data).over(
                    partition_by=User.tg_id,
                    order_by=desc(Newsletter.id)).label("path_to_data")
            )
            .join(Newsletter, onclause=func.position(Newsletter.topic.op('IN')(func.lower(User.topic))) != 0)
            .distinct(User.tg_id)
#            .filter(func.date(Newsletter.updated_at) >= target_date)
            .filter(func.date(Newsletter.shown_at) >= target_date)
        )
        result = await session.execute(query)

        user_topics = [
            (
                UserNewsSummary(tg_id=row.tg_id, topics=row.topics, num_newsletters=row.num_newsletters),
                NewsletterGaleryPreview(
                    id=row.id,
                    topic=row.topic,
                    title=row.title,
                    publisher=row.publisher,
                    publication_date=row.publication_date,
                    short_content=NewsletterService.cut_content(row.message),
                    img=row.path_to_data)
            )
            for row in result.all()]
        return user_topics

    @staticmethod
    def cut_content(content):
        len_short_content = len(content) if len(content) < 201 else 200
        return content[:len_short_content]

    @staticmethod
    async def get_fresh_user_topics_for_one_in_date(tg_id: str, target_date: date) -> Optional[UserNewsSummary]:
        """
        Function to collect all users who have fresh news in their
        """
        query = (
            select(
                User.tg_id,
                func.array_agg(Newsletter.topic).over(partition_by=User.tg_id).label("topics"),
                func.count(Newsletter.id).over(partition_by=User.tg_id).label("num_newsletters")
            )
            .join(Newsletter, onclause=func.position(Newsletter.topic.op('IN')(func.lower(User.topic))) != 0)
            .distinct(User.tg_id)
#            .filter(func.date(Newsletter.updated_at) >= target_date)
            .filter(func.date(Newsletter.shown_at) >= target_date)
            .filter(User.tg_id == tg_id)
        )
        result = await session.execute(query)
        user_summary = result.first()

        if user_summary is None:
            return None

        return UserNewsSummary(
            tg_id=user_summary.tg_id, topics=user_summary.topics, num_newsletters=user_summary.num_newsletters)

    @staticmethod
    async def get_newsletter_audio_files(newsletter_id: int) -> dict[str, str]:
        """
        Function to collect all users who have fresh news in their
        """
        query = (
            select(
                NewsletterAudio.speaker_id,
                NewsletterAudio.file_path
            )
            .filter(NewsletterAudio.newsletter_id == newsletter_id)
        )
        result = await session.execute(query)
        newsletter_audio_files = result.all()

        return {row.speaker_id: row.file_path for row in newsletter_audio_files}

    @staticmethod
    async def get_topics_newsletter_preview_on_date(
            topics: List[str], target_date: date, newsletter_num: int) -> Optional[NewsletterGaleryPreview]:
        """
        Function to collect all users who have fresh news in their
        """
        query = (
            select(
                Newsletter.id,
                Newsletter.topic,
                Newsletter.title,
                Newsletter.message,
                Newsletter.publisher,
                Newsletter.publication_date,
                Newsletter.path_to_data
            )
#            .filter(func.date(Newsletter.updated_at) >= target_date)
            .filter(func.date(Newsletter.shown_at) >= target_date)
            .filter(Newsletter.topic.in_(topics))
            .order_by(desc(Newsletter.id))
#            .order_by(desc(Newsletter.created_at))
        )
        result = await session.execute(query)
        all_news = result.all()
        if newsletter_num >= len(all_news):
            return None
        newsletter_preview = all_news[newsletter_num]
        return NewsletterGaleryPreview(
            id=newsletter_preview.id,
            topic=newsletter_preview.topic,
            title=newsletter_preview.title,
            publisher=newsletter_preview.publisher,
            publication_date=newsletter_preview.publication_date,
            short_content=NewsletterService.cut_content(newsletter_preview.message),
            img=newsletter_preview.path_to_data
        )

    @staticmethod
    async def delete_newsletter(newsletter_id: int):
        await NewsletterService.delete_newsletter_audio(newsletter_id)

        query = select(Newsletter).where(Newsletter.id == newsletter_id)
        result = await session.execute(query)
        newsletter = result.scalars().first()

        if os.path.exists(newsletter.path_to_data):
            os.remove(newsletter.path_to_data)

        delete_query = delete(Newsletter).where(Newsletter.id == newsletter_id)
        await session.execute(delete_query)
        await session.commit()

    @staticmethod
    async def renew_newsletter(newsletter_id: int):
        await NewsletterService.delete_newsletter_audio(newsletter_id)

        query = update(Newsletter).where(Newsletter.id == newsletter_id).values(updated_at=datetime.now())

        await session.execute(query)
        await session.commit()

    @staticmethod
    async def delete_newsletter_audio(newsletter_id: int):
        query = select(NewsletterAudio).where(NewsletterAudio.newsletter_id == newsletter_id)
        result = await session.execute(query)
        newsletter_audio = result.scalars().all()

        for audio in newsletter_audio:
            if os.path.exists(audio.file_path):
                os.remove(audio.file_path)

        delete_query = delete(NewsletterAudio).where(NewsletterAudio.newsletter_id == newsletter_id)
        await session.execute(delete_query)
        await session.commit()
