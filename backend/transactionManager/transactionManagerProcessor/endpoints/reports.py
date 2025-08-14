from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from transactionManagerProcessor.enums import Currency
from transactionManagerProcessor.models import Transaction
from rest_framework.views import APIView
from pydantic import BaseModel, NonNegativeInt, Field
from typing import Annotated
from enum import Enum

_ValidType = Enum("_ValidType", "VALID")
_VALID = _ValidType.VALID


def _validate_uuid(value: str, label: str) -> Response | _ValidType:
    if not value:
        return Response(
            {"error": f"Missing {label} in path."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        value = UUID(value)
    except ValueError as e:
        return Response(
            {"error": f"Incorrect {label}. Must be valid UUID"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return _VALID


_currency_exchange_to_PLN: dict[Currency, Decimal] = {
    Currency.PLN: Decimal("1.00"),
    Currency.EUR: Decimal("4.30"),
    Currency.USD: Decimal("4.00"),
}


class CustomerSummary(BaseModel):
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_products: NonNegativeInt
    last_transaction: datetime | None


class CustomerSummaryEndpoint(APIView):
    def get(self, request: Request, customer_id=None):
        validation_result = _validate_uuid(customer_id, "customer_id")
        if validation_result is not _VALID:
            return validation_result

        transactions = Transaction.objects.filter(customer_id=customer_id)

        last_transaction: datetime | None = None
        unique_products = set()
        total_amount = Decimal(0)

        for transaction in transactions:

            try:
                total_amount += (
                    transaction.amount
                    * transaction.quantity
                    * _currency_exchange_to_PLN[transaction.currency]
                )
            except KeyError as e:
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
        customer_summary = CustomerSummary(
            total_amount=total_amount,
            last_transaction=last_transaction,
            unique_products=len(unique_products),
        )

        return Response(
            customer_summary.model_dump(mode="json"),
            status=status.HTTP_200_OK,
        )


class ProductSummary(BaseModel):
    total_quantity: NonNegativeInt
    total_amount: Annotated[Decimal, Field(ge=0, max_digits=20, decimal_places=2)]
    unique_customers: NonNegativeInt


class ProductSummaryEndpoint(APIView):
    def get(self, request: Request, product_id=None):
        validation_result = _validate_uuid(product_id, "product_id")
        if validation_result is not _VALID:
            return validation_result

        transactions = Transaction.objects.filter(product_id=product_id)

        total_quantity = 0
        total_amount = Decimal(0)
        unique_customers = set()

        for transaction in transactions:
            total_quantity += transaction.quantity
            try:
                total_amount += (
                    transaction.amount
                    * transaction.quantity
                    * _currency_exchange_to_PLN[transaction.currency]
                )
            except KeyError as e:
                return Response(
                    {
                        "error": f"Generating product summary failed. {transaction.id=} unknow currency {transaction.currency=}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            unique_customers.add(transaction.customer_id)

        total_amount = total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        product_summary = ProductSummary(
            total_quantity=total_quantity,
            total_amount=total_amount,
            unique_customers=len(unique_customers),
        )

        return Response(
            product_summary.model_dump(mode="json"),
            status=status.HTTP_200_OK,
        )
