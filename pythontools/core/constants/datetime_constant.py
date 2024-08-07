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

import calendar
import datetime
from collections import namedtuple
from enum import Enum

QuarterTuple = namedtuple(
    "QuarterTuple",
    [
        "name",
        "chinese_name",
        "func",
        "val",
    ],
)
TimeUnitTuple = namedtuple("TimeUnitTuple", ["desc", "unit_val_in_ns"])
WeekTuple = namedtuple(
    "WeekTuple", ["name", "chinese_name", "alias", "calendar_value", "iso8601_value"]
)
MonthTuple = namedtuple(
    "MonthTuple", ["name", "chinese_name", "alias", "calendar_value"]
)


class Quarter(Enum):
    Q1 = QuarterTuple("Q1", "第一季度", lambda x: 1 <= x.month <= 3, 1)
    Q2 = QuarterTuple("Q2", "第二季度", lambda x: 4 <= x.month <= 6, 2)
    Q3 = QuarterTuple("Q3", "第三季度", lambda x: 7 <= x.month <= 9, 3)
    Q4 = QuarterTuple("Q4", "第四季度", lambda x: 10 <= x.month <= 12, 4)

    @staticmethod
    def get_quarter(dt: datetime.datetime) -> "Quarter":
        for q in Quarter:
            if q.value.func(dt):
                return q

        raise KeyError

    @staticmethod
    def get_chinese_format(quarter: "Quarter") -> str:
        return quarter.value.chinese_name


class TimeUnit(Enum):
    NANOSECONDS = TimeUnitTuple("纳秒(ns)", 1)
    MICROSECONDS = TimeUnitTuple("微秒(µs)", 1000 * NANOSECONDS.unit_val_in_ns)
    MILLISECONDS = TimeUnitTuple("毫秒(ms)", 1000 * MICROSECONDS.unit_val_in_ns)
    SECONDS = TimeUnitTuple("秒(s)", 1000 * MILLISECONDS.unit_val_in_ns)
    MINUTES = TimeUnitTuple("分钟(min)", 60 * SECONDS.unit_val_in_ns)
    HOURS = TimeUnitTuple("小时(h)", 60 * MINUTES.unit_val_in_ns)
    DAYS = TimeUnitTuple("天(d)", 24 * HOURS.unit_val_in_ns)

    def to_nanos(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns

    def to_micros(self, duration: int) -> int:
        return (
            duration
            * self.value.unit_val_in_ns
            // TimeUnit.MICROSECONDS.value.unit_val_in_ns
        )

    def to_millis(self, duration: int) -> int:
        return (
            duration
            * self.value.unit_val_in_ns
            // TimeUnit.MILLISECONDS.value.unit_val_in_ns
        )

    def to_seconds(self, duration: int) -> int:
        return (
            duration
            * self.value.unit_val_in_ns
            // TimeUnit.SECONDS.value.unit_val_in_ns
        )

    def to_minutes(self, duration: int) -> int:
        return (
            duration
            * self.value.unit_val_in_ns
            // TimeUnit.MINUTES.value.unit_val_in_ns
        )

    def to_hours(self, duration: int) -> int:
        return (
            duration * self.value.unit_val_in_ns // TimeUnit.HOURS.value.unit_val_in_ns
        )

    def to_days(self, duration: int) -> int:
        return (
            duration * self.value.unit_val_in_ns // TimeUnit.DAYS.value.unit_val_in_ns
        )


class Week(Enum):
    MONDAY = WeekTuple("MONDAY", "星期一", "mon", calendar.MONDAY, 1)
    TUESDAY = WeekTuple("TUESDAY", "星期二", "tue", calendar.TUESDAY, 2)
    WEDNESDAY = WeekTuple("WEDNESDAY", "星期三", "wed", calendar.WEDNESDAY, 3)
    THURSDAY = WeekTuple("THURSDAY", "星期四", "thu", calendar.THURSDAY, 4)
    FRIDAY = WeekTuple("FRIDAY", "星期五", "fri", calendar.FRIDAY, 5)
    SATURDAY = WeekTuple("SATURDAY", "星期六", "sat", calendar.SATURDAY, 6)
    SUNDAY = WeekTuple("SUNDAY", "星期日", "sun", calendar.SUNDAY, 7)

    @classmethod
    def get_week(cls, name: int | str) -> "Week" | None:
        if isinstance(name, int):
            for week in cls:
                if week.get_iso8601_value() == name:
                    return week
        elif isinstance(name, str):
            if name.startswith("星期") or name.startswith("周"):
                last = name[-1]
                chinese_format = cls._get_week_from_chinese_format(last)
                if chinese_format:
                    return chinese_format
                numerical_format = cls._get_week_from_numerical_format(int(last))
                if numerical_format:
                    return numerical_format
        else:
            raise TypeError("name must be int or str")

    def get_value(self) -> int:
        return self.value.calendar_value

    def get_iso8601_value(self) -> int:
        return self.value.iso8601_value

    def get_chinese_format(self) -> str:
        return self.value.chinese_name

    def get_alias(self) -> str:
        return self.value.alias

    @classmethod
    def _get_week_from_chinese_format(cls, last_value: str) -> "Week" | None:
        if last_value == "一":
            return Week.MONDAY
        elif last_value == "二":
            return Week.TUESDAY
        elif last_value == "三":
            return Week.WEDNESDAY
        elif last_value == "四":
            return Week.THURSDAY
        elif last_value == "五":
            return Week.FRIDAY
        elif last_value == "六":
            return Week.SATURDAY
        elif last_value == "日":
            return Week.SUNDAY
        else:
            return None

    @classmethod
    def _get_week_from_numerical_format(cls, last_value: int) -> "Week" | None:
        if last_value == 1:
            return Week.MONDAY
        elif last_value == 2:
            return Week.TUESDAY
        elif last_value == 3:
            return Week.WEDNESDAY
        elif last_value == 4:
            return Week.THURSDAY
        elif last_value == 5:
            return Week.FRIDAY
        elif last_value == 6:
            return Week.SATURDAY
        elif last_value == 7:
            return Week.SUNDAY
        else:
            return None
