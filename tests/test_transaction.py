"""Test module for Transaction class."""

from datetime import datetime, timezone

import pytest
from myof.transaction import Transaction
from pydantic import ValidationError


def test_transaction():
    """Test the Transaction class."""
    transaction = Transaction(
        transaction_id="123",
        account_id="456",
        date=datetime.now(tz=timezone.utc),
        amount=100.0,
        payee="Payee",
        description="Description",
        category="Category",
    )
    assert isinstance(transaction, Transaction)
    assert transaction.transaction_id == "123"
    assert transaction.account_id == "456"
    assert isinstance(transaction.date, datetime)
    assert transaction.amount == 100.0
    assert transaction.payee == "Payee"
    assert transaction.description == "Description"
    assert transaction.category == "Category"


def test_optional_fields():
    """Test that optional fields are optional."""
    transaction = Transaction(
        transaction_id="123",
        account_id="456",
        date=datetime.now(tz=timezone.utc),
        amount=100.0,
    )
    assert isinstance(transaction, Transaction)
    assert transaction.transaction_id == "123"
    assert transaction.account_id == "456"
    assert isinstance(transaction.date, datetime)
    assert transaction.amount == 100.0
    assert transaction.payee is None
    assert transaction.description is None
    assert transaction.category is None


def test_min_length_fields():
    """Test that min_length fields are enforced."""
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            payee="",
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            description="",
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            category="",
        )


def max_length_fields():
    """Test that max_length fields are enforced."""
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="a" * 101,
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="a" * 101,
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            payee="a" * 101,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            description="a" * 1001,
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="123",
            account_id="456",
            date=datetime.now(tz=timezone.utc),
            amount=100.0,
            category="a" * 101,
        )


def test_freeze_fields():
    """Test that frozen fields are frozen."""
    transaction = Transaction(
        transaction_id="123",
        account_id="456",
        date=datetime.now(tz=timezone.utc),
        amount=100.0,
    )
    with pytest.raises(ValueError):
        transaction.transaction_id = "456"
    with pytest.raises(ValueError):
        transaction.account_id = "789"


def test_required_fields():
    """Test that required fields are required."""
    with pytest.raises(ValidationError):
        Transaction()  # type: ignore
