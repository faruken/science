# -*- coding: utf-8 -*-

"""Configs
"""
from typing import (Optional, Dict)

import logbook
import os
from raven import Client


class Config:
    """Base config
    """
    DEBUG: bool = True
    TESTING: bool = False
    LOGLEVEL: int = logbook.DEBUG
    PORT: int = 5000
    log_backend: str = "127.0.0.1"
    broker_url: str = "redis://127.0.0.1:6379/0"
    result_backend: str = "redis://127.0.0.1:6379/0"
    sentry_client: Client = Client("http://{0}:{1}@0.0.0.0:9000/{2}".format(os.environ.get("SENTRY_USER"),
                                                                            os.environ.get("SENTRY_PASSWD"),
                                                                            os.environ.get("SENTRY_PROJECT")))
    aws_access_key_id: Optional[str] = None
    aws_access_secret_id: Optional[str] = None


class AWSConfig(Config):
    """AWS Config
    """
    DEBUG: bool = False
    LOGLEVEL: int = logbook.INFO
    aws_access_key_id: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_access_secret_id: Optional[str] = os.environ.get("AWS_ACCESS_SECRET_ID")
    log_backend: str = os.environ.get("AWS_LOG_BACKEND")
    broker_url: str = os.environ.get("AWS_BROKER_URL")
    result_backend: str = os.environ.get("AWS_RESULT_BACKEND")


class TestConfig(Config):
    """
    """
    TESTING: bool = True
    DEBUG: bool = False


class DockerComposeConfig(Config):
    """DEBUG is `true` since it's only used for development
    """
    DEBUG: bool = True
    log_backend: str = "redis"
    broker_url: str = "redis://redis"
    result_backend: str = "redis://redis"


configs: Dict[str, Config] = {
    "dev": Config,
    "docker": DockerComposeConfig,
    "aws": AWSConfig,
    "test": TestConfig
}

environment: str = os.environ.get("APP_ENV", "dev")
