from decimal import Decimal

from transactionManagerProcessor.enums import Currency

PLN_currency_exchange: dict[Currency, Decimal] = {
    Currency.PLN: Decimal("1.00"),
    Currency.EUR: Decimal("4.30"),
    Currency.USD: Decimal("4.00"),
}
