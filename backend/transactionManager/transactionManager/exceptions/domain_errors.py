class TransactionManagerBaseError(Exception):
    """Base error class"""

    ...


class QuerysetBuilderError(TransactionManagerBaseError):
    """Queryset builder error"""

    ...
