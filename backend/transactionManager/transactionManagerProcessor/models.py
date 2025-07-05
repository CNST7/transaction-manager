from __future__ import annotations
import uuid
from decimal import Decimal
from django.db import models
from transactionManagerProcessor.dto import TransactionDTO
from transactionManagerProcessor.enums import Currency
from naivedatetimefield import NaiveDateTimeField
from django.core.validators import MinValueValidator


def _get_currencies():
    return ((x, x.value) for x in Currency)


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
