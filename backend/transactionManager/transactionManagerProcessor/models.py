from __future__ import annotations

import uuid
from abc import abstractmethod
from decimal import Decimal
from typing import Protocol

from django.core.validators import MinValueValidator
from django.db import IntegrityError, models
from django.db.models import CheckConstraint, Q

from transactionManagerProcessor.enums import Currency, ProcessingStatus


def _get_currencies():
    return ((x, x.value) for x in Currency)


def _get_csv_processing_statuses():
    return ((x, x.value) for x in ProcessingStatus)


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True)
    timestamp = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    currency = models.CharField(max_length=3, choices=_get_currencies)
    customer_id = models.UUIDField(db_index=True)
    product_id = models.UUIDField(db_index=True)
    quantity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(amount__gte=Decimal("0.01")), name="amount_gte_0_01"
            ),
            CheckConstraint(condition=Q(quantity__gte=1), name="quantity_gte_1"),
        ]

    def save(self, **kwargs):
        self._validate_quantity()
        self._validate_currency()
        super().save(**kwargs)

    def _validate_currency(self):
        if self.currency not in (c.name for c in Currency):
            raise IntegrityError({"currency": "Must be a valid Currency"})

    def _validate_quantity(self):
        if isinstance(self.quantity, str) and self.quantity.isdigit():
            self.quantity = int(self.quantity)
            return
        if not isinstance(self.quantity, int):
            raise IntegrityError({"quantity": "Quantity must be an integer."})


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
