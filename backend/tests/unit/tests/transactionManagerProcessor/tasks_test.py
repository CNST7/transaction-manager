from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest
from transactionManagerProcessor.enums import Currency, ProcessingStatus
from transactionManagerProcessor.models import (
    CSVProcessingStatus,
    Transaction,
    TransactionCSV,
)
from transactionManagerProcessor.tasks import (
    CSVProcessingStatusManager,
    process_transaction_csv,
)

pytestmark = pytest.mark.django_db(transaction=True)


class Test_ProcessTransactionsCSV:
    def test_process_transactions_csv__processing_status(
        self, transaction_csv: TransactionCSV
    ):
        process_transaction_csv(transaction_csv.id)

        csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )

        assert csv_processing_status.no_fails == 1
        assert csv_processing_status.no_successes == 3

    def test_process_transactions_csv__transaction_created(
        self, transaction_csv: TransactionCSV
    ):
        process_transaction_csv(transaction_csv.id)

        transaction = Transaction.objects.get(
            transaction_id="d0466264-1384-4dc0-82d0-39e541b5c121"
        )
        assert transaction.timestamp == datetime.fromisoformat(
            "2025-07-02 20:48:45.336874+00:00"
        )
        assert transaction.amount == Decimal("25.30")
        assert transaction.currency == Currency.PLN
        assert transaction.customer_id == UUID("14245004-9354-4b77-8744-19e36372f4cd")
        assert transaction.product_id == UUID("0e64a915-9711-47f3-a640-be6f517546b1")
        assert transaction.quantity == 5


class Test_CSVProcessingStatusManager:
    def test_csv_processing_status_manager__sets_finished_status_on_successful_exit(
        self,
        transaction_csv: TransactionCSV,
    ):
        with CSVProcessingStatusManager(transaction_csv):
            ...

        csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )
        assert csv_processing_status.status == ProcessingStatus.SUCCESS

    def test_csv_processing_status_manager__sets_failed_status_on_error_exit(
        self,
        transaction_csv: TransactionCSV,
    ):
        with CSVProcessingStatusManager(transaction_csv):
            raise Exception()

        csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )
        assert csv_processing_status.status == ProcessingStatus.FAIL

    def test_csv_processing_status_manager__counts_successes(
        self,
        transaction_csv: TransactionCSV,
    ):
        with CSVProcessingStatusManager(transaction_csv) as processing_tracker:
            processing_tracker.register_success()
            processing_tracker.register_success()
            processing_tracker.register_success()

        csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )
        assert csv_processing_status.status == ProcessingStatus.SUCCESS
        assert csv_processing_status.no_successes == 3

    def test_csv_processing_status_manager__counts_failures(
        self,
        transaction_csv: TransactionCSV,
    ):
        with CSVProcessingStatusManager(transaction_csv) as processing_tracker:
            processing_tracker.register_fail()
            processing_tracker.register_fail()
            processing_tracker.register_fail()

        csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )
        assert csv_processing_status.status == ProcessingStatus.SUCCESS
        assert csv_processing_status.no_fails == 3
