from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import jwt

from src.config.config import config

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

image_directory = "static/img/img_newsletter"
audio_directory = "static/audio/newsletter_audio"


def create_jwt_token(data: dict):
    """
    Создается токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY_ADMIN, algorithm=config.ALGORITHM)
    return encoded_jwt


async def generate_token_and_redirect(username: str) -> RedirectResponse:
    """
    Принимаем username по нему делаем токен и закидываем его в куки
    """
    token_data = {"sub": username}
    token = create_jwt_token(token_data)
    response = RedirectResponse(url="./admin")
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response
