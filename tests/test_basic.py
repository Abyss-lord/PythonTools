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

import datetime
import os
import platform
import time

import pytest
from loguru import logger

from .context import Gender, Quarter


class TestBasic(object):
    def test_basic(self):
        for root, dirs, files in os.walk(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        ):
            logger.info(f"{root=}, {dirs=}")

    def test_constant(self):
        assert Gender.MALE == Gender.get_gender_by_code(1)
        assert Gender.FEMALE == Gender.get_gender_by_code(2)

    def test_platform(self):
        logger.info(platform.platform())

    def test_sys(self):
        res = datetime.datetime.resolution * 1e6 * 60
        logger.info(res.seconds)

    def test_local_tz(self):
        offset_seconds = time.timezone
        offset_delta = datetime.timedelta(seconds=offset_seconds)
        tzinfo = datetime.timezone(offset_delta)

        logger.info(tzinfo)
        logger.info(time.daylight)

    def test_context(self):
        s = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/README.md"
        with open(s, "rb") as f:
            logger.info(type(f))

    def test_sys_args(self):
        pass


class TestQuarterObject:
    def __init__(self, month: int) -> None:
        self.month = month


class TestConstant:
    @classmethod
    def test_get_quarter_with_incorrect_arguments(cls) -> None:
        incorrect_obj = TestQuarterObject(13)
        with pytest.raises(KeyError):
            Quarter.get_quarter(incorrect_obj)
