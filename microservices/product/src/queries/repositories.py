"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from typing import (
    NoReturn,
)
from uuid import (
    UUID,
)

from minos.common import (
    MinosConfig,
    PostgreSqlMinosDatabase,
)


class ProductInventoryRepository(PostgreSqlMinosDatabase):
    """TODO"""

    async def _setup(self) -> NoReturn:
        await self.submit_query(_CREATE_TABLE)

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> ProductInventoryRepository:
        return cls(database="product_query_db", port=5432, user="minos", password="min0s", host="localhost")

    async def get_without_stock(self) -> list[UUID]:
        """TODO

        :return: TODO
        """
        entries = [entry async for entry in self.submit_query_and_iter(_GET_PRODUCTS_WITHOUT_STOCK)]
        uuids = [entry[0] for entry in entries]
        return uuids

    async def insert_inventory_amount(self, uuid: UUID, inventory_amount: int) -> NoReturn:
        """TODO

        :param uuid: TODO
        :param inventory_amount: TODO
        :return: TODO
        """
        await self.submit_query(_INSERT_PRODUCT_QUERY, {"uuid": uuid, "inventory_amount": inventory_amount})

    async def delete(self, uuid: UUID) -> NoReturn:
        """TODO

        :param uuid: TODO
        :return: TODO
        """
        await self.submit_query(_DELETE_PRODUCT_QUERY, {"uuid": uuid})


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS product (
    uuid UUID NOT NULL PRIMARY KEY,
    inventory_amount INT NOT NULL
);
""".strip()

_INSERT_PRODUCT_QUERY = """
INSERT INTO product (uuid, inventory_amount)
VALUES (%(uuid)s,  %(inventory_amount)s)
ON CONFLICT (uuid)
DO
   UPDATE SET inventory_amount = %(inventory_amount)s
;
""".strip()

_DELETE_PRODUCT_QUERY = """
DELETE FROM product
WHERE uuid = %(uuid)s;
""".strip()

_GET_PRODUCTS_WITHOUT_STOCK = """
SELECT uuid 
FROM product
WHERE inventory_amount = 0;
""".strip()
