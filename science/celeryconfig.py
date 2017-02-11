# -*- coding: utf-8 -*-

"""celery configs.
"""

from typing import (Dict, Union, List, NamedTuple)

from science.config import (configs, environment)

ProtocolType = Dict[str, Union[str, int]]


class BrokerProtocol(NamedTuple):
    """Default broker options for celery.
    """
    visibility_timeout: int = 7200
    polling_interval: int = 30
    queue_name_prefix: str = "celery-science-"
    region: str = "us-east-1"


class CeleryConfig:
    """Celery config options.
    """
    broker_url: str = configs[environment].broker_url
    result_backend: str = configs[environment].result_backend
    broker_transport_options: Dict[ProtocolType] = BrokerProtocol._asdict()
    worker_max_tasks_per_child: int = 1
    worker_max_memory_per_child: int = 400_000  # 400MB
    task_serializer: str = "json"
    task_compression: str = "gzip"
    result_serializer: str = "json"
    result_expires: int = 0
    accept_content: List[str] = ["json"]
    timezone: str = "Australia/Sydney"
    enable_utc: bool = True
