#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (setup, find_packages)

setup(
    name="science",
    version="0.1-alpha",
    description="REST API for Science",
    author="faruken",
    author_email="faruken@users.noreply.github.com",
    platforms="any",
    zip_safe=False,
    license="GPL3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Sanic :: 0.2",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="sanic rest api",
    packages=find_packages(
        exclude=["tests", "coverage", "html", "templates", "log"]),
    install_requires=[
        "aiofiles==0.3.0",
        "appdirs==1.4.0",
        "amqp==2.1.4",
        "billiard==3.5.0.2",
        "celery==4.0.2",
        "hiredis==0.2.0",
        "httptools==0.0.9",
        "Logbook==1.0.0",
        "kombu==4.0.2",
        "multidict==2.1.4",
        "packaging==16.8",
        "pyparsing==2.1.10",
        "pytz==2016.10",
        "redis==2.10.5",
        "Sanic==0.2.0",
        "six==1.10.0",
        "ujson==1.35",
        "uvloop==0.7.2",
        "vine==1.1.3"
    ],
    extras_require={
        "test": ["coverage==4.3.4", "pytest==3.0.5", "pytest-cov==2.4.0"],
        "dev": ["mypy-lang==0.4.6", "typed-ast==0.6.3"]
    },
    entry_points={
        "console_scripts": ["science=science.api:main"]
    }
)
