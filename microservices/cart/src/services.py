"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    uuid4,
)

from minos.common import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    Cart,
    CartItem
)


class CartService(Service):
    """Cart Service class"""

    @staticmethod
    async def create_cart(user: int) -> Cart:
        """
        Creates a cart

        :param user_id: The user ID.
        :param products: The list of product identifiers to be included in the ticket.
        """
        cart = await Cart.create(user=user, products=[])
        #await self.saga_manager.run("CreateCart", context=SagaContext(cart=cart, product_ids=products))

        return cart

    @staticmethod
    async def add_item(cart: int, product: CartItem, quantity: int) -> Cart:
        """
        Creates a cart

        :param user_id: The user ID.
        :param products: The list of product identifiers to be included in the ticket.
        """
        cart = await Cart.get_one(cart)
        cart_item = CartItem(product=product, quantity=quantity)
        cart.products.append(cart_item)
        await cart.save()

        return cart

    @staticmethod
    async def delete_item(user_id: int, product: CartItem) -> Cart:
        pass

    @staticmethod
    async def update_item(user_id: int, product: CartItem) -> CartItem:
        pass

    @staticmethod
    async def get_cart(user: int) -> Cart:
        pass

    @staticmethod
    async def delete_cart(user_id: int, cart: Cart) -> Cart:
        pass