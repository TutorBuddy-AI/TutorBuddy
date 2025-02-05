#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:aalingua_admin.sock --access-logfile '/home/ubuntu/aalingua_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
