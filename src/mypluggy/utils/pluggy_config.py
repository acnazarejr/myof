"""Configuration class for the MyPluggy package."""

import uuid

from pydantic import BaseModel


class PluggyConfig(BaseModel):
    """Configuration class for the MyPluggy package."""

    client_id: None | uuid.UUID
    client_secret: None | str
    items: dict[str, uuid.UUID] = {}
    accounts: dict[str, uuid.UUID] = {}
