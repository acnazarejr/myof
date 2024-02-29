"""Transaction class for the myof package."""

from datetime import datetime


class Transaction:
    """A class to represent a transaction."""

    def __init__(
        self,
        transaction_id: str,
        account_id: str,
        date: datetime,
        amount: float,
        payee: None | str = None,
        description: None | str = None,
        category: None | str = None,
    ) -> None:
        """Initialize a Transaction object instance."""

        self._transaction_id = transaction_id
        self._account_id = account_id
        self._date = date
        self._amount = amount
        self._payee = payee
        self._description = description
        self._category = category
