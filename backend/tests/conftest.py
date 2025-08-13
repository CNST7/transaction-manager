import pytest
from transactionManagerProcessor.models import (
    Transaction,
    TransactionCSV,
)
from transactionManagerProcessor.enums import Currency
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from collections.abc import Generator
from django.conf import settings
from pathlib import PosixPath
from transactionManager.settings_test import BASE_TEST_DIR
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

pytestmark = pytest.mark.django_db()


@pytest.fixture(autouse=True)
def temp_media_root(tmp_path: PosixPath, settings):
    temp_dir = tmp_path / "media"
    temp_dir.mkdir()
    settings.MEDIA_ROOT = str(temp_dir)
    yield


@pytest.fixture
def product_id_a(scope="session") -> UUID:
    return UUID("a" + "e64a915-9711-47f3-a640-be6f517546b1")


@pytest.fixture
def product_id_b(scope="session") -> UUID:
    return UUID("b" + "e64a915-9711-47f3-a640-be6f517546b1")


@pytest.fixture
def customer_id_a(scope="session") -> UUID:
    return UUID("a" + "4245004-9354-4b77-8744-19e36372f4cd")


@pytest.fixture
def customer_id_b(scope="session") -> UUID:
    return UUID("b" + "4245004-9354-4b77-8744-19e36372f4cd")


@pytest.fixture
def single_transaction(
    customer_id_a: UUID, product_id_a: UUID, scope="session"
) -> Transaction:
    return Transaction.objects.create(
        id=UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
        timestamp="2025-07-02 20:48:45.336874",
        amount=25.30,
        currency=Currency.PLN,
        customer_id=customer_id_a,
        product_id=product_id_a,
        quantity=5,
    )


def _create_transations_batch(
    dt_gen: Generator[datetime, None, None],
    customer_id: UUID,
    product_id: UUID,
    count: int = 10,
    currency: Currency = Currency.PLN,
):
    for _ in range(count):
        Transaction.objects.create(
            id=uuid4(),
            timestamp=next(dt_gen),
            amount=12.50,
            currency=currency,
            customer_id=customer_id,
            product_id=product_id,
            quantity=8,
        )


def _datetime_gen():
    dt = datetime.fromisoformat("2025-07-03 15:03:52.593273")
    while True:
        yield dt
        dt += timedelta(seconds=10)


@pytest.fixture
def many_transactions_40(
    customer_id_a: UUID,
    customer_id_b: UUID,
    product_id_a: UUID,
    product_id_b: UUID,
    scope="session",
):

    dt_gen = _datetime_gen()

    _create_transations_batch(
        dt_gen, customer_id_a, product_id_a, currency=Currency.USD
    )
    _create_transations_batch(dt_gen, customer_id_a, product_id_b)
    _create_transations_batch(dt_gen, customer_id_b, product_id_a)
    _create_transations_batch(dt_gen, customer_id_b, product_id_b)


@pytest.fixture
def many_transactions_1k(
    customer_id_a: UUID,
    customer_id_b: UUID,
    product_id_a: UUID,
    product_id_b: UUID,
    scope="session",
):
    dt_gen = _datetime_gen()

    _create_transations_batch(dt_gen, customer_id_a, product_id_a, 50, Currency.EUR)
    _create_transations_batch(dt_gen, customer_id_a, product_id_a, 150)
    _create_transations_batch(dt_gen, customer_id_a, product_id_a, 50, Currency.USD)
    _create_transations_batch(dt_gen, customer_id_a, product_id_b, 250)
    _create_transations_batch(dt_gen, customer_id_b, product_id_a, 250)
    _create_transations_batch(dt_gen, customer_id_b, product_id_b, 250)


@pytest.fixture
def transaction_csv() -> TransactionCSV:
    csv_file_path = BASE_TEST_DIR / "files" / "test.csv"
    csv_file = File(open(csv_file_path, mode="rb"), name="test.csv")
    transaction = TransactionCSV.objects.create(file=csv_file)
    return transaction


@pytest.fixture
def csv_file() -> SimpleUploadedFile:
    csv_content = b"id,timestamp,amount,currency,customer_id,product_id,quantity\nd0466264-1384-4dc0-82d0-39e541b5c121,2025-07-02 20:48:45.336874,25.30,PLN,14245004-9354-4b77-8744-19e36372f4cd,0e64a915-9711-47f3-a640-be6f517546b1,5\nd1466264-1384-4dc0-82d0-39e541b5c121,2025-07-02 20:48:45.336874,25.30,CAD,14245004-9354-4b77-8744-19e36372f4cd,0e64a915-9711-47f3-a640-be6f517546b1,5"
    filename = "test.csv"

    csv_file = SimpleUploadedFile(
        filename,
        csv_content,
        content_type="multipart/form-data",
    )
    return csv_file
