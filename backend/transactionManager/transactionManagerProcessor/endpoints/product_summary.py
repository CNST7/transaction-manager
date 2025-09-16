import logging
from decimal import Decimal
from typing import Annotated, TypedDict

from django.db.models import Count, F, Sum
from django.db.models.query import QuerySet
from pydantic import BaseModel, Field, NonNegativeInt
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


class ProductSummaryOut(BaseModel):
    total_quantity: NonNegativeInt
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_customers: NonNegativeInt


class ProductSummaryPerCurrency(TypedDict):
    currency: str
    total: Decimal


def prepare_product_summary(
    transactions: QuerySet[Transaction],
    currency_exchange_processor: ExchangeProcessor,
) -> ProductSummaryOut:
    total_quantity = (
        transactions.values("product_id")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("product_id")
        .first()
        .get("total_quantity")
    )

    _total_amount_by_currency: QuerySet[ProductSummaryPerCurrency] = (
        transactions.annotate(total=Sum(F("amount") * F("quantity"))).values(
            "currency", "total"
        )
    )
    total_amount: Decimal = sum(
        x["total"] * currency_exchange_processor.get_exchange_rate(x["currency"])
        for x in _total_amount_by_currency
    )

    unique_customers = transactions.aggregate(
        count=Count("customer_id", distinct=True)
    )["count"]

    product_summary = ProductSummaryOut(
        total_quantity=total_quantity,
        total_amount=total_amount,
        unique_customers=unique_customers,
    )

    return product_summary.model_dump(mode="json")


class ProductSummaryEndpoint(APIView):
    def get(self, request: Request, product_id: str = None):
        transactions = (
            TransactionQuerySetPartialDirector.product_summary_queryset()
            .with_filter_value(product_id)
            .with_query_params(**request.query_params)
            .build()
        )

        currency_processor = ExchangeFactory.prepare_strategy(request.query_params)

        product_summary = prepare_product_summary(transactions, currency_processor)

        return Response(product_summary)
