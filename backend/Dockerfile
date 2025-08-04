FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/:/backend/transactionManager"

RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN useradd -m -u 1000 backend
WORKDIR /backend/transactionManager

COPY --chown=backend:backend ./entrypoint.sh /backend/transactionManager/entrypoint.sh

COPY ./requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt --no-cache-dir

COPY --chown=backend:backend ./transactionManager /backend/transactionManager/
USER backend

CMD ["./entrypoint.sh"]