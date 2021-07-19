"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from datetime import datetime

from uuid import uuid4, UUID

from minos.common import Service, Request, Response

from ..aggregates import User


class UserCommandService(Service):
    """User Service class"""

    @staticmethod
    async def create_user(request: Request) -> Response:
        """Create a new User instance.

        :param request: The ``Request`` that contains the needed information to create the User.
        :return: A ``Response`` containing the already created User.
        """
        content = await request.content()

        username = content["username"]
        status = content["status"]
        created_at = datetime.now()

        user = await User.create(username, status, created_at)

        return Response(user)
