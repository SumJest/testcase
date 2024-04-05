#!/bin/sh

python manage.py migrate

uvicorn testcase.asgi:application --host 0.0.0.0 --port 8002 --log-level info