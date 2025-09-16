import logging
from datetime import datetime
from decimal import Decimal
from typing import Annotated, TypedDict

from django.db.models import Count, F, Sum
from django.db.models.query import QuerySet
from pydantic import BaseModel, Field, NonNegativeInt, field_serializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.utils.currency import (
    ExchangeFactory,
    ExchangeProcessor,
)
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


class CustomerSummaryPerCurrency(TypedDict):
    currency: str
    total: Decimal


def prepare_customer_summary(
    transactions: QuerySet[Transaction],
    currency_exchange_processor: ExchangeProcessor,
) -> CustomerSummaryOut:
    transactions = transactions.order_by("-timestamp")
    last_transaction = transactions.first().timestamp

    _total_amount_by_currency: QuerySet[CustomerSummaryPerCurrency] = (
        transactions.annotate(total=Sum(F("amount") * F("quantity"))).values(
            "currency", "total"
        )
    )
    total_amount: Decimal = sum(
        x["total"] * currency_exchange_processor.get_exchange_rate(x["currency"])
        for x in _total_amount_by_currency
    )

    unique_products = transactions.aggregate(count=Count("product_id", distinct=True))[
        "count"
    ]

    customer_summary = CustomerSummaryOut(
        total_amount=total_amount,
        last_transaction=last_transaction,
        unique_products=unique_products,
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

        currency_processor = ExchangeFactory.prepare_strategy(request.query_params)

        customer_summary = prepare_customer_summary(transactions, currency_processor)

        return Response(customer_summary)
