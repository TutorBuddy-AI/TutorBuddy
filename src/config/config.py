import os

from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env.local')
load_dotenv(dotenv_path=dotenv_path)

BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBHOOK_SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET_TOKEN")
OPENAI_API = os.environ.get('OPENAI_API')
PROXY = os.environ.get('PROXY')
ELEVENLABS_API = os.environ.get('ELEVENLABS_API')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', "files")
APP_HOST: str = os.environ.get('APP_HOST', "localhost")
APP_PORT: str = os.environ.get('APP_PORT', 8000)


class Config(BaseModel):
    SKIP_UPDATES: bool = True
    APP_HOST: str = APP_HOST
    APP_PORT: int = APP_PORT
    BOT_API_TOKEN: str = BOT_API_TOKEN
    DATABASE_URL: str = DATABASE_URL
    WEBHOOK_URL: str = WEBHOOK_URL
    WEBHOOK_SECRET_TOKEN: str = WEBHOOK_SECRET_TOKEN
    WEBHOOK_PATH: str = "/webhook"
    OPENAI_API: List = OPENAI_API
    ELEVENLABS_API: str = ELEVENLABS_API
    PROXY: List = PROXY
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    UPLOAD_FOLDER: str = UPLOAD_FOLDER


config = Config()
