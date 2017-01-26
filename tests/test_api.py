#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import unittest
from typing import (Dict, Union)

from sanic import Sanic
from sanic.config import Config
from sanic.request import Request
from sanic.response import json as sanic_json
from sanic.utils import sanic_endpoint_test

from science.api import app

Config.REQUEST_TIMEOUT: int = 1
ProtocolType = Dict[str, Union[str, int]]


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app: Sanic = app

    def test_error_404(self) -> None:
        _, res = sanic_endpoint_test(self.app, uri="/does_not_exist")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("status"), 404)
        self.assertEqual(payload.get("message"), "Not Found")

    def test_error_408(self):
        @self.app.route("/408")
        async def handler_408(request: Request) -> ProtocolType:
            await asyncio.sleep(1.1)
            return sanic_json({"status": 408, "message": "Request Timeout"})

        _, res = sanic_endpoint_test(self.app, uri="/408", method="get")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("status"), 408)
        self.assertEqual(payload.get("message"), "Request Timeout")

    def test_error_405(self):
        _, res = sanic_endpoint_test(self.app, uri="/")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("status"), 405)
        self.assertEqual(payload.get("message"), "Method Not Allowed")

    def test_error_500(self):
        @self.app.route("/err")
        async def handler(request: Request) -> str:
            return "fail"

        _, res = sanic_endpoint_test(self.app, uri="/err")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("status"), 500)
        self.assertEqual(payload.get("message"), "Something went wrong :(")
