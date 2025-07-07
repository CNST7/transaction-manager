# Transaction Manager

A modular Django-based backend for managing and reporting product transactions, with CSV upload, REST API, and Dockerized deployment.

## Features

- Upload transactions via CSV file
- REST API for listing, retrieving, and filtering transactions
- Summary reports for customers and products
- Modular monolith architecture, ready for future microservices split
- Docker Compose setup with Nginx gateway
- SQLite (default) database, ready for PostgreSQL migration
- Logging, pagination, and filtering
- Pytest-based test suite

## Stack

- Python 3.12
- Django 5.2.3
- Django REST Framework 3.16.0
- django-filter
- django-naivedatetimefield
- Pydantic 2.11.7
- SQLite3 (default)
- Docker, Docker Compose
- Nginx (gateway)
- Pytest

## Project Structure

```
.
├── backend/
│   ├── transactionManager/
│   │   ├── transactionManager/
│   │   ├── transactionManagerCore/
│   │   └── transactionManagerProcessor/
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── ...
├── gateway/
│   └── nginx.conf
├── docker-compose.yml
└── ...
```

## Getting Started

### Local Development

1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set PYTHONPATH**
   ```sh
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/transactionManager
   ```
5. **Apply migrations**
   ```sh
   cd backend/transactionManager
   python manage.py migrate
   ```
6. **Run the development server**
   ```sh
   python manage.py runserver --settings=transactionManager.settings_local
   ```
   The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Running Tests

```sh
cd backend
pytest
```

### Docker Compose

1. **Build and start services**
   ```sh
   docker-compose up --build
   ```
2. **Access the API**
   - [http://127.0.0.1/](http://127.0.0.1/) (proxied via Nginx)

## API Endpoints

- `POST /transactions/upload` — Upload CSV file with transactions
- `GET /transactions` — List transactions (with filtering)
- `GET /transactions/{id}` — Retrieve transaction details
- `GET /reports/customer-summary/{customer_id}` — Customer summary report
- `GET /reports/product-summary/{product_id}` — Product summary report

## Development Notes

- Modular monolith architecture for easy future refactoring
- Currency exchange rates are hardcoded for simplicity
- Transaction IDs are primary keys; uploading duplicate IDs will overwrite data
- Logging is configured to file and console
- See [backend/README.md](backend/README.md) for more details and TODOs

## TODO

- PostgreSQL support
- Improved Docker volumes and permissions
- Swagger/OpenAPI documentation
- Production settings and CI/CD
- Pre-commit hooks and code linting

More [backend todos](backend/README.md#todo)

**Author:** Michał Jarek

**License:** MIT
