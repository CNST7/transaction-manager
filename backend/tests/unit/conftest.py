from collections.abc import Generator
from datetime import datetime, timedelta
from pathlib import PosixPath
from uuid import UUID

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from transactionManager.settings_test import BASE_TEST_DIR
from transactionManagerProcessor.enums import Currency
from transactionManagerProcessor.models import (
    Transaction,
    TransactionCSV,
)

pytestmark = pytest.mark.django_db()


@pytest.fixture(autouse=True)
def temp_media_root(tmp_path: PosixPath, settings):
    temp_dir = tmp_path / "media"
    temp_dir.mkdir()
    settings.MEDIA_ROOT = str(temp_dir)
    yield


@pytest.fixture
def product_id_a(scope="session") -> UUID:
    return UUID("985e4402-5d1e-404b-8254-968070a3c7c7")


@pytest.fixture
def product_id_b(scope="session") -> UUID:
    return UUID("170cc51f-8755-4a6e-9c76-1992782902dc")


@pytest.fixture
def product_id_c(scope="session") -> UUID:
    return UUID("fe350cba-4f9c-4b98-8bda-2bda7c7f310c")


@pytest.fixture
def customer_id_a(scope="session") -> UUID:
    return UUID("51f53702-b492-47be-b20d-80b6852368dd")


@pytest.fixture
def customer_id_b(scope="session") -> UUID:
    return UUID("a036e9d1-d475-4f80-a106-160df1fc2882")


@pytest.fixture
def customer_id_c(scope="session") -> UUID:
    return UUID("2a6efd2d-702e-41d7-b303-8bca7c87617c")


@pytest.fixture
def qs_builder_transactions(
    customer_id_a: UUID, product_id_a: UUID, scope="session"
) -> list[Transaction]:
    date_early = datetime(2025, 7, 2)
    date_earliest = date_early - timedelta(microseconds=1)
    date_middle = datetime(2025, 7, 25)
    date_latest = datetime(2025, 8, 2)
    date_later = date_latest - timedelta(microseconds=1)

    return [
        Transaction.objects.create(
            transaction_id=UUID("f00a9313-4eaf-4e15-9b85-2802a5213764"),
            timestamp=date_earliest,
            amount=10.00,
            currency=Currency.PLN,
            customer_id=customer_id_a,
            product_id=product_id_a,
            quantity=10,
        ),
        Transaction.objects.create(
            transaction_id=UUID("d2993a99-3358-41af-8047-070fa648d079"),
            timestamp=date_early,
            amount=10.00,
            currency=Currency.PLN,
            customer_id=customer_id_a,
            product_id=product_id_a,
            quantity=10,
        ),
        Transaction.objects.create(
            transaction_id=UUID("ddaf9b82-1bf5-44b5-89ff-45816857403b"),
            timestamp=date_middle,
            amount=20.50,
            currency=Currency.PLN,
            customer_id=customer_id_a,
            product_id=product_id_a,
            quantity=1,
        ),
        Transaction.objects.create(
            transaction_id=UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
            timestamp=date_later,
            amount=25.30,
            currency=Currency.PLN,
            customer_id=customer_id_a,
            product_id=product_id_a,
            quantity=5,
        ),
        Transaction.objects.create(
            transaction_id=UUID("b2f4b977-c0de-409c-ae9b-39b806f3f309"),
            timestamp=date_latest,
            amount=25.30,
            currency=Currency.PLN,
            customer_id=customer_id_a,
            product_id=product_id_a,
            quantity=5,
        ),
    ]


@pytest.fixture
def customer_summary_transactions(
    customer_id_a: UUID,
    customer_id_b: UUID,
    product_id_a: UUID,
    product_id_b: UUID,
    product_id_c: UUID,
    scope="session",
) -> list[Transaction]:
    base_transaction_data = {
        "amount": 10.00,
        "customer_id": customer_id_a,
        "product_id": product_id_a,
        "quantity": 10,
    }

    test_case_transaction_data = [
        {
            **base_transaction_data,
            "transaction_id": UUID("1fb17aed-9480-420e-aeb2-6908462ac7c0"),
            "currency": Currency.PLN,
            "timestamp": "2025-08-01 10:00:00.000000",
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("f895f44a-73f7-45dc-b84a-561d57d6a1df"),
            "currency": Currency.EUR,
            "timestamp": "2025-08-02 10:00:00.000000",
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("4b88b84d-84b2-4d1c-96ec-533b0b691d7d"),
            "currency": Currency.USD,
            "timestamp": "2025-08-03 10:00:00.000000",
            "product_id": product_id_b,
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("dd171bff-eb14-42d1-aee5-d44fdf1277dd"),
            "currency": Currency.USD,
            "timestamp": "2025-08-04 10:00:00.000000",
            "customer_id": customer_id_b,
            "product_id": product_id_c,
        },
    ]

    return [
        Transaction.objects.create(**transaction)
        for transaction in test_case_transaction_data
    ]


