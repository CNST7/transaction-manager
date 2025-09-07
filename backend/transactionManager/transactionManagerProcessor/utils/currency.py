import logging
from abc import ABC, abstractmethod
from decimal import Decimal

from pydantic import BaseModel, ValidationError
from transactionManager.exceptions import domain_errors
from transactionManagerProcessor.enums import Currency

logger = logging.getLogger(__name__)


class ExchangeStrategy(ABC):
    @abstractmethod
    def get_exchange_rate(self, currency: Currency) -> Decimal: ...


class _PLNFixedRatioStrategy(ExchangeStrategy):
    def get_exchange_rate(self, currency: Currency) -> Decimal:
        PLN_currency_exchange: dict[Currency, Decimal] = {
            Currency.PLN: Decimal("1.00"),
            Currency.EUR: Decimal("4.30"),
            Currency.USD: Decimal("4.00"),
        }
        try:
            exchange_rate = PLN_currency_exchange[currency]
        except KeyError:
            raise domain_errors.CurrencyExchangeError(f"Unhandled currency {currency}")

        return exchange_rate


class ExchangeProcessor(ABC):
    @property
    @abstractmethod
    def strategy(self) -> ExchangeStrategy: ...

    @abstractmethod
    def get_exchange_rate(self, currency: Currency) -> Decimal: ...


class _ExchangeProcessor(ExchangeProcessor):
    def __init__(self, strategy: ExchangeStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> ExchangeStrategy:
        return self._strategy

    def get_exchange_rate(self, currency: Currency) -> Decimal:
        return self._strategy.get_exchange_rate(currency)


class _ExchangeKey(BaseModel, frozen=True):
    currency: Currency = Currency.PLN
    fixed_rate: bool = True


class ExchangeFactory:
    _available_strategies: dict[_ExchangeKey, ExchangeStrategy] = {
        _ExchangeKey(currency=Currency.PLN, fixed_rate=True): _PLNFixedRatioStrategy,
    }

    @classmethod
    def prepare_strategy(
        cls,
        query_params: dict = None,
    ) -> ExchangeProcessor:
        if query_params is None:
            query_params = {}
        try:
            currency_exchange_key = _ExchangeKey(**query_params)
            strategy = cls._available_strategies[currency_exchange_key]
            processor = _ExchangeProcessor(strategy())

        except (KeyError, ValidationError):
            def_currency_exchange = _ExchangeKey()
            error_message = f"Currency exchange strategy is not implemented for currency={query_params.get('currency', def_currency_exchange.currency)} and fixed_rate={query_params.get('fixed_rate', def_currency_exchange.fixed_rate)} parameters. Possible values: {cls._possible_values()}"
            logger.error(error_message)
            raise domain_errors.ExchangeStrategyNotImplementedError(error_message)
        return processor

    @classmethod
    def _possible_values(cls):
        return ", ".join(
            f"currency={x.currency.value}, fixed_rate={x.fixed_rate}"
            for x in cls._available_strategies.keys()
        )
