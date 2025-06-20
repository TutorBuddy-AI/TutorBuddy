import logging
import os
import uvicorn

from src.config import config

logging.basicConfig(level=logging.INFO)

# create static directory if not exist
os.makedirs("./static", 0o777, exist_ok=True)


def main():
    uvicorn.run(
        app="src.fastapi_app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=False,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )


if __name__ == "__main__":
    main()
