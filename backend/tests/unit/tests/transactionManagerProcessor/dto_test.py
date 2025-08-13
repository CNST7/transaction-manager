import pytest
from contextlib import nullcontext as does_not_raise
from transactionManagerProcessor.dto import TransactionDTO
from transactionManagerProcessor.enums import Currency
from uuid import UUID
from pydantic import ValidationError

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

transation_data_zero_amount = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": 0,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 5,
}

transation_data_minimal_amount = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": 00.01,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 5,
}

transation_data_negative_amount = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": -3,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 5,
}

transation_data_zero_quantity = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": 25.30,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 0,
}

transation_data_negative_quantity = {
    "id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": 25.30,
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": -5,
}


@pytest.mark.parametrize(
    "transation_data,expectation",
    [
        (transation_data_ok, does_not_raise()),
        (transation_data_zero_amount, pytest.raises(ValidationError)),
        (transation_data_minimal_amount, does_not_raise()),
        (transation_data_negative_amount, pytest.raises(ValidationError)),
        (transation_data_zero_quantity, pytest.raises(ValidationError)),
        (transation_data_negative_quantity, pytest.raises(ValidationError)),
    ],
)
def test_transaction_dto(transation_data, expectation):
    with expectation:
        try:
            _ = TransactionDTO(**transation_data)
        except Exception as e:
            raise e


# TODO timestamp, currency, ids (missing/incorrect UUID)
