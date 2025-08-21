import logging
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from functools import partial
from typing import Annotated

from django.db.models.query import QuerySet
from pydantic import BaseModel, Field, NonNegativeInt
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.utils.currency_exchange import PLN_currency_exchange
from transactionManagerProcessor.utils.qs_builder import build_qs

logger = logging.getLogger(__name__)


build_customer_summary_qs = partial(
    build_qs,
    "customer_id",
)


class CustomerSummaryOut(BaseModel):
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_products: NonNegativeInt
    last_transaction: datetime | None


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
            return Response(
                {
                    "error": f"Generating customer summary failed. {transaction.id=} unknow currency {transaction.currency=}"
                },
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
        transactions = build_customer_summary_qs(
            customer_id,
            **request.query_params,
        )

        customer_summary = prepare_customer_summary(transactions)

        return Response(customer_summary)
