"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import (
    datetime,
)

from minos.common import (
    Aggregate,
    DeclarativeModel
)


class User(Aggregate):
    """User Aggregate class."""

    username: str
    status: str

    created_at: datetime
    updated_at: datetime

class Address(DeclarativeModel):
    street: str
    street_no: int
