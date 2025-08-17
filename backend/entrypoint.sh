#!/bin/bash

set -e 

python manage.py migrate

python manage.py collectstatic

uvicorn transactionManager.asgi:application --reload --host 0.0.0.0 --port 8000