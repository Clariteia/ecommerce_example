"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.saga import (
    Saga,
    SagaContext,
)
from src.aggregates import (
    Cart,
)

from .callbacks import (
    _release_products_callback,
    _reserve_products_callback,
)


async def _create_commit_callback(context: SagaContext) -> SagaContext:
    cart_id = context["cart_id"]
    product = context["product"]
    cart = await Cart.get_one(cart_id)
    cart.products.discard(product)

    await cart.save()
    return SagaContext(cart=cart)


REMOVE_CART_ITEM = (
    Saga("RemoveCartItem")
    .step()
    .invoke_participant("ReserveProducts", _release_products_callback)
    .with_compensation("ReserveProducts", _reserve_products_callback)
    .commit(_create_commit_callback)
)
