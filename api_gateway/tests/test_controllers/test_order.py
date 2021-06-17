"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import unittest

import requests
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.test_utils import unittest_run_loop
from minos.api_gateway.common import MinosConfig
from minos.api_gateway.rest import ApiGatewayRestService
from tests.mock_servers.server import MockServer
from tests.utils import BASE_PATH


class TestOrder(AioHTTPTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def setUp(self) -> None:
        self.config = MinosConfig(self.CONFIG_FILE_PATH)
        self.discovery_server = MockServer(
            host=self.config.discovery.connection.host,
            port=self.config.discovery.connection.port,
        )
        self.discovery_server.add_json_response(
            "/discover",
            {
                "ip": "localhost",
                "port": "5568",
                "name": "order",
                "status": True,
                "subscribed": True,
            },
            methods=("GET",),
        )

        self.order_microservice = MockServer(host="localhost", port=5568)
        self.order_microservice.add_json_response("/order/5", {}, methods=("GET",))
        self.order_microservice.add_json_response(
            "/order", {"product_added": 5}, methods=("POST",)
        )
        self.order_microservice.add_json_response(
            "/order/5/history", {"products": [1, 7, 49]}, methods=("GET",)
        )

        self.discovery_server.start()
        self.order_microservice.start()
        super().setUp()

    def tearDown(self) -> None:
        self.discovery_server.shutdown_server()
        self.order_microservice.shutdown_server()
        super().tearDown()

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        app = web.Application()
        rest_interface = ApiGatewayRestService(config=self.config, app=app)

        return await rest_interface.create_application()

    @unittest_run_loop
    async def test_discovery_up_and_running(self):
        response = requests.get(
            "http://%s:%s/discover"
            % (
                self.config.discovery.connection.host,
                self.config.discovery.connection.port,
            )
        )

        self.assertEqual(200, response.status_code)

    @unittest_run_loop
    async def test_microservice_up_and_running(self):
        response = requests.get("http://localhost:5568/order/5")

        self.assertEqual(200, response.status_code)

    @unittest_run_loop
    async def test_get(self):
        resp = await self.client.request("GET", "/order/5")
        assert resp.status == 200
        text = await resp.text()
        # assert "works" in text

    @unittest_run_loop
    async def test_add(self):
        resp = await self.client.request("POST", "/order")
        assert resp.status == 200
        text = await resp.text()
        # assert "works" in text

    @unittest_run_loop
    async def test_history(self):
        resp = await self.client.request("GET", "/order/5/history")
        assert resp.status == 200
        text = await resp.text()
        # assert "works" in text


if __name__ == "__main__":
    unittest.main()
