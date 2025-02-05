#!/bin/bash
# poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:original_admin.sock --access-logfile '/home/ubuntu/original_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
