from uuid import UUID

import pytest
from django.core.exceptions import FieldError
from rest_framework.serializers import ValidationError
from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.utils.qs_builder import (
    build_qs,
)

pytestmark = pytest.mark.django_db(transaction=True)


class TestQSBuilder:
    def test_qs_builder(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
        )

        excepted_transactions = Transaction.objects.filter(customer_id=customer_id_a)

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_date_from(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            date_from="2025-08-02",
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("d0466264-1384-4dc0-82d0-39e541b5c121")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_date_to(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            date_to="2025-07-02",
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("d2993a99-3358-41af-8047-070fa648d079")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_date_range(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            date_from="2025-07-03",
            date_to="2025-08-01",
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("ddaf9b82-1bf5-44b5-89ff-45816857403b")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_multiple_dates(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            date_from=["2025-08-02", "2025-08-01", "2025-08-15"],
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("d0466264-1384-4dc0-82d0-39e541b5c121")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_inapropriate_date_format(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        with pytest.raises(ValidationError):
            _ = build_qs(
                filter_key="customer_id",
                id=str(customer_id_a),
                date_from="02-08-2025",
            )

    def test_qs_builder_incorrect_filter_key(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        with pytest.raises(FieldError):
            _ = build_qs(
                filter_key="incorrect_id",
                id=str(customer_id_a),
            )

    def test_qs_builder_ignores_additional_query_params(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            additional_query_param="Ignore me",
            another_additional_param="Ignore me",
        )

        excepted_transactions = Transaction.objects.filter(customer_id=customer_id_a)

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_qs_builder_date_from_cannot_be_after_date_to(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        with pytest.raises(ValidationError) as error:
            _ = build_qs(
                filter_key="customer_id",
                id=str(customer_id_a),
                date_from="2025-08-02",
                date_to="2025-08-01",
            )

        assert error.match("`date_from` cannot occur after `date_to`")

    def test_qs_builder_date_from_equals_date_to(
        self,
        qs_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        qs = build_qs(
            filter_key="customer_id",
            id=str(customer_id_a),
            date_from="2025-08-02",
            date_to="2025-08-02",
        )

        assert [tr.transaction_id for tr in qs] == [
            UUID("d0466264-1384-4dc0-82d0-39e541b5c121")
        ]
