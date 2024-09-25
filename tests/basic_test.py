#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_basic.py
@Date       :   2024/07/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib

import platform

from loguru import logger


class TestBasic:
    def test_platform(self):
        logger.info(platform.system())
