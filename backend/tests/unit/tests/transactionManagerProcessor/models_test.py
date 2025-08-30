import pytest
from transactionManagerProcessor.models import Transaction

from backend.tests.unit.fixtures.transactions_testdata import (
    test_data,
    test_names,
)

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize(
    "transaction_data,expectation",
    test_data,
    ids=test_names,
)
def test_transaction_model_save(transaction_data, expectation):
    with expectation:
        transaction = Transaction(**transaction_data)
        transaction.save()
