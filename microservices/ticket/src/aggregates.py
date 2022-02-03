from __future__ import annotations

from minos.aggregate import (
    RootEntity,
    ExternalEntity,
    Entity,
    EntitySet,
    Ref,
)


class Ticket(RootEntity):
    """Ticket RootEntity class."""

    code: str
    total_price: float
    entries: EntitySet[TicketEntry]


class TicketEntry(Entity):
    """Order Item class"""

    title: str
    unit_price: float
    quantity: int
    product: Ref[Product]


class Product(ExternalEntity):
    """Order ExternalEntity class."""

    title: str
    price: float
