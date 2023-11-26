# AI Tutor Buddy

## Install dependencies

```
poetry shell && poetry install
```

## Setup .env keys

```
BOT_API_TOKEN=''
DATABASE_URL='postgresql+asyncpg://user:password@127.0.0.1:5432/db_name'
ADMIN_PASSWORD='123123'
WEBHOOK_URL=''
WEBHOOK_SECRET_TOKEN='' # auth token у ngrok
EDEN_API = '["Bearer api_1", "Bearer api_2"]'
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
python3 set_webhooh_url.py
```
Just start and turn it off once ⬆️
```
python3 main.py
```

If the bot stops working due to frequent server restarts, use ```python3 set_webhooh_url.py```

## SQLAlchemy for asyncio context

```python
from src.database import Transactional, session


@Transactional()
async def create_user(self):
    session.add(User(email="padocon@naver.com"))
```

Do not use explicit `commit()`. `Transactional` class automatically do.

