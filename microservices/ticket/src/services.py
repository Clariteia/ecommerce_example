"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Service,
)

from .aggregates import (
    Ticket,
)


class TicketService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_ticket(code: str, order: int, amount: int) -> Ticket:
        """
        Creates a ticket

        :param code: Unique str representing the ticket
        :param order: `Order` associated to the `Ticket`
        :param amount: Total amount in €
        """
        payments = list()
        return await Ticket.create(code, order, payments, amount)

    @staticmethod
    async def get_tickets(ids: list[int]) -> list[Ticket]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Ticket.get(ids=ids)}
        return [values[id] for id in ids]