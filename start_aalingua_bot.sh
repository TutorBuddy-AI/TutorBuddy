#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:aalingua_bot.sock --access-logfile './aalingua_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app
