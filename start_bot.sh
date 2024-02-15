#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:bot.sock --access-logfile './bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app