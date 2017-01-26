#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from typing import (Dict, Union, List)

from science.tools.protocols import Protocol
from science.tools.utils import imgur_parser


class TestProtocol(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol: Protocol = Protocol(200, "Hello World")
        self.urls: List[str] = ["http://i.imgur.com/531SUvC.jpg",
                                "http://example.com/b.jpg",
                                "http://i.imgur.com/2M11zXf.gifv",
                                "http://imgur.com/531SUvC",
                                "imgur.com/531SUvC",
                                "http://imgur.com/a/531SUvC",
                                "http://imgur.com/a/531SUvC.jpg"]

    def test_protocol(self) -> None:
        mapp: Dict[str, Union[str, int]] = self.protocol._asdict()
        self.assertDictEqual({"status": 200, "message": "Hello World"}, mapp)
        self.assertEqual(self.protocol.status, 200)
        self.assertEqual(self.protocol.message, "Hello World")

    def test_imgur_parser(self) -> None:
        self.assertIsNone(imgur_parser(None))
        self.assertEqual(self.urls[0], imgur_parser(self.urls[0]))
        for url in self.urls[1:]:
            self.assertIsNone(imgur_parser(url))
