"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    ModelType,
)
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

META = MetaData()
REVIEW_TABLE = Table(
    "review",
    META,
    Column("uuid", UUID_PG(as_uuid=True), primary_key=True),
    Column("product_uuid", UUID_PG(as_uuid=True)),
    Column("user_uuid", UUID_PG(as_uuid=True)),
    Column("version", Integer, nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("score", Integer, nullable=False),
    Column("product_title", Text, nullable=False),
    Column("username", Text, nullable=False),
    UniqueConstraint('product_uuid', 'user_uuid', name='uix_1'),
)

ProductDTO = ModelType.build(
    "ProductDTO",
    {
        "uuid": UUID,
        "product_uuid": UUID,
        "user_uuid": UUID,
        "title": str,
        "description": str,
        "score": int,
        "product_title": str,
        "username": str,
    },
)

RatingDTO = ModelType.build(
    "RatingDTO",
    {
        "product_uuid": UUID,
        "product_title": str,
        "average": float,
    },
)
