FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/:/backend/transactionManager"

EXPOSE 8000
WORKDIR /backend/transactionManager
RUN apt-get update && apt-get upgrade -y && apt-get clean

# RUN mkdir -p /backend/transactionManager/staticfiles
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt --no-cache-dir

# TODO remove when volume will be created
COPY ./transactionManager /backend/transactionManager/

RUN useradd -u 1000 my-user
ADD --chown=1000:1000 ./transactionManager /backend/transactionManager
USER my-user

RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver"]
CMD ["gunicorn", "transactionManager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4", "--timeout", "120"]
