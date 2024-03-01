"""Importer abstract class."""

import abc
from collections.abc import Iterable

from myof.transaction import Transaction


class Importer(abc.ABC):
    """Importer abstract class."""

    @abc.abstractmethod
    def retrieve_transactions(self) -> Iterable[Transaction]:
        """Retrieve transactions from the source."""
