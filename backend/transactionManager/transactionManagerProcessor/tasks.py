import csv
import logging
from abc import ABC, abstractmethod

from celery import shared_task
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError

from transactionManagerProcessor.models import (
    CSVProcessingStatus,
    ProcessingTracker,
    TransactionCSV,
)
from transactionManagerProcessor.serializers import TransactionSerializer

logger = logging.getLogger(__name__)


@shared_task()
def process_transaction_csv(transaction_csv_id: str):
    try:
        transaction_csv = TransactionCSV.objects.get(id=transaction_csv_id)
    except TransactionCSV.DoesNotExist():
        logger.error(
            f"Failed to process {transaction_csv_id}, file does not exist in database."
        )
        return

    with (
        CSVProcessingStatusManager(transaction_csv) as status_tracker,
        open(transaction_csv.file.path, encoding="utf-8") as csvfile,
    ):
        dict_reader = csv.DictReader(csvfile)
        for transaction_data in dict_reader:
            _process_transaction(transaction_data, status_tracker)


def _process_transaction(
    transaction_data: dict[str, any],
    status_tracker: ProcessingTracker,
):
    try:
        try:
            serializer = TransactionSerializer(data=transaction_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.debug(f"PROCESSED DATA: {transaction_data}")
        except Exception:
            status_tracker.register_fail()
            raise
    except ValidationError:
        logger.error(f"FAILED DATA: {transaction_data}")
    except IntegrityError:
        logger.error(f"TRANSACTION ALREADY EXIST {transaction_data}")
    except Exception:
        logger.error(
            f"FAILED TO CREATE TRANSACTION, UNHANDLED ERROR {transaction_data}"
        )
    else:
        status_tracker.register_success()


class ProcessingStatusManager(ABC):
    @abstractmethod
    def __enter__(self) -> ProcessingTracker: ...

    @abstractmethod
    def __exit__(self, type, value, traceback) -> bool: ...


class CSVProcessingStatusManager(ProcessingStatusManager):
    def __init__(self, transaction_csv: TransactionCSV):
        self._csv_processing_status = CSVProcessingStatus.objects.get(
            transaction_csv=transaction_csv
        )

    def __enter__(self) -> ProcessingTracker:
        return self._csv_processing_status

    def __exit__(self, type, value, traceback) -> bool:
        if value:
            self._csv_processing_status.set_failed()
        else:
            self._csv_processing_status.set_finished()
        self._csv_processing_status.save()
        return True
