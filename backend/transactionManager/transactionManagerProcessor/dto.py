from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, PositiveInt, Field
from uuid import UUID
from datetime import datetime
from transactionManagerProcessor.enums import Currency


class TransactionDTO(BaseModel):
    id: UUID
    timestamp: datetime
    amount: Annotated[Decimal, Field(ge=00.01, max_digits=10, decimal_places=2)]
    currency: Currency
    customer_id: UUID
    product_id: UUID
    quantity: PositiveInt
