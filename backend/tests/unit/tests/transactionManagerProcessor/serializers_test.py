from contextlib import nullcontext as does_not_raise
from uuid import UUID

import pytest
from rest_framework.serializers import ValidationError
from transactionManagerProcessor.enums import Currency
from transactionManagerProcessor.serializers import TransactionSerializer

pytestmark = pytest.mark.django_db(transaction=True)

transation_data_ok = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": 25.30,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 5,
}

transation_data_zero_amount = transation_data_ok.copy()
transation_data_zero_amount.update({"amount": 0})

transation_data_minimal_amount = transation_data_ok.copy()
transation_data_minimal_amount.update({"amount": 00.01})

transation_data_negative_amount = transation_data_ok.copy()
transation_data_negative_amount.update({"amount": -3})

transation_data_zero_quantity = transation_data_ok.copy()
transation_data_zero_quantity.update({"quantity": 0})

transation_data_minimal_quantity = transation_data_ok.copy()
transation_data_minimal_quantity.update({"quantity": 1})

transation_data_negative_quantity = transation_data_ok.copy()
transation_data_negative_quantity.update({"quantity": -5})


testdata = [
    (transation_data_ok, does_not_raise()),
    (transation_data_zero_amount, pytest.raises(ValidationError)),
    (transation_data_minimal_amount, does_not_raise()),
    (transation_data_negative_amount, pytest.raises(ValidationError)),
    (transation_data_zero_quantity, pytest.raises(ValidationError)),
    (transation_data_minimal_quantity, does_not_raise()),
    (transation_data_negative_quantity, pytest.raises(ValidationError)),
]

testdata_ids = [
    "transation_data_ok",
    "transation_data_zero_amount",
    "transation_data_minimal_amount",
    "transation_data_negative_amount",
    "transation_data_zero_quantity",
    "transation_data_minimal_quantity",
    "transation_data_negative_quantity",
]


@pytest.mark.parametrize(
    "transation_data,expectation",
    testdata,
    ids=testdata_ids,
)
def test_transaction_serializer_is_valid(transation_data, expectation):
    with expectation:
        try:
            serializer = TransactionSerializer(data=transation_data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise e
