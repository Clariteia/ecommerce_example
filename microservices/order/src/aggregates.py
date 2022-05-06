from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    Optional,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    Entity,
    Ref,
    ValueObject,
)
from minos.common import (
    Inject,
)
from minos.saga import (
    SagaContext,
    SagaManager,
    SagaStatus,
)


class OrderStatus(str, Enum):
    """Order Status class."""

    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"


# noinspection PyUnresolvedReferences
class Order(Entity):
    """Order Entity class."""

    ticket: Optional[Ref["src.aggregates.Ticket"]]

    payment: Optional[Ref["src.aggregates.Payment"]]
    payment_detail: PaymentDetail

    # TODO: Future Shipment Microservice
    shipment_detail: ShipmentDetail

    status: OrderStatus
    total_amount: Optional[float]

    created_at: datetime
    updated_at: datetime

    customer: Ref["src.aggregates.Customer"]


class PaymentDetail(ValueObject):
    """Payment Detail class."""

    card_holder: str
    card_number: int
    card_expire: str
    card_cvc: str


class ShipmentDetail(ValueObject):
    """Shipment Detail class."""

    name: str
    last_name: str
    email: str
    address: str
    country: str
    city: str
    province: str
    zip: int


# noinspection PyUnresolvedReferences
class OrderAggregate(Aggregate[Order]):
    """Order Aggregate class."""

    @Inject()
    def __init__(self, *args, saga_manager: SagaManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.saga_manager = saga_manager

    async def create_order(
        self, cart_uuid: UUID, customer_uuid: UUID, payment: dict[str, Any], shipment: dict[str, Any]
    ) -> Order:
        """TODO"""
        from .commands import (
            CREATE_ORDER,
        )

        payment_detail = PaymentDetail(**payment)
        shipment_detail = ShipmentDetail(**shipment)

        execution = await self.saga_manager.run(
            CREATE_ORDER,
            context=SagaContext(
                cart_uuid=cart_uuid,
                customer_uuid=customer_uuid,
                payment_detail=payment_detail,
                shipment_detail=shipment_detail,
            ),
            raise_on_error=False,
        )

        if execution.status != SagaStatus.Finished:
            raise ValueError("An error occurred during order creation.")

        return execution.context["order"]

    async def create_order_instance(
        self,
        ticket: Ref["src.aggregates.Ticket"],
        payment: Ref["src.aggregates.Payment"],
        payment_detail: PaymentDetail,
        shipment_detail: ShipmentDetail,
        total_amount: float,
        customer: Ref["src.aggregates.Customer"],
    ) -> Order:
        """TODO"""
        order, delta = await self.repository.create(
            Order,
            ticket=ticket,
            payment=payment,
            payment_detail=payment_detail,
            shipment_detail=shipment_detail,
            total_amount=total_amount,
            status=OrderStatus.COMPLETED,
            customer=customer,
        )
        await self.publish_domain_event(delta)

        return order
