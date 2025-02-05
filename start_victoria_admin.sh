#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:victoria_admin.sock --access-logfile '/home/ubuntu/victoria_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
