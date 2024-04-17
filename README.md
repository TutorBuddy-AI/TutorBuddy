# AI Tutor Buddy
## АААААА, это что, документация?
## Install dependencies

```
poetry shell && poetry install
```

## Setup .env keys

```
# [bot]
BOT_TYPE='original' # original/personal
BOT_PERSON='Anastasia' # may use Anastasia for original, or Oksana/AA_Lingua for personal bot
BOT_API_TOKEN='{your_test_bot_token}'
WEBHOOK_URL='{ngrok_active_url}'
# [database]
DATABASE_URL='postgresql+asyncpg://postgres:rMoAwRMbgI@localhost:5432/{db_name}'
# [admin]
ADMIN_PASSWORD='123123'
SECRET_KEY_ADMIN='aboba'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN=100
# [generation]
PROXY = '[["http://13.50.236.62:9670", "7pxHP6", "pHY5rF"]]'
OPENAI_API = '["Bearer {your_openapitoken}"]' # may use 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
ELEVENLABS_API='09a580962bcc1c023379f70fa8cf19bf'
# [admin]
ADMIN_PASSWORD='admin'
```

## Run migrations

```
export CONF_FILE_PATH="./.env.local"
alembic upgrade heads
```

## Run admin

```
export CONF_FILE_PATH="./.env.local"
export PYTHONPATH=$PWD
```

```
python src/admin/admin_main.py
```

Open in browser http://127.0.0.1:8001/admin

Sign in using creds:

Username: admin

Password: your password from `ADMIN_PASSWORD` .env variable

## Run Bot

```
ngrok http 8000
```
Just start it once ⬆️
Then setup ngrok forwarding url to config
```
export CONF_FILE_PATH="./.env.local"
python main.py
```

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

DON'T USE IT LOCALLY

```
t.me/tutorbuddyai_bot - 6348419609:AAElinRGeTOxK8bhkJaRiD8xftFCqBM9MF8

t.me/TutorBuddy_Andrizh_bot - 6707186501:AAFUPlkTeaq5uW82iBkCyktZEf3qL6q4R_s
```
