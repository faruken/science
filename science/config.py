# -*- coding: utf-8 -*-

"""Configs
"""
from typing import (Optional, Dict)

import os


class Config:
    """Base config
    """
    DEBUG: bool = True
    TESTING: bool = False
    broker_url: str = "redis://127.0.0.1:6379/0"
    result_backend: str = "redis://127.0.0.1:6379/0"
    aws_access_key_id: Optional[str] = None
    aws_access_secret_id: Optional[str] = None


class AWSConfig(Config):
    """AWS Config
    """
    aws_access_key_id: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_access_secret_id: Optional[str] = os.environ.get("AWS_ACCESS_SECRET_ID")
    broker_url: str = os.environ.get("AWS_BROKER_URL")
    result_backend: str = os.environ.get("AWS_RESULT_BACKEND")


class TestConfig(Config):
    """
    """
    TESTING: bool = True


class DockerComposeConfig(Config):
    """DEBUG is `true` since it's only used for development
    """
    DEBUG: bool = True
    broker_url: str = "redis://:redis_passwdd@redis"
    result_backend: str = "redis://:redis_passwdd@redis"


configs: Dict[str, Config] = {
    "dev": Config,
    "docker": DockerComposeConfig,
    "aws": AWSConfig,
    "test": TestConfig
}

environment: str = os.environ.get("APP_ENV", "dev")
