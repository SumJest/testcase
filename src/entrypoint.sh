#!/bin/sh

python manage.py migrate

celery -A testcase worker -l info --concurrency 1 -P solo &
uvicorn testcase.asgi:application --host 0.0.0.0 --port 8002 --log-level info