from typing import Optional

from sqlalchemy import select, update, delete

from src.database import session
from src.database.models import Setting


class SettingService:
    def __init__(self):
        pass

    @staticmethod
    async def is_summary_on(tgid) -> Optional[bool]:
        query = select(Setting).where(Setting.tg_id == tgid)
        result = await session.execute(query)
        user = result.scalars().first()
        if user is not None:
            return user.summary_on
        else:
            return True

    @staticmethod
    async def is_summary_answered(tgid) -> Optional[bool]:
        query = select(Setting).where(Setting.tg_id == tgid)
        result = await session.execute(query)
        user = result.scalars().first()
        if user is not None:
            return user.summary_answered
        else:
            return False