from src.utils.user import UserService

from aiogram import types
from aiogram.dispatcher.filters import Filter


class IsNotRegister(Filter):
    async def check(self, message: types.Message) -> bool:
        return not await UserService().is_exist(str(message.from_user.id))
