#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_basic
   Description :
   date：          2024/7/16
-------------------------------------------------
   Change Activity:
                   2024/7/16:
-------------------------------------------------
"""
import calendar
import datetime
import os
import sys
import platform
import time

import pytz
from loguru import logger
from .context import Sex


class TestBasic(object):
    def test_basic(self):
        for root, dirs, files in os.walk(
                '/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools'):
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
