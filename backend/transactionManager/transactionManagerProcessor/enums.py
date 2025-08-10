from enum import StrEnum


class Currency(StrEnum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"


class ProcessingStatus(StrEnum):
    PROCESSING = "processing"
    SUCCESS = "success"
    FAIL = "fail"
