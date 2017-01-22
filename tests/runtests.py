#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import unittest

import os
from logbook import Logger

import coverage

CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.join(CURRENT_DIR, "../.."))
sys.path.insert(0, BASE_DIR)
log = Logger(__name__)


def main() -> None:
    cov = coverage.coverage(
        cover_pylib=False,
        config_file=os.path.join(BASE_DIR, ".coveragerc"),
        include="{0}/*".format(BASE_DIR)
    )
    cov.start()
    log.info("Starting coverage.")
    test_suite = unittest.TestLoader().discover(start_dir=CURRENT_DIR,
                                                pattern="test_*.py")
    tests = unittest.TestSuite(test_suite)
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    log.info("Generating coverage HTML report.")
    cov.html_report()
    log.info("All finished.")


if __name__ == '__main__':
    main()
