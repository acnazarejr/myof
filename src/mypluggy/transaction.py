"""Transaction class for the myof package."""

from datetime import datetime

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    """A class to represent a transaction."""

    transaction_id: str = Field(min_length=1, max_length=100, frozen=True)
    account_id: str = Field(min_length=1, max_length=100, frozen=True)
    date: datetime = Field(frozen=False)
    amount: float = Field(frozen=False)
    payee: None | str = Field(default=None, min_length=1, max_length=100)
    description: None | str = Field(default=None, min_length=1, max_length=1000)
    category: None | str = Field(default=None, min_length=1, max_length=100)
