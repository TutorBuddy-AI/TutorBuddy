from src.database.models import Person
from src.database.models import User, MessageHistory, Setting
from src.database import Transactional, session
from src.utils.user.schemas import GetUserInfo, UserInfo, GetUserPersonInfo, GetUserMessageHistory
from src.utils.generator.question_history import SupportHistory
from src.utils.feedback_loop import FeedbackHistory

from src.utils.message_history_mistakes import MessageMistakesService
from sqlalchemy import select, update, delete, text
from src.utils.message_hint import MessageHintService
from src.utils.message_translation import MessageTranslationService
from src.utils.paraphrasing import MessageParaphraseService


class UserService:
    def __init__(self):
        pass

    @Transactional()
    async def create_user(
            self, user_info: UserInfo
    ) -> None:
        user = User(
            tg_id=str(user_info["tg_id"]),
            call_name=user_info["call_name"],
            phone_number=user_info["phone_number"],
            tg_firstName=user_info["tg_firstName"],
            tg_lastName=user_info["tg_lastName"],
            tg_language=user_info["tg_language"],
            tg_username=user_info["tg_username"],
            source=user_info["source"],
            goal=user_info["goal"],
            native_lang=user_info["native_lang"],
            topic=user_info["topic"],
            additional_topic=user_info["additional_topic"],
            english_level=user_info["english_level"]
        )

        # user_location = UserLocation(
        #     tg_id=str(user_info["tg_id"]),
        #     ip_adress=str(user_location_info["ipAddress"]),
        #     latitude=str(user_location_info["latitude"]),
        #     longitude=str(user_location_info["longitude"]),
        #     country_name=str(user_location_info["countryName"]),
        #     country_code=str(user_location_info["countryCode"]),
        #     time_zone=str(user_location_info["timeZone"]),
        #     zip_code=str(user_location_info["zipCode"]),
        #     city_name=str(user_location_info["cityName"]),
        #     region_name=str(user_location_info["regionName"]),
        #     continent=str(user_location_info["continent"]),
        #     continent_code=str(user_location_info["continentCode"])г,
        # )

        session.add(user)
        # session.add(user_location)

    async def get_user_message_history(
            self,
            tg_id: str,
            limit: int = 20
    ) -> GetUserMessageHistory:
        query = select(MessageHistory).where(MessageHistory.tg_id == str(tg_id)).order_by(MessageHistory.id.desc())

        query = query.limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = list(reversed([{'role': row.role, 'content': row.message} for row in result]))

        return results

    async def count_message_history(self, tg_id) -> int:
        query = text("SELECT COUNT(*) AS message_count FROM message_history WHERE tg_id = :tg_id and role = 'user';")
        result = await session.execute(query, {"tg_id": str(tg_id)})
        return result.scalar()

    async def is_exist(
            self,
            tg_id: str
    ) -> bool:
        query = select(User.tg_firstName).where(User.tg_id == str(tg_id))
        result = await session.execute(query)

        return True if result.scalars().first() else False

    async def get_user_info(
            self,
            tg_id: str
    ) -> GetUserInfo:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        result = result.scalars().first()
        return {
            "name": result.call_name,
            "goal": result.goal,
            "native_lang": result.native_lang,
            "topic": result.topic,
            "english_level": result.english_level,
            "speaker": result.speaker
        }

    async def get_user_person(
            self,
            tg_id: str
    ) -> GetUserPersonInfo:
        query = (
            select(
                User,
                Person
            )
            .join(Person, User.speaker == Person.id)
            .where(User.tg_id == tg_id)
        )
        result = await session.execute(query)
        result = result.first()

        return {
            "name": result.User.call_name,
            "goal": result.User.goal,
            "native_lang": result.User.native_lang,
            "topic": result.User.topic,
            "english_level": result.User.english_level,
            "speaker_id": result.Person.id,
            "speaker_short_name": result.Person.short_name,
            "speaker_full_name": result.Person.full_name
        }

    @Transactional()
    async def change_callname(self, tg_id: str, new_callname: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(call_name=new_callname)
        await session.execute(query)

    @Transactional()
    async def change_topic(self, tg_id: str, new_topic: str, new_additional_topic: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(topic=new_topic, additional_topic=new_additional_topic)
        await session.execute(query)

    @Transactional()
    async def change_native_language(self, tg_id: str, new_native_language: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(native_lang=new_native_language)
        await session.execute(query)

    @Transactional()
    async def change_english_level(self, tg_id: str, new_english_level: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(english_level=new_english_level)
        await session.execute(query)

    @Transactional()
    async def change_goal(self, tg_id: str, new_goal: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(goal=new_goal)
        await session.execute(query)

    @Transactional()
    async def change_speaker(self, tg_id: str, new_speaker: str) -> None:
        query = update(User).where(User.tg_id == tg_id).values(speaker=new_speaker)
        await session.execute(query)

    @Transactional()
    async def delete_user_info(self, tg_id: str) -> None:
        await MessageMistakesService().delete_user_message_mistakes(tg_id)
        await MessageHintService().delete_user_message_hints(tg_id)
        await MessageTranslationService().delete_user_message_translations(tg_id)
        await MessageParaphraseService().delete_user_message_paraphrases(tg_id)
        await SupportHistory().delete_user_questions_history(tg_id)
        await FeedbackHistory().delete_user_feedbacks_history(tg_id)
        await session.execute(delete(MessageHistory).where(MessageHistory.tg_id == tg_id))
        await session.execute(delete(Setting).where(Setting.tg_id == tg_id))
        await session.execute(delete(User).where(User.tg_id == tg_id))
