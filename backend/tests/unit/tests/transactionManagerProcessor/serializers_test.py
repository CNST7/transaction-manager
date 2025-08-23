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

transation_data_incorrect_id = {**transation_data_ok, **{"id": "asdf"}}
transation_data_missing_product_id = {**transation_data_ok}
del transation_data_missing_product_id["id"]

transation_data_incorrect_timestamp = {
    **transation_data_ok,
    **{"timestamp": "02-07-2025 20:48:45.336874"},
}
transation_data_timezone_timestamp = {
    **transation_data_ok,
    **{"timestamp": "2025-07-02 20:48:45.336874+02:00"},
}
transation_data_missing_timestamp = {**transation_data_ok}
del transation_data_missing_timestamp["timestamp"]

transation_data_zero_amount = {**transation_data_ok, **{"amount": 0}}
transation_data_minimal_amount = {**transation_data_ok, **{"amount": 00.01}}
transation_data_negative_amount = {**transation_data_ok, **{"amount": -3}}
transation_data_missing_amount = {**transation_data_ok}
del transation_data_missing_amount["amount"]

transation_data_PLN_currency = {**transation_data_ok, **{"currency": "PLN"}}
transation_data_USD_currency = {**transation_data_ok, **{"currency": "USD"}}
transation_data_EUR_currency = {**transation_data_ok, **{"currency": "EUR"}}
transation_data_incorrect_currency = {**transation_data_ok, **{"currency": "AAA"}}
transation_data_missing_currency = {**transation_data_ok}
del transation_data_missing_currency["currency"]

transation_data_incorrect_customer_id = {**transation_data_ok, **{"id": "asdf"}}
transation_data_missing_customer_id = {**transation_data_ok}
del transation_data_missing_customer_id["id"]

transation_data_incorrect_product_id = {**transation_data_ok, **{"id": "asdf"}}
transation_data_missing_product_id = {**transation_data_ok}
del transation_data_missing_product_id["id"]

transation_data_zero_quantity = {**transation_data_ok, **{"quantity": 0}}
transation_data_minimal_quantity = {**transation_data_ok, **{"quantity": 1}}
transation_data_negative_quantity = {**transation_data_ok, **{"quantity": -5}}
transation_data_missing_quantity = {**transation_data_ok}
del transation_data_missing_quantity["quantity"]


testdata = [
    (transation_data_ok, does_not_raise()),
    (transation_data_incorrect_id, pytest.raises(ValidationError)),
    (transation_data_missing_product_id, pytest.raises(ValidationError)),
    (transation_data_incorrect_timestamp, pytest.raises(ValidationError)),
    (transation_data_timezone_timestamp, does_not_raise()),
    (transation_data_missing_timestamp, pytest.raises(ValidationError)),
    (transation_data_zero_amount, pytest.raises(ValidationError)),
    (transation_data_minimal_amount, does_not_raise()),
    (transation_data_negative_amount, pytest.raises(ValidationError)),
    (transation_data_missing_amount, pytest.raises(ValidationError)),
    (transation_data_PLN_currency, does_not_raise()),
    (transation_data_USD_currency, does_not_raise()),
    (transation_data_EUR_currency, does_not_raise()),
    (transation_data_incorrect_currency, pytest.raises(ValidationError)),
    (transation_data_missing_currency, pytest.raises(ValidationError)),
    (transation_data_incorrect_customer_id, pytest.raises(ValidationError)),
    (transation_data_missing_customer_id, pytest.raises(ValidationError)),
    (transation_data_incorrect_product_id, pytest.raises(ValidationError)),
    (transation_data_missing_product_id, pytest.raises(ValidationError)),
    (transation_data_zero_quantity, pytest.raises(ValidationError)),
    (transation_data_minimal_quantity, does_not_raise()),
    (transation_data_negative_quantity, pytest.raises(ValidationError)),
    (transation_data_missing_quantity, pytest.raises(ValidationError)),
]

testdata_ids = [
    "transation_data_ok",
    "transation_data_incorrect_id",
    "transation_data_missing_id",
    "transation_data_incorrect_timestamp",
    "transation_data_timezone_timestamp",
    "transation_data_missing_timestamp",
    "transation_data_zero_amount",
    "transation_data_minimal_amount",
    "transation_data_negative_amount",
    "transation_data_missing_amount",
    "transation_data_PLN_currency",
    "transation_data_USD_currency",
    "transation_data_EUR_currency",
    "transation_data_incorrect_currency",
    "transation_data_missing_currency",
    "transation_data_zero_quantity",
    "transation_data_minimal_quantity",
    "transation_data_negative_quantity",
    "transation_data_missing_quantity",
    "transation_data_incorrect_customer_id",
    "transation_data_missing_customer_id",
    "transation_data_incorrect_product_id",
    "transation_data_missing_product_id",
]


@pytest.mark.parametrize(
    "transation_data,expectation",
    testdata,
    ids=testdata_ids,
)
def test_transaction_serializer_is_valid(transation_data, expectation):
    with expectation:
        serializer = TransactionSerializer(data=transation_data)
        serializer.is_valid(raise_exception=True)
