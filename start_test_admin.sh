#!/bin/bash
poetry shell
gunicorn --worker-class uvicorn.workers.UvicornWorker --bind unix:test_admin.sock --access-logfile '/home/ubuntu/test_admin.log' --forwarded-allow-ips "*" -m 007 wsgi:app
