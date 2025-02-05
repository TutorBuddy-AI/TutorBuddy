#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:oksana_bot.sock --access-logfile './oksana_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app
