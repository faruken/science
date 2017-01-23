# -*- coding: utf-8 -*-


"""Protocols
"""

from typing import NamedTuple


class Protocol(NamedTuple):
    """Response protocol.
    """
    status: int
    message: str
