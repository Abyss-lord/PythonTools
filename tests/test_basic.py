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

import datetime
import os
import platform
import time
import warnings
from pathlib import Path

from loguru import logger


class TestBasic:
    def test_basic(self):
        for root, dirs, files in os.walk("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"):
            logger.info(f"{root=}, {dirs=}")

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

    def test_str_join(self):
        s = []
        res = "".join(s)
        logger.debug(f"res: {res}")
        logger.debug(type(res))

    def test_warning(self):
        with warnings.catch_warnings(record=True) as _:
            warnings.simplefilter("always")
            warnings.warn("This is a warning")
            logger.warning("This is a warning")

    def test_type(self):
        class SubTuple(tuple):
            pass

        a = SubTuple()
        logger.debug(type(a))
        logger.debug(type(a).__bases__[0] is tuple)

    def test_str_new_func(self):
        s = "hello\tworld"

        logger.debug(s.casefold())
        logger.debug(s.expandtabs())

    def test_type_t(self):
        s = "asb"
        logger.debug(type(s.__class__))

    def test_number_mro(self) -> None:
        from numbers import Number

        s = complex(4, 3)
        s = abs(s)
        logger.debug(s)
        logger.debug(isinstance(s, Number))
        logger.debug(isinstance(1.3, Number))
        logger.debug(isinstance(1, Number))

    def test_unicode_type(self):
        logger.debug(str)

        logger.debug(hex(pow(2, 128)))

    def test_path(self):
        res = Path("")
        logger.debug(res)
