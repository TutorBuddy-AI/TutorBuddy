#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:oksana_admin.sock --access-logfile '/home/ubuntu/oksana_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
