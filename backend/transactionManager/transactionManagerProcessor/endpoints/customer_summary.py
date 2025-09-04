import logging
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from django.db.models.query import QuerySet
from pydantic import BaseModel, Field, NonNegativeInt, field_serializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.utils.currency_exchange import PLN_currency_exchange
from transactionManagerProcessor.utils.queryset_builder import (
    TransactionQuerySetPartialDirector,
)

logger = logging.getLogger(__name__)


class CustomerSummaryOut(BaseModel):
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_products: NonNegativeInt
    last_transaction: datetime | None

    @field_serializer("last_transaction")
    def serialize_created_at(self, value: datetime, _info):
        return value.strftime("%Y-%m-%d %H:%M:%S")


def prepare_customer_summary(
    transactions: QuerySet[Transaction],
) -> CustomerSummaryOut:
    last_transaction: datetime | None = None
    unique_products = set()
    total_amount = Decimal(0)

    for transaction in transactions:
        try:
            total_amount += (
                transaction.amount
                * transaction.quantity
                * PLN_currency_exchange[transaction.currency]
            )
        except KeyError:
            error_message = f"Generating product summary failed. \
                Unknow currency={transaction.currency} \
                in transaction_id={transaction.transaction_id}"
            logger.critical(error_message, exc_info=True)
            return Response(
                {"error": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if last_transaction is None:
            last_transaction = transaction.timestamp
        elif transaction.timestamp > last_transaction:
            last_transaction = transaction.timestamp

        unique_products.add(transaction.product_id)

    total_amount = total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    customer_summary = CustomerSummaryOut(
        total_amount=total_amount,
        last_transaction=last_transaction,
        unique_products=len(unique_products),
    )

    return customer_summary.model_dump(mode="json")


class CustomerSummaryEndpoint(APIView):
    def get(self, request: Request, customer_id=None):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(customer_id)
            .with_query_params(**request.query_params)
            .build()
        )

        customer_summary = prepare_customer_summary(transactions)

        return Response(customer_summary)
