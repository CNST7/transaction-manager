from decimal import Decimal

import pytest
from transactionManager.exceptions import domain_errors
from transactionManagerProcessor.utils.currency import (
    ExchangeFactory,
    ExchangeStrategy,
    _PLNFixedRatioStrategy,
)

test_cases = {
    "default_strategy": (
        {},
        _PLNFixedRatioStrategy,
    ),
    "default_strategy_type": (
        {"currency": "PLN"},
        _PLNFixedRatioStrategy,
    ),
    "default_strategy_currency": (
        {"fixed_rate": True},
        _PLNFixedRatioStrategy,
    ),
    "chosen_strategy": (
        {"currency": "PLN", "fixed_rate": True},
        _PLNFixedRatioStrategy,
    ),
}

test_names, test_data = zip(*test_cases.items(), strict=False)


class TestExchangeFactory:
    @pytest.mark.parametrize(
        "parameters,expected_strategy",
        test_data,
        ids=test_names,
    )
    def test_exchange_factory_loads_strategy(
        self, parameters: dict, expected_strategy: ExchangeStrategy
    ):
        strategy_processor = ExchangeFactory.prepare_strategy(parameters)
        assert isinstance(strategy_processor.strategy, expected_strategy)

    def test_exchange_factory_raises_error_on_not_implemented_strategy(self):
        with pytest.raises(
            domain_errors.ExchangeStrategyNotImplementedError,
            match=r"^Currency exchange strategy is not implemented for currency=AAA and fixed_rate=True parameters.",
        ):
            _ = ExchangeFactory.prepare_strategy({"currency": "AAA"})

    def test_exchange_factory_raises_error_on_strategy_unhandled_currency(self):
        with pytest.raises(
            domain_errors.CurrencyExchangeError,
            match=r"^Unhandled currency",
        ):
            default_strategy_processor = ExchangeFactory.prepare_strategy()
            default_strategy_processor.get_exchange_rate("AAA")

    def test_exchange_factory_fixed_rate_strategy_returns_proper_rates(self):
        default_strategy_processor = ExchangeFactory.prepare_strategy()

        rate_for_PLN = default_strategy_processor.get_exchange_rate("PLN")
        rate_for_EUR = default_strategy_processor.get_exchange_rate("EUR")
        rate_for_USD = default_strategy_processor.get_exchange_rate("USD")

        assert rate_for_PLN == Decimal("1.00")
        assert rate_for_EUR == Decimal("4.30")
        assert rate_for_USD == Decimal("4.00")
