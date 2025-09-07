class TransactionManagerBaseError(Exception):
    """
    Base error class for domain-specific errors in Transaction Manager.

    All custom domain errors should inherit from this class to ensure consistent error handling.

    Example:
        class CustomDomainError(TransactionManagerBaseError):
            \"\"\"Raised when certain case happens\"\"\"

        ...
    """

    ...


class QuerysetBuilderError(TransactionManagerBaseError):
    """Raised when building queryset with builder class fails."""

    ...


class ExchangeStrategyNotImplementedError(TransactionManagerBaseError):
    """Raised when currency exchange strategy is not implemented."""

    ...


class CurrencyExchangeError(TransactionManagerBaseError):
    """Raised when currency exchange strategy fails to provide exchange ratio."""

    ...
