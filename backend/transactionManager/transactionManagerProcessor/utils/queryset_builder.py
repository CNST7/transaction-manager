from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import date, timedelta
from typing import Self
from uuid import UUID

from django.db.models.query import QuerySet
from transactionManager.exceptions import domain_errors
from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.serializers import (
    IDSerializer,
    QueryParamsSerializer,
)


class _ReportQueryParamsRaw:
    def __init__(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        **kwargs,  # noqa: ARG001
    ):
        self.date_from = date_from
        self.date_to = date_to


class _ReportQueryParamsValidated:
    def __init__(self, date_from: date | None = None, date_to: date | None = None):
        self.date_from = date_from
        self.date_to = date_to + timedelta(days=1) if date_to else date_to


class _ReportPathParam:
    def __init__(self, id: UUID):
        self.id = id


def _get_first(query_param):
    if isinstance(query_param, str):
        return query_param
    if isinstance(query_param, Iterable):
        if query_param:
            return query_param[0]
    return query_param


class DirectedQuerySetBuilder(ABC):
    @abstractmethod
    def build(self) -> QuerySet: ...

    @abstractmethod
    def with_filter_value(self, filter_value: str) -> Self: ...

    @abstractmethod
    def with_query_params(self, **kwargs) -> Self: ...


class QuerySetBuilder(DirectedQuerySetBuilder):
    @abstractmethod
    def with_filter_key(self, filter_key: str) -> Self: ...


class TransactionQuerySetBuilder(QuerySetBuilder):
    @abstractmethod
    def build(self) -> QuerySet[Transaction]: ...


class DirectedTransactionQuerySetBuilder(
    TransactionQuerySetBuilder,
    DirectedQuerySetBuilder,
): ...


class _TransactionQuerySetBuilder(TransactionQuerySetBuilder):
    def __init__(self):
        self._queryset: QuerySet[Transaction] = Transaction.objects.all()
        self._filter_value: str | None = None
        self._filter_key: str | None = None
        self._query_params: _ReportQueryParamsValidated | None = None

    def build(self) -> QuerySet[Transaction]:
        if not self._filter_key:
            raise domain_errors.QuerysetBuilderError(
                "Please use `with_filter_key()` method before build"
            )
        if not self._filter_value:
            raise domain_errors.QuerysetBuilderError(
                "Please use `with_filter_value()` method before build"
            )

        self._queryset: QuerySet[Transaction] = Transaction.objects.filter(
            **{f"{self._filter_key}": self._filter_value}
        )

        if self._query_params:
            if self._query_params.date_from:
                self._queryset = self._queryset.filter(
                    timestamp__gte=self._query_params.date_from
                )

            if self._query_params.date_to:
                self._queryset = self._queryset.filter(
                    timestamp__lt=self._query_params.date_to
                )

        return self._queryset

    def with_filter_key(self, filter_key: str) -> Self:
        valid_filter_keys = ("customer_id", "product_id")
        if filter_key not in valid_filter_keys:
            raise domain_errors.QuerysetBuilderError(
                f"Invalid value for {filter_key=}. Should be one of {valid_filter_keys=}"
            )
        self._filter_key = filter_key
        return self

    def with_filter_value(self, filter_value: str) -> Self:
        id_serializer = IDSerializer(data={"id": filter_value})
        id_serializer.is_valid(raise_exception=True)
        self._filter_value = _ReportPathParam(**id_serializer.validated_data).id
        return self

    def with_query_params(self, **kwargs) -> Self:
        raw_query_params = _ReportQueryParamsRaw(**kwargs)
        query_serializer = QueryParamsSerializer(
            data={
                "date_from": _get_first(raw_query_params.date_from),
                "date_to": _get_first(raw_query_params.date_to),
            }
        )
        query_serializer.is_valid(raise_exception=True)
        self._query_params = _ReportQueryParamsValidated(
            **query_serializer.validated_data
        )
        return self


class TransactionQuerySetPartialDirector:
    """Starts building process"""

    @staticmethod
    def customer_summary_queryset() -> DirectedTransactionQuerySetBuilder:
        """Initiate queryset build for customer summary"""
        return _TransactionQuerySetBuilder().with_filter_key("customer_id")

    @staticmethod
    def product_summary_queryset() -> DirectedTransactionQuerySetBuilder:
        """Initiate queryset build for product summary"""
        return _TransactionQuerySetBuilder().with_filter_key("product_id")
