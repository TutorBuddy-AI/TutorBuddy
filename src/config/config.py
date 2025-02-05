import os

from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

CONF_FILE_PATH = os.environ.get("CONF_FILE_PATH")
load_dotenv(dotenv_path=CONF_FILE_PATH)

BOT_TYPE = os.environ.get("BOT_TYPE")
BOT_PERSON = os.environ.get("BOT_PERSON")
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBHOOK_SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET_TOKEN")
OPENAI_API = os.environ.get('OPENAI_API')
PAYMENT_ID = os.environ.get('PAYMENT_ID')
PAYMENT_KEY = os.environ.get('PAYMENT_KEY')
PAYMENT_RETURN_URL = os.environ.get('PAYMENT_RETURN_URL')
PAYMENT_PRICE_1MO = os.environ.get('PAYMENT_PRICE_1MO')
PAYMENT_PRICE_6MO = os.environ.get('PAYMENT_PRICE_6MO')
PAYMENT_1MO_DURATION = os.environ.get('PAYMENT_1MO_DURATION')        # 44640 minutes for 31 days, 10 minutes for test purposes
PAYMENT_DEMO_DURATION = os.environ.get('PAYMENT_DEMO_DURATION')        # 2880 minutes for 2 days, 8 minutes for test purposes
PAYMENT_FREE_RESET_DURATION = os.environ.get('PAYMENT_FREE_RESET_DURATION')        # 1080 minutes for 18 hours, 5 minutes for test purposes
PAYMENT_FREE_MSG = os.environ.get('PAYMENT_FREE_MSG')
PAYMENT_FREE_MIST = os.environ.get('PAYMENT_FREE_MIST')
PAYMENT_DEMO_RESET_TAG = os.environ.get('PAYMENT_DEMO_RESET_TAG')
PAYMENT_FREE_10MIN_TAG = os.environ.get('PAYMENT_FREE_10MIN_TAG')
PAYMENT_FREE_1MO_TAG = os.environ.get('PAYMENT_FREE_1MO_TAG')
PROXY = os.environ.get('PROXY')
ELEVENLABS_API = os.environ.get('ELEVENLABS_API')
VOICE_ID_ANASTASIA = os.environ.get('VOICE_ID_ANASTASIA')
VOICE_ID_AA_LINGUA = os.environ.get('VOICE_ID_AA_LINGUA')
VOICE_ID_OKSANA = os.environ.get('VOICE_ID_OKSANA')
VOICE_ID_VICTORIA = os.environ.get('VOICE_ID_VICTORIA')
VOICE_ID_KATYA = os.environ.get('VOICE_ID_KATYA')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', "files")
APP_HOST: str = os.environ.get('APP_HOST', "localhost")
APP_PORT: str = os.environ.get('APP_PORT', 8000)
SECRET_KEY_ADMIN = os.environ.get("SECRET_KEY_ADMIN")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN")
TIME_ZONE = "Etc/UTC"
#TIME_ZONE = "Europe/Moscow"

class Config(BaseModel):
    SKIP_UPDATES: bool = True
    APP_HOST: str = APP_HOST
    APP_PORT: int = APP_PORT
    BOT_TYPE: str = BOT_TYPE
    BOT_PERSON: str = BOT_PERSON
    BOT_API_TOKEN: str = BOT_API_TOKEN
    DATABASE_URL: str = DATABASE_URL
    WEBHOOK_URL: str = WEBHOOK_URL
    WEBHOOK_SECRET_TOKEN: str = WEBHOOK_SECRET_TOKEN
    WEBHOOK_PATH: str = "/webhook"
    OPENAI_API: List = OPENAI_API
    ELEVENLABS_API: str = ELEVENLABS_API
    VOICE_ID_ANASTASIA: str = VOICE_ID_ANASTASIA
    VOICE_ID_AA_LINGUA: str = VOICE_ID_AA_LINGUA
    VOICE_ID_OKSANA: str = VOICE_ID_OKSANA
    VOICE_ID_VICTORIA: str = VOICE_ID_VICTORIA
    VOICE_ID_KATYA: str = VOICE_ID_KATYA
    PAYMENT_ID: str = PAYMENT_ID
    PAYMENT_KEY: str = PAYMENT_KEY
    PAYMENT_RETURN_URL: str = PAYMENT_RETURN_URL
    PAYMENT_PRICE_1MO: str = PAYMENT_PRICE_1MO
    PAYMENT_PRICE_6MO: str = PAYMENT_PRICE_6MO
    PAYMENT_1MO_DURATION: int = int(PAYMENT_1MO_DURATION)
    PAYMENT_DEMO_DURATION: int = int(PAYMENT_DEMO_DURATION)
    PAYMENT_FREE_RESET_DURATION: int = int(PAYMENT_FREE_RESET_DURATION)
    PAYMENT_FREE_MSG: int = int(PAYMENT_FREE_MSG)
    PAYMENT_FREE_MIST: int = int(PAYMENT_FREE_MIST)
    PAYMENT_DEMO_RESET_TAG: str = PAYMENT_DEMO_RESET_TAG
    PAYMENT_FREE_10MIN_TAG: str = PAYMENT_FREE_10MIN_TAG
    PAYMENT_FREE_1MO_TAG: str = PAYMENT_FREE_1MO_TAG
    PROXY: List = PROXY
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    UPLOAD_FOLDER: str = UPLOAD_FOLDER
    SECRET_KEY_ADMIN: str = SECRET_KEY_ADMIN
    ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN: int = int(ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN)
    TIME_ZONE: str = TIME_ZONE


config = Config()
