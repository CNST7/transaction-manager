#!/bin/bash

set -e

python manage.py migrate --no-input

python manage.py collectstatic --no-input --clear

uvicorn transactionManager.asgi:application --reload --host 0.0.0.0 --port 8000
