import tempfile
from datetime import datetime, date
import base64
import os
from typing import Any

from fastapi import Form
from fastapi import Request, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy import select, desc, text, delete, Row, RowMapping, func

from config import config
from database.models import NewsletterAudio
from src.utils.newsletter.newsletter_publisher import NewsletterPublisher
from src.database.models.admin import Admin, pwd_context
from src.admin.config_admin import (app, templates, image_directory,
                                    generate_token_and_redirect, audio_directory)

from src.admin.model_pydantic import NewsletterData, ChangeNewsletter, SendNewsletterDatetime, MessageData, \
    SummaryFromParsing
from src.database.models import User, MessageHistory, Newsletter, MessageForUsers, MessageMistakes

from src.database import session
from utils.audio_converter.audio_converter_cache import AudioConverterCache
from utils.news_gallery.news_gallery import NewsGallery
from utils.newsletter.newsletter_service import NewsletterService
from utils.transcriber.text_to_speech import TextToSpeech

"""Docs /docs"""


@app.exception_handler(403)
async def custom_403_handler(request, exc):
    return templates.TemplateResponse("login.html", {"request": request})


async def is_valid_token(token: str = Cookie(None, alias="Authorization")):
    """
    Проверка валидности JWT-токена.
    """
    try:
        if token is None:
            return False

        token = token.split("Bearer ")[-1]

        payload = jwt.decode(token, config.SECRET_KEY_ADMIN, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        query = select(Admin).where(Admin.username == username)
        result = await session.execute(query)
        admin = result.scalars().first()
        if username is None or username != admin.username:
            return False
    except DecodeError:
        return False
    except ExpiredSignatureError:
        return False

    return True


async def check_authentication(is_valid: bool = Depends(is_valid_token)):
    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
    else:
        return True


@app.get("/admin", response_model=str)
async def admin_page(request: Request, deps: bool = Depends(check_authentication)):
    """html admin
    """
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/admin1", response_model=str)
async def admin_page(request: Request, deps: bool = Depends(check_authentication)):
    """html admin
    """
    return templates.TemplateResponse("admin_old.html", {"request": request})


@app.post("/admin")
async def admin_page_post(request: Request, deps: bool = Depends(check_authentication)):
    """после login идет post запрос на admin
    """
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/get_users")
async def get_users():
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().unique().all()

    users_with_last_message = []
    for idx, user in enumerate(users):
        query_info_message = (
            select(MessageHistory)
            .where(MessageHistory.tg_id == str(user.tg_id))
            .order_by(desc(MessageHistory.created_at))
            .limit(1)
        )
        result_info_message = await session.execute(query_info_message)
        user_last = result_info_message.scalars().first()

        user_data = {
            "id": idx + 1,
            "tg_id": user.tg_id,
            "name": None,
            "status": "online",
            "profile": "./static/dist/images/user_chat.png"
        }
        if user.tg_firstName and user.tg_lastName:
            user_data["name"] = f"{user.tg_firstName} {user.tg_lastName}"
        elif user.tg_firstName:
            user_data["name"] = user.tg_firstName
        elif user.tg_lastName:
            user_data["name"] = user.tg_lastName

        if user_last:
            user_data["last_message"] = datetime.strftime(user_last.created_at, "%Y-%m-%d %H:%M:%S")

        users_with_last_message.append(user_data)

    response = {"users": users_with_last_message}
    return JSONResponse(content=response)


@app.post("/save-newsletter")
async def save_newsletter(
        newsletter_data: NewsletterData,
        deps: bool = Depends(check_authentication)
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
        publisher = newsletter_data.publisher
        publication_date = newsletter_data.publication_date
        title = newsletter_data.title

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"newsletter_image_{timestamp}.jpg"
        image_path = os.path.join(image_directory, image_filename)

        image_data = newsletter_data.image
        image_data_decoded = base64.b64decode(image_data)

        with open(image_path, "wb") as image_file:
            image_file.write(image_data_decoded)

        new_newsletter = Newsletter(
            message=message,
            topic=topic,
            url=url,
            path_to_data=image_path,
            publisher=publisher,
            publication_date=publication_date,
            title=title
        )

        session.add(new_newsletter)
        await session.commit()

        post_text = await NewsletterPublisher.formatting_post_text(new_newsletter)
        cleaned_post_text = await NewsletterPublisher.remove_html_tags(post_text)

        audio_files = await save_newsletter_audio(cleaned_post_text)
        newsletter_audio = [
            NewsletterAudio(
                newsletter_id=new_newsletter.id,
                speaker_id=audio_speaker,
                file_path=audio_file
            ) for audio_speaker, audio_file in audio_files.items()]
        session.add_all(newsletter_audio)
        await session.commit()
        return JSONResponse(content={"message": "Newsletter successfully saved"})
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to save the newsletter. {str(e)}"}, status_code=500)


async def save_newsletter_audio(post_text: str):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if config.BOT_TYPE == "original":
        audio = {
            'Anastasia': await TextToSpeech.get_speech_by_voice('Anastasia', post_text),
            'TutorBuddy': await TextToSpeech.get_speech_by_voice('TutorBuddy', post_text)
        }
    else:
        audio = {
            config.BOT_PERSON: await TextToSpeech.get_speech_by_voice(config.BOT_PERSON, post_text)
        }
    audio_output_files = {
        key: os.path.join(audio_directory, f"newsletter_audio_{timestamp}_{key}.ogg") for key in audio.keys()}
    print(audio_output_files)
    AudioConverterCache(audio).convert_audio_to_ogg_fixed_files(audio_output_files)
    return audio_output_files


@app.post("/save-message")
async def save_message(
        message_data: MessageData,
        deps: bool = Depends(check_authentication)
):
    """
    Сохранение рассылки в базу DailyNews.
    Пример запроса:
    ```json
    {
        "message": "Подробности в нашей новой сообщений!",
        "image": "base64_encoded_image_data"
    }
    ```
    """
    try:

        message = message_data.message

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"message_image_{timestamp}.jpg"
        image_path = os.path.join(image_directory, image_filename)

        image_data = message_data.image
        image_data_decoded = base64.b64decode(image_data)

        with open(image_path, "wb") as image_file:
            image_file.write(image_data_decoded)

        new_message = MessageForUsers(
            message=message,
            path_to_data=image_path,
        )

        session.add(new_message)
        await session.commit()

        return JSONResponse(content={"message": "Message successfully saved"})
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to save the newsletter. {str(e)}"}, status_code=500)


@app.get("/get_newsletters")
async def get_newsletters(deps: bool = Depends(check_authentication)):
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
    query = select(Newsletter)
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
        return {"status": "empty"}


@app.get("/get_fresh_newsletters")
async def get_newsletters(deps: bool = Depends(check_authentication)):
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
    query = select(Newsletter).where(func.date(Newsletter.updated_at) == date.today())
    print(query)
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
        return JSONResponse(content=[])


@app.get("/get_newsletter_info/{newsletter_id}")
async def get_newsletter_info(newsletter_id: int, deps: bool = Depends(check_authentication)):
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
    query = select(Newsletter).where(Newsletter.id == newsletter_id)
    result = await session.execute(query)
    newsletter = result.scalars().first()

    newsletter_info = {
        "id": newsletter.id,
        "message": newsletter.message,
        "topic": newsletter.topic,
        "url": newsletter.url,
        "path_to_data": newsletter.path_to_data,
        "publisher": newsletter.publisher,
        "publication_date": newsletter.publication_date,
        "title": newsletter.title,
    }

    return JSONResponse(content=newsletter_info)


@app.put("/change_newsletter_info")
async def change_newsletter_info(
        newsletter: ChangeNewsletter, deps: bool = Depends(check_authentication)):
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
        query = select(Newsletter).where(Newsletter.id == newsletter.newsletter_id)
        result = await session.execute(query)
        newsletter_info = result.scalars().first()
        setattr(newsletter_info, newsletter.column, newsletter.changed_text)
        await session.commit()

        return {"message": "Успешно изменено"}
    except Exception as e:
        return JSONResponse(content={"error": f"Не удалось изменить. {str(e)}"}, status_code=500)


@app.delete("/del_newsletter/{newsletter_id}")
async def del_newsletter(newsletter_id: int, deps: bool = Depends(check_authentication)):
    """
    Удаление рассылки по идентификатору newsletter_id.
    Пример ответа:
    ```json
    {
        "status": "success delete newsletter with id: 123"
    }
    ```
    """
    await NewsletterService.delete_newsletter(newsletter_id)

    return {"status": f"success delete newsletter with id: {newsletter_id}"}


@app.post("/renew_newsletter/{newsletter_id}")
async def renew_newsletter(newsletter_id: int, deps: bool = Depends(check_authentication)):
    """
    Обновление рассылки по идентификатору newsletter_id.
    Пример ответа:
    ```json
    {
        "status": "success renew newsletter with id: 123"
    }
    ```
    """
    await NewsletterService.renew_newsletter(newsletter_id)
    new_newsletter = await NewsletterService.get_newsletter(newsletter_id)

    post_text = await NewsletterPublisher.formatting_post_text(new_newsletter)
    cleaned_post_text = await NewsletterPublisher.remove_html_tags(post_text)

    audio_files = await save_newsletter_audio(cleaned_post_text)
    newsletter_audio = [
        NewsletterAudio(
            newsletter_id=new_newsletter.id,
            speaker_id=audio_speaker,
            file_path=audio_file
        ) for audio_speaker, audio_file in audio_files.items()]
    session.add_all(newsletter_audio)
    await session.commit()

    return {"status": f"success renewed newsletter with id: {newsletter_id}"}


@app.get("/send_newsletter/{newsletter_id}")
async def send_newsletter(newsletter_id: int, deps: bool = Depends(check_authentication)):
    """
    Отправляет рассылку по newsletter_id
    """
    newsletter = await NewsletterService.get_newsletter(newsletter_id)
    await NewsletterPublisher().send_newsletter(newsletter)
    return {"message": "Рассылка успешно отправлена"}


@app.get("/send_newsletter/{newsletter_id}/{tg_id}")
async def send_newsletter_in_chat(newsletter_id: int, tg_id: str, deps: bool = Depends(check_authentication)):
    """
    Отправляет рассылку по newsletter_id
    """
    newsletter = await NewsletterService.get_newsletter(newsletter_id)
    await NewsletterPublisher().send_newsletter_to_chat(newsletter, tg_id)
    return {"message": "Рассылка успешно отправлена"}


@app.get("/send_news_gallery")
async def send_news_gallery():
    """
    Отправляет рассылку по newsletter_id
    """
    await NewsGallery().send_news_gallery()
    return {"message": "Рассылка успешно отправлена"}


@app.post("/send_newsletter_datetime")
async def send_newsletter(
        newsletter_data: SendNewsletterDatetime, deps: bool = Depends(check_authentication)):
    """
    Отправляет рассылку по newsletter_id в дату datetime
    """
    query = select(Newsletter).where(Newsletter.id == newsletter_data.newsletter_id)
    result = await session.execute(query)
    newsletter = result.scalars().first()

    print(newsletter_data.datetime_iso)
    return


@app.get("/get_message_history_user/{tg_id}")
async def get_message_history(tg_id: int, deps: bool = Depends(check_authentication)):
    query = select(MessageHistory).where(MessageHistory.tg_id == str(tg_id))
    result = await session.execute(query)
    message_history = result.scalars().unique().all()

    if message_history:
        message_history_list = [
            {
                "id": idx + 1,
                "from_id": 2 if message.role == "assistant" else 1,
                "to_id": 1 if message.role == "assistant" else 2,
                "msg": message.message,
                "has_dropDown": True,
                "datetime": datetime.strftime(message.created_at, "%I:%M %p"),
                "isReplied": 2 if message.role == "assistant" else 1
            }
            for idx, message in enumerate(message_history)
        ]
        response = {"chats": message_history_list}
        return JSONResponse(content=response)
    else:
        return {"status": "empty"}


@app.get("/get_info_user/{tg_id}")
async def get_user_profile(tg_id: int, deps: bool = Depends(check_authentication)):
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
async def get_statistic(deps: bool = Depends(check_authentication)):
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
        "count_topic": count_topic_dict_filtered,
        "count_choice_nastya": count_choice_nastya,
        "count_choice_bot": count_choice_bot
    }

    return JSONResponse(content=statistic)


@app.get("/get_message_hint_user/{tg_id}")
async def get_message_hint_user(tg_id: int, deps: bool = Depends(check_authentication)):
    """
    Получение информации о ошибках пользователя с указанным tg_id.
    Пример успешного ответа:

    ```json
    {
        "id": 1,
        "tg_id": "1234567",
        "message": "message",
        "created_at": "2024-03-05 06:02:04"
    }
    ```
    """
    query = select(MessageMistakes).where(MessageMistakes.tg_id == str(tg_id))
    result = await session.execute(query)
    user_mistake = result.scalars().first()

    if user_mistake:
        user_dict = {
            "id": user_mistake.id,
            "tg_id": user_mistake.tg_id,
            "message": user_mistake.message,
            "created_at": datetime.strftime(user_mistake.created_at, "%Y-%m-%d %H:%M:%S")
        }
        return JSONResponse(content=user_dict)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/")
async def login_page(request: Request):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/change_password")
async def change_page(request: Request):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("change_password.html", {"request": request})


@app.get("/dialogs")
async def dialogs_page(request: Request, deps: bool = Depends(check_authentication)):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("dialogs.html", {"request": request})


@app.get("/profile")
async def profile_page(request: Request, deps: bool = Depends(check_authentication)):
    """
    Отображение страницы входа.
    """
    return templates.TemplateResponse("profile.html", {"request": request})


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
                          old_password: str = Form(...),
                          new_password: str = Form(...),
                          confirm_password: str = Form(...),
                          request: Request = None):
    """
    Смена пароля.
    """
    query = select(Admin).where(Admin.username == username)
    result = await session.execute(query)
    admin = result.scalars().first()

    if admin and pwd_context.verify(old_password, admin.password):
        if new_password == confirm_password:
            hashed_password = pwd_context.hash(new_password)
            admin.password = hashed_password
            await session.commit()
            return await generate_token_and_redirect(username)
        else:
            error_message_change_password = "New passwords do not match"
    else:
        error_message_change_password = "Username or old password do not match"

    return templates.TemplateResponse("login.html",
                                      {"error_message": error_message_change_password, "request": request})


@app.get("/logout")
async def logout(request: Request):
    """
    Выход.
    """
    response = RedirectResponse(url="/")
    return response


@app.post("/add_summary")
async def add_summary(summary_data: SummaryFromParsing):
    query = select(Newsletter).where(Newsletter.title == summary_data.title)
    result = await session.execute(query)
    existing_entry = result.scalars().first()

    if existing_entry:
        return {"message": "duplicate"}

    newsletter_entry = Newsletter(
        message=summary_data.message,
        topic=summary_data.topic,
        url=summary_data.url,
        path_to_data=summary_data.path_to_data,
        publisher=summary_data.publisher,
        publication_date=summary_data.publication_date,
        title=summary_data.title
    )

    session.add(newsletter_entry)
    await session.commit()

    return {"message": "Data saved successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="src.admin.admin_main:app", port=8001, reload=True)
