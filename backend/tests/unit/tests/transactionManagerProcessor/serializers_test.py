import pytest
from transactionManagerProcessor.serializers import TransactionSerializer

from backend.tests.unit.fixtures.serializers.transactions_testdata import (
    test_data,
    test_names,
)

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize(
    "transaction_data,expectation",
    test_data,
    ids=test_names,
)
def test_transaction_serializer_is_valid(transaction_data, expectation):
    with expectation:
        serializer = TransactionSerializer(data=transaction_data)
        serializer.is_valid(raise_exception=True)