@pytest.fixture
def product_summary_transactions(
    customer_id_a: UUID,
    customer_id_b: UUID,
    customer_id_c: UUID,
    product_id_a: UUID,
    product_id_b: UUID,
    scope="session",
) -> list[Transaction]:
    base_transaction_data = {
        "amount": 10.00,
        "customer_id": customer_id_a,
        "product_id": product_id_a,
        "quantity": 10,
    }

    test_case_transaction_data = [
        {
            **base_transaction_data,
            "transaction_id": UUID("9a78f23c-b7e1-495c-8f01-47a4e669959b"),
            "currency": Currency.PLN,
            "timestamp": "2025-08-01 10:00:00.000000",
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("bfe4cf74-6128-42cc-b819-2bcbbb4942ed"),
            "currency": Currency.EUR,
            "timestamp": "2025-08-02 10:00:00.000000",
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("94503da6-0fd7-4eb1-9bd1-40be6384c2b8"),
            "currency": Currency.USD,
            "timestamp": "2025-08-03 10:00:00.000000",
            "customer_id": customer_id_b,
        },
        {
            **base_transaction_data,
            "transaction_id": UUID("7c813364-a746-4609-960e-c112afb5448f"),
            "currency": Currency.USD,
            "timestamp": "2025-08-04 10:00:00.000000",
            "product_id": product_id_b,
            "customer_id": customer_id_c,
        },
    ]

    return [
        Transaction.objects.create(**transaction)
        for transaction in test_case_transaction_data
    ]


def _datetime_generator() -> Generator[datetime]:
    dt = datetime.fromisoformat("2025-07-03 15:03:52.593273")
    while True:
        yield dt
        dt += timedelta(seconds=10)


@pytest.fixture
def create_1000_transactions(
    customer_id_a: UUID,
    customer_id_b: UUID,
    product_id_a: UUID,
    product_id_b: UUID,
    scope="session",
):
    dt_gen = _datetime_generator()

    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=50,
        customer_id=customer_id_a,
        product_id=product_id_a,
        currency=Currency.EUR,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )
    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=50,
        customer_id=customer_id_a,
        product_id=product_id_a,
        currency=Currency.USD,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )
    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=150,
        customer_id=customer_id_a,
        product_id=product_id_a,
        currency=Currency.PLN,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )
    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=250,
        customer_id=customer_id_a,
        product_id=product_id_b,
        currency=Currency.PLN,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )
    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=250,
        customer_id=customer_id_b,
        product_id=product_id_a,
        currency=Currency.PLN,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )
    baker.make(
        "transactionManagerProcessor.Transaction",
        _quantity=250,
        customer_id=customer_id_b,
        product_id=product_id_b,
        currency=Currency.PLN,
        timestamp=dt_gen,
        amount=12.50,
        quantity=8,
    )


@pytest.fixture
def transaction_csv() -> TransactionCSV:
    csv_file_path = BASE_TEST_DIR / "unit" / "fixtures" / "test.csv"
    csv_file = File(open(csv_file_path, mode="rb"), name="test.csv")
    transaction = TransactionCSV.objects.create(file=csv_file)
    return transaction


@pytest.fixture
def csv_file() -> SimpleUploadedFile:
    csv_content = b"transaction_id,timestamp,amount,currency,customer_id,product_id,quantity\nd0466264-1384-4dc0-82d0-39e541b5c121,2025-07-02 20:48:45.336874,25.30,PLN,14245004-9354-4b77-8744-19e36372f4cd,0e64a915-9711-47f3-a640-be6f517546b1,5\nd1466264-1384-4dc0-82d0-39e541b5c121,2025-07-02 20:48:45.336874,25.30,CAD,14245004-9354-4b77-8744-19e36372f4cd,0e64a915-9711-47f3-a640-be6f517546b1,5"
    filename = "test.csv"

    csv_file = SimpleUploadedFile(
        filename,
        csv_content,
        content_type="multipart/form-data",
    )
    return csv_file
