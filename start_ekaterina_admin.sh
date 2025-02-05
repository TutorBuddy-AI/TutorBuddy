#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:ekaterina_admin.sock --access-logfile '/home/ubuntu/ekaterina_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
