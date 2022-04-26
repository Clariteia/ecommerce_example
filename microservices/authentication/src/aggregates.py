from __future__ import (
    annotations,
)

import logging
from typing import (
    Any,
)
from uuid import (
    UUID,
)

from minos.aggregate import (
    Aggregate,
    Condition,
    ExternalEntity,
    Ref,
    RootEntity,
)
from minos.common import (
    Inject,
)
from minos.saga import (
    SagaContext,
    SagaManager,
)

logger = logging.getLogger(__name__)


class Credentials(RootEntity):
    """Credentials RootEntity class.

    The purpose of this aggregate is to store the needed information to be authenticated.
    """

    username: str
    password: str
    active: bool
    user: Ref[Customer]


class Customer(ExternalEntity):
    """Customer ExternalEntity class."""


class CredentialsAggregate(Aggregate[Credentials]):
    """Credentials Aggregate class."""

    @Inject()
    def __init__(self, *args, saga_manager: SagaManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.saga_manager = saga_manager

    async def create_credentials(self, username: str, password: str, metadata: dict[str, Any]) -> Credentials:
        """TODO"""
        from .commands import (
            CREATE_CREDENTIALS_SAGA,
        )

        execution = await self.saga_manager.run(
            definition=CREATE_CREDENTIALS_SAGA,
            context=SagaContext(username=username, password=password, metadata=metadata),
        )

        credentials = execution.context["credentials"]
        return credentials

    async def exists_username(self, username: str) -> bool:
        """Check if username already exists.

        :param username: The username to be checked.
        :return: ``True`` if the username exists or ``False`` otherwise.
        """
        try:
            await self.repository.find(Credentials, Condition.EQUAL("username", username)).__anext__()
            return True
        except StopAsyncIteration:
            return False

    async def delete_credentials(self, uuid: UUID) -> None:
        """TODO"""
        credentials = await self.repository.get(Credentials, uuid)

        await self.repositsaory.delete(credentials)

    async def delete_credentials_by_user(self, user: UUID) -> None:
        """TODO"""
        entries = {
            credentials async for credentials in self.repository.find(Credentials, Condition.EQUAL("user", user))
        }

        if len(entries) == 0:
            return

        if len(entries) > 1:
            logger.warning(f"The user identified by {user!r} had multiple associated credentials")

        for credentials in entries:
            await self.repository.delete(credentials)
