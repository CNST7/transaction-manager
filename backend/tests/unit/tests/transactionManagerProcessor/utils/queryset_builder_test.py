from uuid import UUID

import pytest
from rest_framework.serializers import ValidationError
from transactionManager.exceptions import domain_errors
from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.utils.queryset_builder import (
    TransactionQuerySetPartialDirector,
)

pytestmark = pytest.mark.django_db(transaction=True)


class TestTransactionQuerySetPartialDirector:
    def test_transaction_queryset_partial_director(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .build()
        )

        excepted_transactions = Transaction.objects.filter(customer_id=customer_id_a)

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_date_from(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(date_from="2025-08-02")
            .build()
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("b2f4b977-c0de-409c-ae9b-39b806f3f309")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_date_to(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(date_to="2025-07-02")
            .build()
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id__in=(
                UUID("d2993a99-3358-41af-8047-070fa648d079"),
                UUID("f00a9313-4eaf-4e15-9b85-2802a5213764"),
            )
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_date_range(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(date_from="2025-07-02", date_to="2025-08-01")
            .build()
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id__in=(
                UUID("d2993a99-3358-41af-8047-070fa648d079"),
                UUID("ddaf9b82-1bf5-44b5-89ff-45816857403b"),
                UUID("d0466264-1384-4dc0-82d0-39e541b5c121"),
            )
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_multiple_dates(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(date_from=["2025-08-02", "2025-08-01", "2025-08-15"])
            .build()
        )

        excepted_transactions = Transaction.objects.filter(
            transaction_id=UUID("b2f4b977-c0de-409c-ae9b-39b806f3f309")
        )

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_inapropriate_date_format(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        with pytest.raises(ValidationError):
            _ = (
                TransactionQuerySetPartialDirector.customer_summary_queryset()
                .with_filter_value(str(customer_id_a))
                .with_query_params(date_from="02-08-2025")
                .build()
            )

    def test_transaction_queryset_partial_director_ignores_additional_query_params(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(
                additional_query_param="Ignore me",
                another_additional_param="Ignore me",
            )
            .build()
        )

        excepted_transactions = Transaction.objects.filter(customer_id=customer_id_a)

        assert set(transactions.values_list("transaction_id", flat=True)) == set(
            excepted_transactions.values_list("transaction_id", flat=True)
        )

    def test_transaction_queryset_partial_director_date_from_cannot_be_after_date_to(
        self,
        customer_id_a: UUID,
    ):
        with pytest.raises(ValidationError) as error:
            _ = (
                TransactionQuerySetPartialDirector.customer_summary_queryset()
                .with_filter_value(str(customer_id_a))
                .with_query_params(
                    date_from="2025-08-02",
                    date_to="2025-08-01",
                )
                .build()
            )

        assert error.match("`date_from` cannot occur after `date_to`")

    def test_transaction_queryset_partial_director_date_from_equals_date_to(
        self,
        queryset_builder_transactions: list[Transaction],
        customer_id_a: UUID,
    ):
        transactions = (
            TransactionQuerySetPartialDirector.customer_summary_queryset()
            .with_filter_value(str(customer_id_a))
            .with_query_params(
                date_from="2025-08-02",
                date_to="2025-08-02",
            )
            .build()
        )

        assert [tr.transaction_id for tr in transactions] == [
            UUID("b2f4b977-c0de-409c-ae9b-39b806f3f309")
        ]

    def test_transaction_queryset_partial_director_raises_queryset_build_error_when_filter_value_was_not_set(
        self,
    ):
        with pytest.raises(domain_errors.QuerysetBuilderError) as error:
            _ = TransactionQuerySetPartialDirector.customer_summary_queryset().build()

        assert error.match(r"^Please use `with_filter_value\(\)` method before build$")
