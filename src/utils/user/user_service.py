from src.database.models import User, UserLocation, MessageHistory
from src.database import Transactional, session
from src.utils.user.schemas import GetUserInfo, UserInfo, UserLocationInfo, GetUserMessageHistory

from typing import Optional, List

from sqlalchemy import select, update, delete


class UserService:
    def __init__(self):
        ...

    @Transactional()
    async def create_user(
            self, user_info: UserInfo, user_location_info: UserLocationInfo
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
        query = select(MessageHistory).where(MessageHistory.tg_id == str(tg_id))

        query = query.limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'role': row.role, 'content': row.message} for row in result]

        if not results:
            for i in range(2):
                results.append(0)

        return results

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
        query = select(User).where(User.tg_id == str(tg_id))
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

    async def change_callname(self, tg_id, new_callname) -> None:
        query = update(User).where(User.tg_id == tg_id).values(call_name=new_callname)
        await session.execute(query)

    async def change_topic(self, tg_id, new_topic) -> None:
        query = update(User).where(User.tg_id == tg_id).values(topic=new_topic)
        await session.execute(query)

    async def change_native_language(self, tg_id, new_native_language) -> None:
        query = update(User).where(User.tg_id == tg_id).values(native_lang=new_native_language)
        await session.execute(query)

    async def change_english_level(self, tg_id, new_english_level) -> None:
        query = update(User).where(User.tg_id == tg_id).values(english_level=new_english_level)
        await session.execute(query)

    async def change_goal(self, tg_id, new_goal) -> None:
        query = update(User).where(User.tg_id == tg_id).values(goal=new_goal)
        await session.execute(query)

    async def change_speaker(self, tg_id, new_speaker) -> None:
        query = update(User).where(User.tg_id == tg_id).values(speaker=new_speaker)
        await session.execute(query)

    @Transactional()
    async def delete_user_info(self, tg_id) -> None:
        messages = select(MessageHistory).where(MessageHistory.tg_id == tg_id)
        await session.delete(messages)
        user = select(User).where(User.tg_id == tg_id).first()
        await session.delete(user)
