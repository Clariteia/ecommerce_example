from __future__ import (
    annotations,
)

import sys
import unittest
from pathlib import (
    Path,
)
from uuid import (
    UUID,
    uuid4,
)

import jwt
from minos.aggregate import (
    InMemoryTransactionRepository,
    InMemorySnapshotRepository,
    InMemoryEventRepository,
)
from minos.common import (
    DependencyInjector,
)
from minos.common.testing import (
    PostgresAsyncTestCase,
)
from minos.networks import (
    ResponseException,
)

from microservices.authentication.tests.utils import FakeLockPool
from src import (
    CredentialsQueryRepository,
    CredentialsQueryService,
)
from tests.utils import (
    _FakeBroker,
    _FakeRequest,
    _FakeRestRequest,
    _FakeSagaManager,
)


class TestCredentialsQueryService(PostgresAsyncTestCase):
    CONFIG_FILE_PATH = Path(__file__).parents[2] / "config.yml"

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.injector = DependencyInjector(
            self.config,
            saga_manager=_FakeSagaManager,
            event_broker=_FakeBroker,
            lock_pool=FakeLockPool,
            transaction_repository=InMemoryTransactionRepository,
            event_repository=InMemoryEventRepository,
            snapshot_repository=InMemorySnapshotRepository,
            credentials_repository=CredentialsQueryRepository.from_config(
                self.config, database=self.config.repository.database
            ),
        )
        await self.injector.wire(modules=[sys.modules[__name__]])

        self.service = CredentialsQueryService()

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    async def test_get_token(self):
        uuid = uuid4()
        username = "foo"  # UUID just to ensure its unique
        password = "bar"
        user = uuid4()

        await self.service.repository.create_credentials(uuid, username, password, True, user)

        fake_request = _FakeRestRequest(username, password)
        response = await self.service.generate_token(fake_request)
        token = (await response.content())["token"]
        payload = jwt.decode(token, options={"verify_signature": False})
        observed = UUID(payload["sub"])

        self.assertEqual(user, observed)

    async def test_get_by_username_does_not_exist(self):
        wrong_username = "should_not_exist"

        with self.assertRaises(ResponseException):
            fake_request = _FakeRequest({"username": wrong_username})
            await self.service.get_by_username(fake_request)

    async def test_unique_username(self):
        request = _FakeRequest({"username": "foo"})
        response = await self.service.unique_username(request)
        self.assertTrue(await response.content())

    async def test_unique_username_raises(self):
        await self.service.repository.create_credentials(uuid4(), "foo", "bar", True, uuid4())
        with self.assertRaises(ResponseException):
            request = _FakeRequest({"username": "foo"})
            await self.service.unique_username(request)


if __name__ == "__main__":
    unittest.main()
