#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""REST API module.
"""

from typing import Optional

from celery import (Celery, signature)
from celery.canvas import Signature
from kombu.exceptions import OperationalError
from logbook import Logger
from logbook.queues import RedisHandler
from sanic import Sanic
from sanic.config import Config
from sanic.exceptions import (NotFound, ServerError, RequestTimeout,
                              InvalidUsage)
from sanic.request import Request
from sanic.response import json
from sanic.router import REGEX_TYPES

from science.config import (configs, environment)
from science.tools.protocols import Protocol
from science.tools.utils import imgur_parser

app = Sanic("__ml_web__")
app.config: Config = Config()
app.config.LOGO: Optional[str] = None
app.config.REQUEST_TIMEOUT: int = 300  # 5 mins
app.config.REQUEST_MAX_SIZE: int = 1_048_576  # 1 MB
celery: Celery = Celery("tasks")
celery.config_from_object("celeryconfig")

UUID4_REGEX: str = r"[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z"
REGEX_TYPES.update({"uuid": (str, UUID4_REGEX)})
log = Logger("__ml_web__")


@app.exception(RequestTimeout)
def error_408(request: Request, exception: RequestTimeout) -> str:
    """Request Time out.
    :param request: Request
    :param exception: RequestTimeout
    :return: JSON
    """
    return json(Protocol(408, "Request Timeout")._asdict())


@app.exception(InvalidUsage)
def error_405(request: Request, exception: InvalidUsage) -> str:
    """MEthod Not Allowed. For some odd reasons, Sanic doesn't have MethodNotAllowedException.
    :param request: Request
    :param exception: InvalidUsage (hopefully Sanic will implement a proper MethodNotAllowedException)
    :return: JSON
    """
    return json(Protocol(405, "Method Not Allowed")._asdict())


@app.exception(NotFound)
def error_404(request: Request, exception: NotFound) -> str:
    """Not Found
    :param request: Request
    :param exception: NotFound
    :return: JSON
    """
    return json(Protocol(404, "Not Found")._asdict())


@app.exception(ServerError)
def error_500(request: Request, exception: ServerError) -> str:
    """Internal Server Error
    :param request: Request
    :param exception: Exception
    :return: JSON
    """
    return json(Protocol(500, "Something went wrong :(")._asdict())


@app.route("/status/<task_id:uuid>")
async def status(request: Request, task_id: str) -> str:
    """Status route for given task id
    :param request: Request
    :param task_id: UUID4 value of task_id
    :return: JSON
    """
    task: Signature = signature("tasks.analyze").AsyncResult(task_id)
    return json(Protocol(200, task.result)._asdict())


@app.route("/", methods=["POST"])
async def index(request: Request) -> str:
    """Chain the tasks and send it to background workers. Supports only POST.
    :param request: Request
    :return: JSON
    """
    user_url: Optional[str] = request.json.get("url")
    url: Optional[str] = imgur_parser(user_url)
    if not url:
        log.debug("URL Error: {0}".format(url))
        return json(Protocol(200, "Please type an imgur URL")._asdict())
    chain: Signature = signature("tasks.fetch", kwargs={"url": url})
    chain |= signature("tasks.analyze", kwargs={"url": url})
    try:
        task = chain()
    except OperationalError:
        log.critical("Cannot connect to broker: {0}".format(
            configs[environment].broker_url))
        return json(Protocol(500, "Something went wrong. Sorry :(")._asdict())
    return json(Protocol(200, task.task_id)._asdict())


def main() -> None:  # pragma: no cover
    """Run the application.
    :return: None
    """
    import asyncio
    from multiprocessing import cpu_count
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    workers: int = cpu_count()
    app.run(host="0.0.0.0", port=configs[environment].PORT, workers=workers,
            debug=configs[environment].DEBUG)


if __name__ == '__main__':
    handler = RedisHandler(host=configs[environment].log_backend,
                           key="log",
                           level=configs[environment].LOGLEVEL)
    with handler:
        main()
