from collections.abc import Iterable
from datetime import date, timedelta
from uuid import UUID

from django.db.models.query import QuerySet
from transactionManagerProcessor.models import Transaction
from transactionManagerProcessor.serializers import (
    IDSerializer,
    QueryParamsSerializer,
)


class _ReportQueryParams:
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


def build_qs(
    filter_key: str,
    id: str,
    date_from: str | None = None,
    date_to: str | None = None,
    **kwargs,  # noqa: ARG001
) -> QuerySet[Transaction]:

    id_serializer = IDSerializer(data={"id": id})
    id_serializer.is_valid(raise_exception=True)
    path_param = _ReportPathParam(**id_serializer.validated_data)
    transactions: QuerySet[Transaction] = Transaction.objects.filter(
        **{f"{filter_key}": path_param.id}
    )

    query_serializer = QueryParamsSerializer(
        data={
            "date_from": _get_first(date_from),
            "date_to": _get_first(date_to),
        }
    )
    query_serializer.is_valid(raise_exception=True)
    query_params = _ReportQueryParams(**query_serializer.validated_data)

    if query_params.date_from:
        transactions = transactions.filter(timestamp__gte=query_params.date_from)

    if query_params.date_to:
        transactions = transactions.filter(timestamp__lt=query_params.date_to)

    return transactions
