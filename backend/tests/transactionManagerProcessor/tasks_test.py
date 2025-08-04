from decimal import Decimal
from uuid import UUID
import pytest
from transactionManagerProcessor.tasks import process_transactions_csv
from transactionManagerProcessor.models import (
    TransactionCSV,
    CSVProcessingResult,
    Transaction,
)
from transactionManager.settings_test import BASE_TEST_DIR
from django.core.files import File
from datetime import datetime
from transactionManagerProcessor.enums import Currency

pytestmark = pytest.mark.django_db(transaction=True)


def test_process_transactions_csv():
    csv_file_path = BASE_TEST_DIR / "test_files" / "test.csv"
    csv_file = File(open(csv_file_path, mode="rb"), name="test.csv")
    saved_csv = TransactionCSV.objects.create(file=csv_file)
    assert saved_csv

    process_transactions_csv(saved_csv.id)

    csv_file_processing_result = CSVProcessingResult.objects.get(csv_file=saved_csv)

    assert csv_file_processing_result.no_fails == 1
    assert csv_file_processing_result.no_sucesses == 3

    transaction = Transaction.objects.get(id="d0466264-1384-4dc0-82d0-39e541b5c121")
    assert transaction.timestamp == datetime.fromisoformat("2025-07-02 20:48:45.336874")
    assert transaction.amount == Decimal("25.30")
    assert transaction.currency == Currency.PLN
    assert transaction.customer_id == UUID("14245004-9354-4b77-8744-19e36372f4cd")
    assert transaction.product_id == UUID("0e64a915-9711-47f3-a640-be6f517546b1")
    assert transaction.quantity == 5
