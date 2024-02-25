# from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.config import config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(config.BOT_API_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(storage=MemoryStorage())
