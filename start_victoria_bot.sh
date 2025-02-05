#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:victoria_bot.sock --access-logfile './victoria_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app
