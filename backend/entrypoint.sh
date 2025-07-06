#!/bin/bash

set -e 

python manage.py migrate

# gunicorn transactionManager.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --timeout 120

uvicorn transactionManager.asgi:application --reload --host 0.0.0.0 --port 8000