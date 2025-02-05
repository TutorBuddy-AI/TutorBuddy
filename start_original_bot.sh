#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:original_bot.sock --access-logfile './original_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app