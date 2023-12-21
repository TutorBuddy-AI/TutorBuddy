import shutil

import aiofiles
import uvicorn
import os
from fastapi import Form
from starlette.middleware import Middleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView
from src.database.models import User, UserLocation, Role, MessageHistory, DailyNews, MessageMistakes
from src.database.models.enums.daily_news import DailyNewsEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin import EnumField, TinyMCEEditorField, FileField
from starlette_admin.exceptions import FormValidationError, LoginFailed
import logging
from starlette.datastructures import UploadFile
from starlette.responses import FileResponse
import shutil
from starlette.responses import JSONResponse

Base = declarative_base()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_async_engine(DATABASE_URL, future=True)

logging.basicConfig(level=logging.INFO)

# create static directory if not exist
os.makedirs("./static", 0o777, exist_ok=True)

users = {
    "admin": {
        "name": "admin",
        "avatar": "avatar.png",
        "roles": ["read", "create", "edit", "delete", "action_make_published", "admin"],
    },
}

app = Starlette(routes=[
    Mount(
        "/static", app=StaticFiles(directory="static"), name="static"
    ),
], )  # FastAPI()


class MyAuthProvider(AuthProvider):
    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 3 characters"}
            )

        if username in users and password == os.getenv('ADMIN_PASSWORD'):
            """Save `username` in session"""
            request.session.update({
                "username": username,
                "name": users[username]["name"],
                "roles": users[username]["roles"],
                "avatar": "avatar.png"
            })
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None):
            request.state.user = {
                "name": request.session["username"],
                "username": request.session["username"],
                "roles": request.session["roles"],
                "avatar": request.session["avatar"]
            }
            return True

        return False

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = None
        if user["avatar"] is not None:
            photo_url = request.url_for("static", path=user["avatar"])
        return AdminUser(username=user["name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response


# Create admin
admin = Admin(engine, title="AI Tutor Buddy Admin",
              auth_provider=MyAuthProvider(allow_paths=["/static/logo.svg"]),
              middlewares=[Middleware(SessionMiddleware, secret_key=os.getenv("SECRET"))], )


# example how to work with fields and access
class UserView(ModelView):
    exclude_fields_from_list = [User.id, User.created_at, User.updated_at]
    exclude_fields_from_edit = [User.created_at, User.updated_at]
    exclude_fields_from_create = [User.created_at, User.updated_at]
    page_size_options = [10, 25, 50, 100, -1]
    save_state = True

    def is_accessible(self, request: Request) -> bool:
        roles = ['admin']

        return any(role in roles for role in request.state.user["roles"])

    def can_delete(self, request: Request) -> bool:
        return "admin" in request.state.user["roles"]


class DailyNewsView(ModelView):
    fields = [
        DailyNews.id,
        DailyNews.topic,
        TinyMCEEditorField("message"),
        FileField("file_upload"),  # Добавляем поле загрузки файла
        EnumField(
            "type",
            choices=[
                (DailyNewsEnum.NEWS_TYPE__TEXT.value, "Текст"),
                (DailyNewsEnum.NEWS_TYPE__IMAGE.value, "Изображение"),
                (DailyNewsEnum.NEWS_TYPE__FILE.value, "Файл"),
                (DailyNewsEnum.NEWS_TYPE__VIDEO.value, "Видео"),
            ],
        ),
    ]


class DailyNewsView(ModelView):
    fields = [
        DailyNews.id,
        DailyNews.topic,
        TinyMCEEditorField("message"),
        FileField("file_upload"),
        EnumField(
            "type",
            choices=[
                (DailyNewsEnum.NEWS_TYPE__TEXT.value, "Текст"),
                (DailyNewsEnum.NEWS_TYPE__IMAGE.value, "Изображение"),
                (DailyNewsEnum.NEWS_TYPE__FILE.value, "Файл"),
                (DailyNewsEnum.NEWS_TYPE__VIDEO.value, "Видео"),
            ],
        ),
    ]

    async def on_file_upload(self, request: Request):
        form = await request.form()
        upload_file = form["file_upload"]
        SAVE_DIR = "src/daily_data"
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        file_path = os.path.join(SAVE_DIR, upload_file.filename)
        async with aiofiles.open(file_path, "wb") as dest:
            contents = await upload_file.read()
            await dest.write(contents)
        logging.info("Файл успешно загружен")





exclude_fields_from_list = [DailyNews.created_at, DailyNews.updated_at]
exclude_fields_from_edit = [DailyNews.created_at, DailyNews.updated_at]
exclude_fields_from_create = [User.created_at, User.updated_at]
page_size_options = [10, 25, 50, 100, -1]
save_state = True

# Add view
admin.add_view(UserView(User, label='Пользователи'))
admin.add_view(ModelView(UserLocation))
admin.add_view(ModelView(Role))
admin.add_view(ModelView(MessageHistory))
admin.add_view(ModelView(MessageMistakes))
admin.add_view(DailyNewsView(DailyNews))

# Mount admin to your app
admin.mount_to(app)

if __name__ == "__main__":
    uvicorn.run("admin:app", port=8001, reload=True)
