from src.utils.user import UserService

from aiogram import types
from aiogram.filters.base import Filter


class IsNotRegister(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return not await UserService().is_exist(str(message.from_user.id))


class IsRegister(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return await UserService().is_exist(str(message.from_user.id))
