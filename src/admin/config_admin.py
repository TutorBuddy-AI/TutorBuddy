from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jose import jwt
from pathlib import Path
from dotenv import load_dotenv
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

image_directory = "static/img/img_newsletter"

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin",
    }
}

dotenv_path = Path('.env.local')
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY_ADMIN = os.environ.get("SECRET_KEY_ADMIN")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN")



def create_jwt_token(data: dict):
    """
    Создается токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_ADMIN, algorithm=ALGORITHM)
    return encoded_jwt


async def generate_token_and_redirect(username: str) -> RedirectResponse:
    """
    Принимаем username по нему делаем токен и закидываем его в куки
    """
    token_data = {"sub": username}
    token = create_jwt_token(token_data)
    response = RedirectResponse(url="/admin")
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response