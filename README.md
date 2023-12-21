# AI Tutor Buddy
## АААААА, это что, документация?
## Install dependencies

```
poetry shell && poetry install
```

## Setup .env keys

```
BOT_API_TOKEN=''
DATABASE_URL=''
ADMIN_PASSWORD=''
WEBHOOK_URL=''
WEBHOOK_SECRET_TOKEN='' # auth token у ngrok
OPENAI_API = '["Bearer token"]'
PROXY = '[["http://131.108.17.251:9670", "7pxHP6", "pHY5rF"]]'    # HTTPS, Логин, Пароль. Если нету, пользуйтесь этим
ELEVENLABS_API = 'c207730cb78101ce98761b628554b3a2'
```

## Run migrations

```
alembic upgrade head
```

## Run admin

```
export PYTHONPATH=$PWD
```

```
python3 src/admin/admin.py
```

Open in browser http://127.0.0.1:8001/admin

Sign in using creds:

Username: admin

Password: your password from `ADMIN_PASSWORD` .env variable

## Run Bot

```
python3 set_webhook_url.py
```
Just start and turn it off once ⬆️
```
python3 main.py
```

If the bot stops working due to frequent server restarts, use ```python3 set_webhook_url.py```

## SQLAlchemy for asyncio context

```python
from src.database import Transactional, session


@Transactional()
async def create_user(self):
    session.add(User(email="padocon@naver.com"))
```

Do not use explicit `commit()`. `Transactional` class automatically do.

## Connect to Data Base
```
postgresql+asyncpg://postgres:123@localhost:5432/bot

psql -h localhost -U postgres -d bot
password: 123

```

## Bot Token for prod

```
t.me/tutorbuddyai_bot - 6348419609:AAElinRGeTOxK8bhkJaRiD8xftFCqBM9MF8

t.me/TutorBuddy_Andrizh_bot - 6707186501:AAFUPlkTeaq5uW82iBkCyktZEf3qL6q4R_s
```