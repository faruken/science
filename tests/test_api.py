#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import unittest
from typing import (Dict, Union)
from uuid import (UUID, uuid4)

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

    def test_health(self):
        _, res = sanic_endpoint_test(self.app, uri="/health", method="get")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("message"), 1)
        self.assertEqual(payload.get("status"), 200)

    def test_index_method_not_allowed(self):
        _, res = sanic_endpoint_test(self.app, uri="/", method="get")
        payload: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(payload.get("message"), "Method Not Allowed")
        self.assertEqual(payload.get("status"), 405)

    def test_index_wrong_url(self):
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        payload: Dict[str, str] = {"something": "wrong"}
        _, res = sanic_endpoint_test(self.app, uri="/",
                                     data=json.dumps(payload), headers=headers,
                                     method="post")
        response: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(response.get("message"), "Please type an imgur URL")
        self.assertEqual(response.get("status"), 200)

    def test_index_correct_url_brokers_unreachable(self):
        def __is_uuid4(value):
            try:
                _ = UUID(value, version=4)
            except ValueError:
                return False
            return True
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        payload: Dict[str, str] = {"url": "http://i.imgur.com/531SUvC.jpg"}
        _, res = sanic_endpoint_test(self.app, uri="/",
                                     data=json.dumps(payload), headers=headers,
                                     method="post")
        response: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(response.get("status"), 500)

    def test_status_unknown_task_id(self):
        task_id = "{0}".format(uuid4())
        _, res = sanic_endpoint_test(self.app, uri="/{0}".format(task_id))
        response: Dict[ProtocolType] = json.loads(res.text)
        self.assertEqual(response.get("status"), 404)

