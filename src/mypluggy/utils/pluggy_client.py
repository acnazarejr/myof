"""MyPluggyClient class to interact with Pluggy API."""

import functools
from datetime import datetime

import requests


def require_authentication(func):
    """Decorator to check if the client is authenticated before calling the decorated method."""

    @functools.wraps(func)
    def wrapper(self, *arg, **kw):
        if not self._api_key:
            raise ConnectionError("MyPluggyClient is not authenticated. You must call authenticate() first.")
        return func(self, *arg, **kw)

    return wrapper


DEFAULT_HTTP_CONNECT_TIMEOUT_SECONDS = 10
DEFAULT_HTTP_READ_TIMEOUT_SECONDS = 180


class MyPluggyClient:
    """MyPluggyClient class to interact with Pluggy API."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Initialize a MyPluggyClient object instance."""

        self._base_url = "https://api.pluggy.ai"
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = None

    def authenticate(self) -> None:
        """Authenticate with Pluggy API."""

        url = f"{self._base_url}/auth"
        payload = {"clientId": self._client_id, "clientSecret": self._client_secret}
        response = requests.post(
            url, json=payload, headers=self.__make_headers(), timeout=DEFAULT_HTTP_CONNECT_TIMEOUT_SECONDS
        )

        if response.status_code != 200:
            raise ConnectionError(f"Failed to authenticate with Pluggy API: {response.text}")

        self._api_key = response.json()["apiKey"]

    @require_authentication
    def get_item(self, item_id: str) -> dict:
        """Get item resources details from Pluggy API."""

        url = f"{self._base_url}/items/{item_id}"

        response = requests.get(url, headers=self.__make_headers(), timeout=DEFAULT_HTTP_READ_TIMEOUT_SECONDS)

        if response.status_code == 404:
            raise ValueError(f"Item with ID {item_id} not found.")

        if response.status_code == 500:
            raise ConnectionError(f"Server error when getting item from Pluggy API: {response.text}")

        if response.status_code != 200:
            raise ConnectionError(f"Failed to get item from Pluggy API: {response.text}")

        return response.json()

    @require_authentication
    def list_accounts(self, item_id: str) -> dict:
        """Recovers all accounts collected for the item provided from Pluggy API."""

        url = f"{self._base_url}/accounts?itemId={item_id}"
        response = requests.get(url, headers=self.__make_headers(), timeout=DEFAULT_HTTP_READ_TIMEOUT_SECONDS)

        if response.status_code != 200:
            raise ConnectionError(f"Failed to list accounts from Pluggy API: {response.text}")

        return response.json()

    @require_authentication
    def get_account(self, account_id: str) -> dict:
        """Recovers the account resource by its id from Pluggy API."""

        url = f"{self._base_url}/accounts/{account_id}"
        response = requests.get(url, headers=self.__make_headers(), timeout=DEFAULT_HTTP_READ_TIMEOUT_SECONDS)

        if response.status_code == 404:
            raise ValueError(f"Account with ID {account_id} not found.")

        if response.status_code == 500:
            raise ConnectionError(f"Server error when getting account from Pluggy API: {response.text}")

        if response.status_code != 200:
            raise ConnectionError(f"Failed to get account from Pluggy API: {response.text}")

        return response.json()

    @require_authentication
    def list_transactions(
        self, account_id: str, from_date: str | datetime | None = None, to_date: str | datetime | None = None
    ) -> dict:
        """Recovers all transactions collected for the account provided from Pluggy API."""

        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime("%Y-%m-%d")
            from_date = f"&from={from_date}"

        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime("%Y-%m-%d")
            to_date = f"&to={to_date}"

        url = f"{self._base_url}/transactions?accountId={account_id}{from_date}{to_date}"
        response = requests.get(url, headers=self.__make_headers(), timeout=DEFAULT_HTTP_READ_TIMEOUT_SECONDS)

        if response.status_code == 400:
            raise ValueError(f"Account with ID {account_id} not found.")

        if response.status_code == 500:
            raise ConnectionError(f"Server error when getting account from Pluggy API: {response.text}")

        if response.status_code != 200:
            raise ConnectionError(f"Failed to list transactions from Pluggy API: {response.text}")

        return response.json()

    def get_transaction(self, transaction_id: str) -> dict:
        """Recovers the transaction resource by its id from Pluggy API."""

        url = f"{self._base_url}/transactions/{transaction_id}"
        response = requests.get(url, headers=self.__make_headers(), timeout=DEFAULT_HTTP_READ_TIMEOUT_SECONDS)

        if response.status_code == 404:
            raise ValueError(f"Transaction with ID {transaction_id} not found.")

        if response.status_code == 500:
            raise ConnectionError(f"Server error when getting transaction from Pluggy API: {response.text}")

        if response.status_code != 200:
            raise ConnectionError(f"Failed to get transaction from Pluggy API: {response.text}")

        return response.json()

    def __make_headers(self) -> dict:
        """Create headers for Pluggy API requests."""

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        if self._api_key:
            headers["X-API-KEY"] = self._api_key

        return headers
