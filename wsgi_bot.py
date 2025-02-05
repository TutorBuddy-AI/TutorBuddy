from src.fastapi_app.webhook import app
from src.config import dp, bot, config

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT, proxy_headers=True,reload=False, forwarded_allow_ips="*")
