# -*- coding: utf-8 -*-


"""Protocols
"""

from typing import (NamedTuple, Union)


class Protocol(NamedTuple):
    """Response protocol.
    """
    status: int
    message: Union[str, int]
