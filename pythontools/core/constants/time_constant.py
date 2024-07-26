#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   constant.py
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
import typing
from collections import namedtuple
from enum import Enum

QuarterTuple = namedtuple("QuarterTuple", ["name", "func", "val"])
TimeUnitTuple = namedtuple("TimeUnitTuple", ["desc", "unit_val_in_ns"])


class Quarter(Enum):
    Q1 = QuarterTuple("Q1", lambda x: 1 <= x.month <= 3, 1)
    Q2 = QuarterTuple("Q2", lambda x: 4 <= x.month <= 6, 2)
    Q3 = QuarterTuple("Q3", lambda x: 7 <= x.month <= 9, 3)
    Q4 = QuarterTuple("Q4", lambda x: 10 <= x.month <= 12, 4)

    @staticmethod
    def get_quarter(dt: datetime.datetime) -> "Quarter":
        for q in Quarter:
            if q.value.func(dt):
                return q

        raise KeyError


class TimeUnit(object):
    NANOSECONDS: typing.Final[TimeUnitTuple] = TimeUnitTuple("纳秒(ns)", 1)
    MICROSECONDS: typing.Final[TimeUnitTuple] = TimeUnitTuple("微秒(µs)", 1_000)
    MILLISECONDS: typing.Final[TimeUnitTuple] = TimeUnitTuple("毫秒(ms)", 1_000_000)
    SECONDS: typing.Final[TimeUnitTuple] = TimeUnitTuple("秒(s)", 1_000_000_000)
    MINUTES: typing.Final[TimeUnitTuple] = TimeUnitTuple("分钟(min)", 60_000_000_000)
    HOURS: typing.Final[TimeUnitTuple] = TimeUnitTuple("小时(h)", 3_600_000_000_000)

    @staticmethod
    def convert(value: int, from_unit: TimeUnitTuple, to_unit: TimeUnitTuple) -> float:
        """
        时间转换
        :param value: 时间标量
        :param from_unit: 转换前的时间单位
        :param to_unit: 转换后的时间单位
        :return: 转换后的时间标量
        """
        return value * from_unit.unit_val_in_ns / to_unit.unit_val_in_ns
