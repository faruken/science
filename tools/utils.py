# -*- coding: utf-8 -*-


"""Utils.
"""

from typing import Optional
from urllib.parse import urlparse

import os


def imgur_parser(url: Optional[str]) -> Optional[str]:
    """this is shitshow. Needs to be revised. Like seriously.

    :param url: URL to check if it's valid imgur URL.
    :return: imgur URL or None.
    """
    if not url:
        return None
    o = urlparse(url)
    filename, ext = os.path.splitext(url)
    if "imgur.com" not in o.netloc.lower() or not o.path:
        return None
    if ext not in [".jpg", ".png"]:
        return None
    if "/a/" in o.path:
        return None
    path: str = "{0}{1}".format(filename, ext)
    return path
