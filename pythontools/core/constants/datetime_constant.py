#!/usr/bin/env python
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
from typing import Optional

QuarterTuple = namedtuple(
    "QuarterTuple",
    [
        "name",
        "chinese_name",
        "val",
    ],
)
TimeUnitTuple = namedtuple("TimeUnitTuple", ["desc", "unit_val_in_ns"])
WeekTuple = namedtuple("WeekTuple", ["name", "chinese_name", "alias", "calendar_value", "iso8601_value"])
MonthTuple = namedtuple("MonthTuple", ["name", "chinese_name", "alias", "calendar_value"])


class Quarter(Enum):
    Q1 = QuarterTuple("Q1", "第一季度", 1)
    Q2 = QuarterTuple("Q2", "第二季度", 2)
    Q3 = QuarterTuple("Q3", "第三季度", 3)
    Q4 = QuarterTuple("Q4", "第四季度", 4)

    @classmethod
    def _get_quarter_by_month(cls, month: int) -> "Quarter":
        if month in {1, 2, 3}:
            return Quarter.Q1
        elif month in {4, 5, 6}:
            return Quarter.Q2
        elif month in {7, 8, 9}:
            return Quarter.Q3
        elif month in {10, 11, 12}:
            return Quarter.Q4
        else:
            raise ValueError("month must be in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]")

    @classmethod
    def _get_quarter_by_date(cls, dt: datetime.datetime) -> "Quarter":
        return cls._get_quarter_by_month(dt.month)

    @classmethod
    def get_quarter(cls, dt: datetime.datetime | int) -> "Quarter":
        if isinstance(dt, datetime.date):
            return cls._get_quarter_by_date(dt)
        elif isinstance(dt, int):
            return cls._get_quarter_by_month(dt)
        else:
            raise TypeError("dt must be datetime.datetime or int")

    def get_chinese_format(self) -> str:
        return self.value.chinese_name

    def get_name(self) -> str:
        return self.value.name

    def get_val(self) -> int:
        return self.value.val


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
        return duration * self.value.unit_val_in_ns // TimeUnit.MICROSECONDS.value.unit_val_in_ns

    def to_millis(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns // TimeUnit.MILLISECONDS.value.unit_val_in_ns

    def to_seconds(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns // TimeUnit.SECONDS.value.unit_val_in_ns

    def to_minutes(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns // TimeUnit.MINUTES.value.unit_val_in_ns

    def to_hours(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns // TimeUnit.HOURS.value.unit_val_in_ns

    def to_days(self, duration: int) -> int:
        return duration * self.value.unit_val_in_ns // TimeUnit.DAYS.value.unit_val_in_ns


class Week(Enum):
    MONDAY = WeekTuple("MONDAY", "星期一", "mon", calendar.MONDAY, 1)
    TUESDAY = WeekTuple("TUESDAY", "星期二", "tue", calendar.TUESDAY, 2)
    WEDNESDAY = WeekTuple("WEDNESDAY", "星期三", "wed", calendar.WEDNESDAY, 3)
    THURSDAY = WeekTuple("THURSDAY", "星期四", "thu", calendar.THURSDAY, 4)
    FRIDAY = WeekTuple("FRIDAY", "星期五", "fri", calendar.FRIDAY, 5)
    SATURDAY = WeekTuple("SATURDAY", "星期六", "sat", calendar.SATURDAY, 6)
    SUNDAY = WeekTuple("SUNDAY", "星期日", "sun", calendar.SUNDAY, 7)

    @classmethod
    def get_week(cls, name: int | str) -> Optional["Week"]:
        if isinstance(name, int):
            for week in cls:
                if week.get_iso8601_value() == name:
                    return week
        elif isinstance(name, str):
            if name.startswith("星期") or name.startswith("周"):
                last = name[-1]
                if chinese_format := cls._get_week_from_chinese_format(last):
                    return chinese_format
                if numerical_format := cls._get_week_from_numerical_format(int(last)):
                    return numerical_format
        else:
            raise TypeError("name must be int or str")

        return None

    def get_name(self) -> str:
        return self.value.name

    def get_value(self) -> int:
        return self.value.calendar_value

    def get_iso8601_value(self) -> int:
        return self.value.iso8601_value

    def get_chinese_format(self) -> str:
        return self.value.chinese_name

    def get_alias(self) -> str:
        return self.value.alias

    @classmethod
    def _get_week_from_chinese_format(cls, last_value: str) -> Optional["Week"]:
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
    def _get_week_from_numerical_format(cls, last_value: int) -> Optional["Week"]:
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


class Month(Enum):
    JANUARY = MonthTuple("JANUARY", "一月", "jan", 1)
    FEBRUARY = MonthTuple("FEBRUARY", "二月", "feb", 2)
    MARCH = MonthTuple("MARCH", "三月", "mar", 3)
    APRIL = MonthTuple("APRIL", "四月", "apr", 4)
    MAY = MonthTuple("MAY", "五月", "may", 5)
    JUNE = MonthTuple("JUNE", "六月", "jun", 6)
    JULY = MonthTuple("JULY", "七月", "jul", 7)
    AUGUST = MonthTuple("AUGUST", "八月", "aug", 8)
    SEPTEMBER = MonthTuple("SEPTEMBER", "九月", "sep", 9)
    OCTOBER = MonthTuple("OCTOBER", "十月", "oct", 10)
    NOVEMBER = MonthTuple("NOVEMBER", "十一月", "nov", 11)
    DECEMBER = MonthTuple("DECEMBER", "十二月", "dec", 12)

    @classmethod
    def get_month(cls, name: int | str) -> "Month":
        if isinstance(name, int):
            for month in cls:
                if month.get_value() == name:
                    return month

            raise ValueError(f"Invalid month value: {name}")
        elif isinstance(name, str):
            if name.endswith("月"):
                month_expression, _, _ = name.partition("月")
                if month_obj := cls._get_month_from_chinese_format(month_expression):
                    return month_obj
                if month_obj := cls._get_month_from_numerical_format(month_expression):
                    return month_obj

            raise ValueError(f"Invalid month name: {name}")

        raise TypeError("name must be int or str")

    def get_value(self) -> int:
        return self.value.calendar_value

    def get_name(self) -> str:
        return self.value.name

    def get_chinese_format(self) -> str:
        return self.value.chinese_name

    def get_alias(self) -> str:
        return self.value.alias

    def get_last_day(self, year: int) -> int:
        month = self.get_value()
        if month == 2:
            return 29 if calendar.isleap(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    @classmethod
    def _get_month_from_chinese_format(cls, value: str) -> Optional["Month"]:
        if value == "一":
            return Month.JANUARY
        elif value == "二":
            return Month.FEBRUARY
        elif value == "三":
            return Month.MARCH
        elif value == "四":
            return Month.APRIL
        elif value == "五":
            return Month.MAY
        elif value == "六":
            return Month.JUNE
        elif value == "七":
            return Month.JULY
        elif value == "八":
            return Month.AUGUST
        elif value == "九":
            return Month.SEPTEMBER
        elif value == "十":
            return Month.OCTOBER
        elif value == "十一":
            return Month.NOVEMBER
        elif value == "十二":
            return Month.DECEMBER
        else:
            return None

    @classmethod
    def _get_month_from_numerical_format(cls, value: str) -> Optional["Month"]:
        if value == "1":
            return Month.JANUARY
        elif value == "2":
            return Month.FEBRUARY
        elif value == "3":
            return Month.MARCH
        elif value == "4":
            return Month.APRIL
        elif value == "5":
            return Month.MAY
        elif value == "6":
            return Month.JUNE
        elif value == "7":
            return Month.JULY
        elif value == "8":
            return Month.AUGUST
        elif value == "9":
            return Month.SEPTEMBER
        elif value == "10":
            return Month.OCTOBER
        elif value == "11":
            return Month.NOVEMBER
        elif value == "12":
            return Month.DECEMBER
        else:
            return None
