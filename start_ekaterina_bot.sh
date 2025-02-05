#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:ekaterina_bot.sock --access-logfile './ekaterina_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app
