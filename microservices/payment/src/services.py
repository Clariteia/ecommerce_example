"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Service,
)

from .aggregates import (
    Payment,
)


class PaymentService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_payment(credit_number: int, amount: float) -> Payment:
        """
        Creates a payment

        :param credit_number: TODO
        :param amount; TODO
        """
        status = "created"
        return await Payment.create(credit_number, amount, status)

    @staticmethod
    async def get_payments(ids: list[int]) -> list[Payment]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        values = {v.id: v async for v in Payment.get(ids=ids)}
        return [values[id] for id in ids]
