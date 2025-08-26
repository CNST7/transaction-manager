# Transaction Manager

## 📊 Transaction processing and aggregation system

System allows for importing, validating, processing and sharing transaction data.

1. Import data

   - **[POST]** _/transactions/upload_
   - [sample CSV](backend/tests/integration/fixtures/test.csv)

2. Read data

   - **[GET]** _/transactions_
   - **[GET]** _/transactions/{transaction_id}_

3. Aggregate data

   - **[GET]** _/reports/customer-summary/{customer_id}_
   - **[GET]** _/reports/product-summary/{product_id}_

     | Both endpoints accept the optional query parameters `date_from` and `date_to` in `YYYY-MM-DD` format.

## ⚙️ Technology stack

- 🐍 [Python](https://www.python.org/)
- 🔨 [Django](https://www.djangoproject.com/)
- 🔧 [DRF](https://www.django-rest-framework.org/)
- 🐘 [PostgreSQL](https://www.postgresql.org/)
- 🌱 [Celery](https://docs.celeryq.dev/en/stable/index.html)
- 🐰 [RabbitMQ](https://www.rabbitmq.com/)
- 🔑 [Redis](https://redis.io/)
- 🐳 [Docker compose](https://docs.docker.com/compose/)
- 🧪 [Pytest](https://docs.pytest.org/en/stable/)
- 🌐 [NGINX](https://nginx.org/en/)
- ✨ [Pre-commit](https://pre-commit.com)

## 🚀 Start project

To start project run `docker compose up -d --build` and visit [localhost](http://localhost/)

## 💻 Backend Development

Backend docs: [backend/README.md](backend/README.md)

## 👨‍💻 Author

Michał Jarek
