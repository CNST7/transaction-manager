import logging
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
from transactionManagerProcessor.utils.currency_exchange import (
    PLN_currency_exchange,
)
from transactionManagerProcessor.utils.qs_builder import build_qs

logger = logging.getLogger(__name__)


build_product_summary_qs = partial(
    build_qs,
    "product_id",
)


class ProductSummaryOut(BaseModel):
    total_quantity: NonNegativeInt
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_customers: NonNegativeInt


def prepare_product_summary(
    transactions: QuerySet[Transaction],
) -> ProductSummaryOut:
    total_quantity = 0
    total_amount = Decimal(0)
    unique_customers = set()

    for transaction in transactions:
        total_quantity += transaction.quantity
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
        unique_customers.add(transaction.customer_id)

    total_amount = total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    product_summary = ProductSummaryOut(
        total_quantity=total_quantity,
        total_amount=total_amount,
        unique_customers=len(unique_customers),
    )

    return product_summary.model_dump(mode="json")


class ProductSummaryEndpoint(APIView):
    def get(self, request: Request, product_id=None):
        transactions = build_product_summary_qs(
            product_id,
            **request.query_params,
        )

        product_summary = prepare_product_summary(transactions)

        return Response(product_summary)
