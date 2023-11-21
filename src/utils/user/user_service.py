from src.database.models import User, UserLocation, MessageHistory
from src.database import Transactional, session
from src.utils.user.schemas import GetUserInfo, UserInfo, UserLocationInfo, GetUserMessageHistory

from typing import Optional, List

from sqlalchemy import select


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
            limit: int = 50
    ) -> GetUserMessageHistory:
        query = select(MessageHistory).where(MessageHistory.tg_id == str(tg_id))

        query = query.limit(limit)
        result = await session.execute(query)

        result = result.scalars()

        results = [{'role': row.role, 'message': row.message} for row in result]

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
            "english_level": result.english_level
        }
