#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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

import calendar
import datetime
import os
import platform
import time

from loguru import logger

from .context import Sex


class TestBasic(object):
    def test_basic(self):
        for root, dirs, files in os.walk(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        ):
            logger.info(f"{root=}, {dirs=}")

    def test_constant(self):
        assert Sex.MALE == Sex.get_sex(1)
        assert Sex.FEMALE == Sex.get_sex(2)

    def test_platform(self):
        logger.info(platform.platform())

    def test_sys(self):
        res = datetime.datetime.resolution * 1e6 * 60
        logger.info(res.seconds)

    def test_local_tz(self):
        offset_seconds = time.timezone
        offset_delta = datetime.timedelta(seconds=offset_seconds)
        tzinfo = datetime.timezone(offset_delta)
        logger.info(calendar.JANUARY)
        logger.info(tzinfo)
        logger.info(time.daylight)
