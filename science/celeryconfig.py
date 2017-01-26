# -*- coding: utf-8 -*-

"""celery configs.
"""

from typing import (Dict, Union, List)

from science.config import (configs, environment)

broker_url: str = configs[environment].broker_url
result_backend: str = configs[environment].result_backend
broker_transport_options: Dict[str, Union[str, int]] = {
    "visibility_timeout": 7200, "polling_interval": 30,
    "queue_name_prefix": "celery-science-",
    "region": "us-east-1"}

worker_max_tasks_per_child: int = 1
worker_max_memory_per_child: int = 400_000  # 400MB
task_serializer: str = "json"
task_compression: str = "gzip"
result_serializer: str = "json"
result_expires: int = 0
accept_content: List[str] = ["json"]
timezone: str = "Australia/Sydney"
enable_utc: bool = True
