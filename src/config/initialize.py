import ast

from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.config import config

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.utils.api_limiter.APILimiter import init_api_limitters

bot = Bot(config.BOT_API_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())
open_ai_token_limiters = init_api_limitters(ast.literal_eval(config.OPENAI_API))