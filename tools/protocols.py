# -*- coding: utf-8 -*-


"""Protocols
"""

from typing import (NamedTuple, Dict, Union)


class Protocol(NamedTuple):
    status: int
    message: str

    def _asdict(self) -> Dict[str, Union[str, int]]:
        """Return as dict.

        :return: dict
        """
        return {"status": self.status, "message": self.message}
