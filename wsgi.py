from src.admin.admin_main import app
from fastapi import FastAPI, APIRouter


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="src.admin.admin_main:app", host='127.0.0.1', port=8001, proxy_headers=True, forwarded_allow_ips="*")
