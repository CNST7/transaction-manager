import pytest
from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.enums import Currency
from uuid import UUID

pytestmark = pytest.mark.django_db(transaction=True)


def test_transaction():
    transaction = Transaction(
        id=UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
        timestamp="2025-07-02 20:48:45.336874",
        amount="25.30",
        currency=Currency.PLN,
        customer_id=UUID("14245004-9354-4b77-8744-19e36372f4cd"),
        product_id=UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
        quantity=5,
    )

    transaction.save()
    transaction.refresh_from_db()
    assert transaction
