from contextlib import nullcontext as does_not_raise
from decimal import Decimal
from uuid import UUID

import pytest
from transactionManagerProcessor.enums import Currency

transaction_data_ok = {
    "transaction_id": UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
    "timestamp": "2025-07-02 20:48:45.336874",
    "amount": Decimal("25.30"),
    "currency": Currency.PLN,
    "customer_id": UUID("14245004-9354-4b77-8744-19e36372f4cd"),
    "product_id": UUID("0e64a915-9711-47f3-a640-be6f517546b1"),
    "quantity": 5,
}

transaction_data_incorrect_transaction_id = {
    **transaction_data_ok,
    **{"transaction_id": "asdf"},
}
transaction_data_missing_transaction_id = {**transaction_data_ok}
del transaction_data_missing_transaction_id["transaction_id"]

transaction_data_incorrect_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "02-07-2025 20:48:45.336874"},
}
transaction_data_timezone_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02 20:48:45.336874+02:00"},
}
transaction_data_timezone_T_delimiter_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02T20:48:45.336874+02:00"},
}
transaction_data_timezone_Z_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02T20:48:45.336874Z"},
}
transaction_data_no_miliseconds_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02T20:48:45"},
}
transaction_data_timezone_offset_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02T20:48:45+0530"},
}
transaction_data_no_time_timestamp = {
    **transaction_data_ok,
    **{"timestamp": "2025-07-02"},
}
transaction_data_missing_timestamp = {**transaction_data_ok}
del transaction_data_missing_timestamp["timestamp"]

transaction_data_zero_amount = {**transaction_data_ok, **{"amount": Decimal("0")}}
transaction_data_minimal_amount = {
    **transaction_data_ok,
    **{"amount": Decimal("00.01")},
}
transaction_data_negative_amount = {**transaction_data_ok, **{"amount": Decimal("-3")}}
transaction_data_missing_amount = {**transaction_data_ok}
del transaction_data_missing_amount["amount"]

transaction_data_PLN_currency = {**transaction_data_ok, **{"currency": "PLN"}}
transaction_data_USD_currency = {**transaction_data_ok, **{"currency": "USD"}}
transaction_data_EUR_currency = {**transaction_data_ok, **{"currency": "EUR"}}
transaction_data_incorrect_currency = {**transaction_data_ok, **{"currency": "AAA"}}
transaction_data_missing_currency = {**transaction_data_ok}
del transaction_data_missing_currency["currency"]

transaction_data_incorrect_customer_id = {
    **transaction_data_ok,
    **{"customer_id": "asdf"},
}
transaction_data_missing_customer_id = {**transaction_data_ok}
del transaction_data_missing_customer_id["customer_id"]

transaction_data_incorrect_product_id = {
    **transaction_data_ok,
    **{"product_id": "asdf"},
}
transaction_data_missing_product_id = {**transaction_data_ok}
del transaction_data_missing_product_id["product_id"]

transaction_data_zero_quantity = {**transaction_data_ok, **{"quantity": 0}}
transaction_data_minimal_quantity = {**transaction_data_ok, **{"quantity": 1}}
transaction_data_negative_quantity = {**transaction_data_ok, **{"quantity": -5}}
transaction_data_floating_point_quantity = {**transaction_data_ok, **{"quantity": 1.5}}
transaction_data_correct_string_quantity = {**transaction_data_ok, **{"quantity": "5"}}
transaction_data_floating_point_string_quantity = {
    **transaction_data_ok,
    **{"quantity": "5.2"},
}
transaction_data_incorrect_string_quantity = {
    **transaction_data_ok,
    **{"quantity": "abc"},
}
transaction_data_missing_quantity = {**transaction_data_ok}
del transaction_data_missing_quantity["quantity"]

test_cases = {
    "transaction_data_ok": (
        transaction_data_ok,
        does_not_raise(),
    ),
    "transaction_data_incorrect_transaction_id": (
        transaction_data_incorrect_transaction_id,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_transaction_id": (
        transaction_data_missing_transaction_id,
        pytest.raises(Exception),
    ),
    "transaction_data_incorrect_timestamp": (
        transaction_data_incorrect_timestamp,
        pytest.raises(Exception),
    ),
    "transaction_data_timezone_timestamp": (
        transaction_data_timezone_timestamp,
        does_not_raise(),
    ),
    "transaction_data_timezone_T_delimiter_timestamp": (
        transaction_data_timezone_T_delimiter_timestamp,
        does_not_raise(),
    ),
    "transaction_data_timezone_Z_timestamp": (
        transaction_data_timezone_Z_timestamp,
        does_not_raise(),
    ),
    "transaction_data_no_miliseconds_timestamp": (
        transaction_data_no_miliseconds_timestamp,
        does_not_raise(),
    ),
    "transaction_data_timezone_offset_timestamp": (
        transaction_data_timezone_offset_timestamp,
        does_not_raise(),
    ),
    "transaction_data_no_time_timestamp": (
        transaction_data_no_time_timestamp,
        does_not_raise(),
    ),
    "transaction_data_missing_timestamp": (
        transaction_data_missing_timestamp,
        pytest.raises(Exception),
    ),
    "transaction_data_zero_amount": (
        transaction_data_zero_amount,
        pytest.raises(Exception),
    ),
    "transaction_data_minimal_amount": (
        transaction_data_minimal_amount,
        does_not_raise(),
    ),
    "transaction_data_negative_amount": (
        transaction_data_negative_amount,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_amount": (
        transaction_data_missing_amount,
        pytest.raises(Exception),
    ),
    "transaction_data_PLN_currency": (
        transaction_data_PLN_currency,
        does_not_raise(),
    ),
    "transaction_data_USD_currency": (
        transaction_data_USD_currency,
        does_not_raise(),
    ),
    "transaction_data_EUR_currency": (
        transaction_data_EUR_currency,
        does_not_raise(),
    ),
    "transaction_data_incorrect_currency": (
        transaction_data_incorrect_currency,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_currency": (
        transaction_data_missing_currency,
        pytest.raises(Exception),
    ),
    "transaction_data_incorrect_customer_id": (
        transaction_data_incorrect_customer_id,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_customer_id": (
        transaction_data_missing_customer_id,
        pytest.raises(Exception),
    ),
    "transaction_data_incorrect_product_id": (
        transaction_data_incorrect_product_id,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_product_id": (
        transaction_data_missing_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_zero_quantity": (
        transaction_data_zero_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_minimal_quantity": (
        transaction_data_minimal_quantity,
        does_not_raise(),
    ),
    "transaction_data_negative_quantity": (
        transaction_data_negative_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_missing_quantity": (
        transaction_data_missing_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_floating_point_quantity": (
        transaction_data_floating_point_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_correct_string_quantity": (
        transaction_data_correct_string_quantity,
        does_not_raise(),
    ),
    "transaction_data_floating_point_string_quantity": (
        transaction_data_floating_point_string_quantity,
        pytest.raises(Exception),
    ),
    "transaction_data_incorrect_string_quantity": (
        transaction_data_incorrect_string_quantity,
        pytest.raises(Exception),
    ),
}

test_names, test_data = zip(*test_cases.items(), strict=False)
