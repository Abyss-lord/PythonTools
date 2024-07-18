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
import datetime
import os

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
