#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:test_bot.sock --access-logfile './test_bot.log' --forwarded-allow-ips "*" -m 007 wsgi_bot:app
