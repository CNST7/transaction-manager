from __future__ import annotations
from abc import abstractmethod
from typing import Protocol
import uuid
from decimal import Decimal
from django.db import models
from transactionManagerProcessor.dto import TransactionDTO
from transactionManagerProcessor.enums import Currency, ProcessingStatus
from naivedatetimefield import NaiveDateTimeField
from django.core.validators import MinValueValidator


def _get_currencies():
    return ((x, x.value) for x in Currency)


def _get_csv_processing_statuses():
    return ((x, x.value) for x in ProcessingStatus)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    timestamp = NaiveDateTimeField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    currency = models.CharField(max_length=3, choices=_get_currencies)
    customer_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    product_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    quantity = models.PositiveSmallIntegerField()

    @staticmethod
    def from_dto(transaction_dto: TransactionDTO) -> Transaction:
        return Transaction(**transaction_dto.model_dump())


class TransactionCSV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.FileField(upload_to="csv_transactions_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ProcessingTracker(Protocol):
    @abstractmethod
    def register_fail(self): ...

    @abstractmethod
    def register_success(self): ...


class ProcessingStatusBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(
        max_length=15,
        choices=_get_csv_processing_statuses,
        default=ProcessingStatus.PROCESSING.value,
    )
    no_fails = models.PositiveIntegerField(default=0)
    no_successes = models.PositiveIntegerField(default=0)

    def _set_status(self, status: ProcessingStatus):
        self.status = status.value

    def set_failed(self):
        self._set_status(ProcessingStatus.FAIL)

    def set_finished(self):
        self._set_status(ProcessingStatus.SUCCESS)

    def register_fail(self):
        self.no_fails += 1

    def register_success(self):
        self.no_successes += 1

    class Meta:
        abstract = True


class CSVProcessingStatus(ProcessingStatusBase):
    transaction_csv = models.OneToOneField(TransactionCSV, on_delete=models.CASCADE)
