from datetime import datetime
import base64
import os
from fastapi import Form
from fastapi import Request, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from jose import JWTError, jwt

from sqlalchemy import select, desc, text, delete

from src.admin.newsletter_admin.newsletter_admin import Newsletter
from src.database.models.admin import Admin, pwd_context
from src.admin.config_admin import ( app, templates,
    SECRET_KEY_ADMIN, ALGORITHM, image_directory, generate_token_and_redirect
)

from src.admin.model_pydantic import NewsletterData, ChangeNewsletter
from src.database.models import User, MessageHistory, DailyNews

from src.database import session


"""Docs /docs"""


async def is_valid_token(token: str = Cookie(None, alias="Authorization")):
    """
    Проверка валидности JWT-токена.
    """
    try:
        if token is None:
            return False

        token = token.split("Bearer ")[-1]

        payload = jwt.decode(token, SECRET_KEY_ADMIN, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        query = select(Admin).where(Admin.username == username)
        result = await session.execute(query)
        admin = result.scalars().first()
        if username is None or username != admin.username:
            return False
    except JWTError:
        return False

    return True


@app.get("/admin", response_model=str)
async def admin_page(request: Request, is_valid: bool = Depends(is_valid_token)):
    """html admin
    """
    if not is_valid:
        return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("admin.html", {"request": request})

@app.post("/admin")
async def admin_page_post(request: Request, is_valid: bool = Depends(is_valid_token)):
    """после login идет post запрос на admin
    """
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/get_users")
async def get_users(is_valid: bool = Depends(is_valid_token)):
    """
    Показывает начальную информацию о пользователях.
    Пример успешного ответа:

    ```json
    [
        {
            "tg_id": "148912340",
            "tg_firstName": "FirstName19",
            "tg_lastName": "LastName19",
            "tg_username": "username19",
            "last_message": "2024-03-06 19:09:01"
        }
    ]
    ```
    """
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().unique().all()

    users_with_last_message = []
    for user in users:
        query_info_message = (
            select(MessageHistory)
            .where(MessageHistory.tg_id == str(user.tg_id))
            .order_by(desc(MessageHistory.created_at))
            .limit(1)
        )
        result_info_message = await session.execute(query_info_message)
        user_last = result_info_message.scalars().first()

        if user_last:
            user_data = {
                "tg_id": user.tg_id,
                "tg_firstName": user.tg_firstName,
                "tg_lastName": user.tg_lastName,
                "tg_username": user.tg_username,
                "last_message": datetime.strftime(user_last.created_at, "%Y-%m-%d %H:%M:%S")
            }

            users_with_last_message.append(user_data)

    return JSONResponse(content=users_with_last_message)


@app.post("/save-newsletter")
async def save_newsletter(
    newsletter_data: NewsletterData,
    is_valid: bool = Depends(is_valid_token)
):
    """
    Сохранение рассылки в базу DailyNews.
    Пример запроса:
    ```json
    {
        "topic": "Music",
        "url": "https://the_weeknd_last/music",
        "message": "Подробности в нашей новой рассылке!",
        "image": "base64_encoded_image_data"
    }
    ```
    """
    try:
        topic = newsletter_data.topic
        url = newsletter_data.url
        message = newsletter_data.message
        edition = newsletter_data.edition
        publication_date = newsletter_data.publication_date
        title = newsletter_data.title

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"newsletter_image_{timestamp}.jpg"
        image_path = os.path.join(image_directory, image_filename)

        image_data = newsletter_data.image
        image_data_decoded = base64.b64decode(image_data)

        with open(image_path, "wb") as image_file:
            image_file.write(image_data_decoded)

        new_newsletter = DailyNews(
            message=message,
            topic=topic,
            url=url,
            path_to_data=image_path,
            edition=edition,
            publication_date=publication_date,
            title=title
        )

        session.add(new_newsletter)
        await session.commit()

        return JSONResponse(content={"message": "Рассылка успешно сохранена"})
    except Exception as e:
        return JSONResponse(content={"error": f"Не удалось сохранить рассылку. {str(e)}"}, status_code=500)


@app.get("/get_newsletters")
async def get_newsletters(is_valid: bool = Depends(is_valid_token)):
    """
    Возвращает информацию о всех рассылках пользователей.
    Пример успешного ответа:
    ```json
    [
        {
            "id": 7,
            "message": "fdsfsdfsdfsdf",
            "topic": "dfssdf",
            "url": "http://127.0.0.1:8000/admin#",
            "path_to_data": "static/img/img_newsletter/newsletter_image_20240311023457.jpg"
        }
    ]
    ```
    """
    query = select(DailyNews)
    result = await session.execute(query)
    newsletters = result.scalars().unique().all()

    if newsletters:
        newsletters_list = [
            {
                "id": newsletter.id,
                "message": newsletter.message,
                "topic": newsletter.topic,
                "url": newsletter.url,
                "path_to_data": newsletter.path_to_data,
            }
            for newsletter in newsletters
        ]
        return JSONResponse(content=newsletters_list)
    else:
        return {"status":"empty"}


@app.get("/get_newsletter_info/{newsletter_id}")
async def get_newsletter_info(newsletter_id: int, is_valid: bool = Depends(is_valid_token)):
    """
    Возвращает информацию о рассылке по её идентификатору.
    Пример успешного ответа:

    ```json
    {
        "id": 7,
        "message": "fdsfsdfsdfsdf",
        "topic": "dfssdf",
        "url": "http://127.0.0.1:8000/admin#",
        "path_to_data": "static/img/img_newsletter/newsletter_image_20240311023457.jpg"
    }
    ```
    """
    query = select(DailyNews).where(DailyNews.id == newsletter_id)
    result = await session.execute(query)
    newsletter = result.scalars().first()

    newsletter_info = {
        "id": newsletter.id,
        "message": newsletter.message,
        "topic": newsletter.topic,
        "url": newsletter.url,
        "path_to_data": newsletter.path_to_data,
        "edition": newsletter.edition,
        "publication_date": newsletter.publication_date,
        "title": newsletter.title,
    }

    return JSONResponse(content=newsletter_info)


@app.put("/change_newsletter_info")
async def change_newsletter_info(newsletter: ChangeNewsletter, is_valid: bool = Depends(is_valid_token)):
    """
    Изменение DailyNews.
    Пример запроса:
    ```json
    {
        "newsletter_id": 1,
        "column": "topic",
        "changed_text": "Music"
    }
    ```
    """
    try:
        query = select(DailyNews).where(DailyNews.id == newsletter.newsletter_id)
        result = await session.execute(query)
        newsletter_info = result.scalars().first()
        setattr(newsletter_info, newsletter.column, newsletter.changed_text)
        await session.commit()

        return {"message": "Успешно изменено"}
    except Exception as e:
        return JSONResponse(content={"error": f"Не удалось изменить. {str(e)}"}, status_code=500)

@app.delete("/del_newsletter/{newsletter_id}")
async def del_newsletter(newsletter_id: int, is_valid: bool = Depends(is_valid_token)):
    """
    Удаление рассылки по идентификатору newsletter_id.
    Пример ответа:
    ```json
    {
        "status": "success delete newsletter with id: 123"
    }
    ```
    """
    query = select(DailyNews).where(DailyNews.id == newsletter_id)
    result = await session.execute(query)
    newsletter = result.scalars().first()

    if os.path.exists(newsletter.path_to_data):
        os.remove(newsletter.path_to_data)

    delete_query = delete(DailyNews).where(DailyNews.id == newsletter_id)
    result = await session.execute(delete_query)
    await session.commit()


    return {"status": f"success delete newsletter with id: {newsletter_id}"}


@app.get("/send_newsletter/{newsletter_id}")
async def send_newsletter(newsletter_id: int, is_valid: bool = Depends(is_valid_token)):
    """
    Отправляет рассылку по newsletter_id
    """
    query = select(DailyNews).where(DailyNews.id == newsletter_id)
    result = await session.execute(query)
    newsletter = result.scalars().first()
    await Newsletter().send_newsletter(newsletter)
    return {"message":"200"}



@app.get("/get_message_history_user/{tg_id}")
async def get_message_history(tg_id: int, is_valid: bool = Depends(is_valid_token)):
    """
    Получение истории сообщений для пользователя с указанным tg_id.
    Пример успешного ответа:
    ```json
    [
        {
            "message": "Привет, как дела?",
            "role": "user",
            "type": "text",
            "created_at": "2024-03-12 15:30:45"
        },
        {
            "message": "Привет! Всё отлично, спасибо!",
            "role": "admin",
            "type": "text",
            "created_at": "2024-03-12 15:35:12"
        }
    ]
    ```

    Пример ответа, если история пуста:
    ```json
    {
        "status": "empty"
    }
    ```
    """
    query = select(MessageHistory).where(MessageHistory.tg_id == str(tg_id))
    result = await session.execute(query)
    message_history = result.scalars().unique().all()

    if message_history:
        message_history_list = [
            {
                "message": message.message,
                "role": message.role,
                "type": message.type,
                "created_at": datetime.strftime(message.created_at, "%Y-%m-%d %H:%M:%S")
            }
            for message in message_history
        ]
        return JSONResponse(content=message_history_list)
    else:
        return {"status":"empty"}


@app.get("/get_info_user/{tg_id}")
async def get_user_profile(tg_id: int, is_valid: bool = Depends(is_valid_token)):
    """
    Получение информации о пользователе с указанным tg_id.
    Пример успешного ответа:

    ```json
    {
        "id": 1,
        "tg_id": "1234567",
        "call_name": "Name",
        "speaker": "Bot",
        "tg_firstName": "FirstName",
        "tg_lastName": "LastName",
        "tg_language": "ru",
        "tg_username": "tglastname",
        "source": "",
        "goal": "business",
        "native_lang": "RU",
        "teach_lang": "EN",
        "topic": "Psychology StartUps Fashion ",
        "additional_topic": "",
        "english_level": "1",
        "created_at": "2024-03-05 06:02:04"
    }
    ```

    Пример ответа при отсутствии пользователя:

    ```json
    {
        "detail": "User not found"
    }
    """
    query = select(User).where(User.tg_id == str(tg_id))
    result = await session.execute(query)
    user = result.scalars().first()

    if user:
        user_dict = {
            "id": user.id,
            "tg_id": user.tg_id,
            "call_name": user.call_name,
            "speaker": user.speaker,
            "tg_firstName": user.tg_firstName,
            "tg_lastName": user.tg_lastName,
            "tg_language": user.tg_language,
            "tg_username": user.tg_username,
            "source": user.source,
            "goal": user.goal,
            "native_lang": user.native_lang,
            "teach_lang": user.teach_lang,
            "topic": user.topic,
            "additional_topic": user.additional_topic,
            "english_level": user.english_level,
            "created_at": datetime.strftime(user.created_at, "%Y-%m-%d %H:%M:%S")
        }
        return JSONResponse(content=user_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/get_statistic")
async def get_statistic(is_valid: bool = Depends(is_valid_token)):
    """
    Получение статистики по приложению.
    Пример успешного ответа:

    ```json
    {
        "count_users": 1000,
        "count_messages": 5000,
        "count_topic": {
            "Language": 300,
            "StartUps": 150,
            "Fashion": 200
        },
        "count_choice_nastya": 700,
        "count_choice_bot": 300
    }
    ```
    """
    query_count_users = text('SELECT COUNT(*) AS count_users FROM "user"')
    result_count_users = await session.execute(query_count_users)
    count_users = result_count_users.scalar()

    query_count_messages = text('SELECT COUNT(*) AS count_messages FROM "message_history"')
    result_count_messages = await session.execute(query_count_messages)
    count_messages = result_count_messages.scalar()

    query_count_user_choice_nastya = text('SELECT COUNT(*) FROM "user" WHERE "user"."speaker" = :speaker')
    result_count_choice_nastya = await session.execute(query_count_user_choice_nastya, {"speaker": "Anastasia"})
    count_choice_nastya = result_count_choice_nastya.scalar()

    query_count_user_choice_bot = text('SELECT COUNT(*) FROM "user" WHERE "user"."speaker" = :speaker')
    result_count_choice_bot = await session.execute(query_count_user_choice_bot, {"speaker": "TutorBuddy"})
    count_choice_bot = result_count_choice_bot.scalar()

    query_count_topic = text(
        'SELECT unnest(string_to_array("topic", \' \')) AS topic, COUNT(*) AS topic_count FROM "user" GROUP BY topic;')
    result_count_topic = await session.execute(query_count_topic)
    count_topic_rows = result_count_topic.fetchall()
    count_topic_dict = dict(count_topic_rows)
    count_topic_dict_filtered = {key: value for key, value in count_topic_dict.items() if key != ''}

    statistic = {
        "count_users": count_users,
        "count_messages": count_messages,
        "count_topic":count_topic_dict_filtered,
        "count_choice_nastya":count_choice_nastya,
        "count_choice_bot": count_choice_bot
    }

    return JSONResponse(content=statistic)


@app.get("/")
async def login_page(request: Request):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    """
    Обработка запроса на вход пользователя.
    """
    username = form_data.username
    password = form_data.password

    query = select(Admin).where(Admin.username == username)
    result = await session.execute(query)
    admin = result.scalars().first()

    if admin.username == username and pwd_context.verify(password, admin.password):
        return await generate_token_and_redirect(username)
    else:
        error_message = "Invalid username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

@app.post("/change_password")
async def change_password(username: str = Form(...),
                          new_password: str = Form(...),
                          confirm_password: str = Form(...),request: Request = None):
    """
    Смена пароля.
    """
    query = select(Admin).where(Admin.username == username)
    result = await session.execute(query)
    admin = result.scalars().first()
    if admin and new_password == confirm_password:
        hashed_password = pwd_context.hash(new_password)
        admin.password = hashed_password
        await session.commit()
        return await generate_token_and_redirect(username)
    error_message_change_password = "Username or passwords do not match"
    return templates.TemplateResponse("login.html", {"error_message": error_message_change_password, "request": request})

@app.get("/logout")
async def logout(request: Request):
    """
    Выход.
    """
    response = RedirectResponse(url="/")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8001, reload=True)
