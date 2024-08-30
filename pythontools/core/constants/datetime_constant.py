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
from collections import namedtuple
from datetime import date, datetime
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

    @staticmethod
    def get_max_value() -> int:
        return Quarter.Q4.get_value()

    @staticmethod
    def get_min_value() -> int:
        return Quarter.Q1.get_value()

    @classmethod
    def get_quarter(cls, dt: datetime | int | str) -> Optional["Quarter"]:
        """
        根据给定的整数、日期或字符串，获取对应的季度

        Example:
        -------
        >>> Quarter.get_quarter(1)
        <Quarter.Q1: QuarterTuple(name='Q1', chinese_name='第一季度', val=1)>
        >>> Quarter.get_quarter("1")
        <Quarter.Q1: QuarterTuple(name='Q1', chinese_name='第一季度', val=1)>
        >>> Quarter.get_quarter("第一季度")
        <Quarter.Q1: QuarterTuple(name='Q1', chinese_name='第一季度', val=1)>
        >>> Quarter.get_quarter(datetime(2024, 1, 1))
        <Quarter.Q1: QuarterTuple(name='Q1', chinese_name='第一季度', val=1)>

        Parameters
        ----------
        dt : datetime | int | str
            日期或整数或字符串

        Returns
        -------
        Quarter 枚举实例
            Quarter枚举实例, 如果参数错误则返回None

        Raises
        ------
        TypeError
            如果给定参数类型错误, 则抛出TypeError异常
        """
        if isinstance(dt, date):
            return cls._get_quarter_by_date(dt)
        elif isinstance(dt, int):
            return cls._get_quarter_by_month(dt)
        elif isinstance(dt, str):
            return cls._get_quarter_by_name(dt)
        else:
            raise TypeError("dt must be datetime or int or str")

    @classmethod
    def is_valid_quarter(cls, quarter: int) -> bool:
        """
        检查给定的季度是否有效

        Example:
        -------
        >>> Quarter.is_valid_quarter(1)
        True
        >>> Quarter.is_valid_quarter(5)
        False

        Parameters
        ----------
        quarter : int
            季度数字

        Returns
        -------
        bool
            True: 有效, False: 无效
        """
        return Quarter.get_min_value() <= quarter <= Quarter.get_max_value()

    def get_chinese_format(self) -> str:
        """
        获取季度中文名称

        Example:
        -------
        >>> Quarter.Q1.get_chinese_format()
        '第一季度'
        >>> Quarter.Q2.get_chinese_format()
        '第二季度'
        >>> Quarter.Q3.get_chinese_format()
        '第三季度'
        >>> Quarter.Q4.get_chinese_format()
        '第四季度'

        Returns
        -------
        str
            季度的中文名称
        """
        return self.value.chinese_name

    def get_name(self) -> str:
        """
        获取季度的英文名称

        Example:
        -------
        >>> Quarter.Q1.get_name()
        'Q1'
        >>> Quarter.Q2.get_name()
        'Q2'
        >>> Quarter.Q3.get_name()
        'Q3'
        >>> Quarter.Q4.get_name()
        'Q4'

        Returns
        -------
        str
            表示季度的英文名称
        """
        return self.value.name

    def get_value(self) -> int:
        """
        获取季度值

        Example:
        -------
        >>> Quarter.Q1.get_value()
        1
        >>> Quarter.Q2.get_value()
        2
        >>> Quarter.Q3.get_value()
        3
        >>> Quarter.Q4.get_value()
        4

        Returns
        -------
        int
            季度值
        """
        return self.value.val

    def is_first_quarter(self) -> bool:
        """
        判断当前季度是否为第一季度

        Example:
        -------
        >>> Quarter.Q1.is_first_quarter()
        True
        >>> Quarter.Q2.is_first_quarter()
        False
        >>> Quarter.Q3.is_first_quarter()
        False
        >>> Quarter.Q4.is_first_quarter()
        False

        Returns
        -------
        bool
            True: 当前季度为第一季度, False: 当前季度不是第一季度
        """
        return self == Quarter.Q1

    def is_last_quarter(self) -> bool:
        """
        判断当前季度是否为最后一季度

        Example:
        -------
        >>> Quarter.Q1.is_last_quarter()
        False
        >>> Quarter.Q2.is_last_quarter()
        False
        >>> Quarter.Q3.is_last_quarter()
        False
        >>> Quarter.Q4.is_last_quarter()
        True

        Returns
        -------
        bool
            True: 当前季度为最后一季度, False: 当前季度不是最后一季度
        """
        return self == Quarter.Q4

    @classmethod
    def _get_quarter_by_name(cls, name: str) -> Optional["Quarter"]:
        if name.endswith("季度"):
            return cls._get_quarter_by_cn_quarter_name(name)
        elif name.startswith("q") or name.startswith("Q"):
            return cls._get_quarter_by_en_quarter_name(name)

        return None

    @classmethod
    def _get_quarter_by_month(cls, month: int) -> Optional["Quarter"]:
        if month in {1, 2, 3}:
            return Quarter.Q1
        elif month in {4, 5, 6}:
            return Quarter.Q2
        elif month in {7, 8, 9}:
            return Quarter.Q3
        elif month in {10, 11, 12}:
            return Quarter.Q4
        else:
            return None

    @classmethod
    def _get_quarter_by_en_quarter_name(cls, quarter_name: str) -> Optional["Quarter"]:
        if len(quarter_name) != 2:
            return None
        quarter_val = quarter_name[-1]
        if quarter_val == "1":
            return Quarter.Q1
        elif quarter_val == "2":
            return Quarter.Q2
        elif quarter_val == "3":
            return Quarter.Q3
        elif quarter_val == "4":
            return Quarter.Q4

        return None

    @classmethod
    def _get_quarter_by_cn_quarter_name(cls, quarter_name: str) -> Optional["Quarter"]:
        quarter_name = quarter_name.removeprefix("第")
        quarter_val, _, _ = quarter_name.partition("季度")
        if quarter_val in {"一", "1"}:
            return Quarter.Q1
        elif quarter_val in {"二", "2"}:
            return Quarter.Q2
        elif quarter_val in {"三", "3"}:
            return Quarter.Q3
        elif quarter_val in {"四", "4"}:
            return Quarter.Q4

        return None

    @classmethod
    def _get_quarter_by_date(cls, dt: datetime) -> Optional["Quarter"]:
        return cls._get_quarter_by_month(dt.month)


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

    @staticmethod
    def get_max_value() -> int:
        return Month.DECEMBER.get_value()

    @staticmethod
    def get_min_value() -> int:
        return Month.JANUARY.get_value()

    @classmethod
    def get_month(cls, name: int | str | datetime) -> Optional["Month"]:
        """
        根据给定的参数获取月枚举实例

        Example:
        -------
        >>> Month.get_month(1)
        <Month.JANUARY: MonthTuple(name='JANUARY', chinese_name='一月', alias='jan', calendar_value=1)>
        >>> Month.get_month("1")
        <Month.JANUARY: MonthTuple(name='JANUARY', chinese_name='一月', alias='jan', calendar_value=1)>
        >>> Month.get_month("一月")
        <Month.JANUARY: MonthTuple(name='JANUARY', chinese_name='一月', alias='jan', calendar_value=1)>
        >>> Month.get_month(datetime(2024, 1, 1))
        <Month.JANUARY: MonthTuple(name='JANUARY', chinese_name='一月', alias='jan', calendar_value=1)>


        Parameters
        ----------
        name : int | str | datetime
            整数、字符串或日期对象

        Returns
        -------
        Month 枚举实例
            Month枚举实例, 如果参数错误则返回None


        Raises
        ------
        TypeError
            如果给定的参数类型错误, 则抛出TypeError异常
        """
        if isinstance(name, int):
            return cls._get_month_by_number(name)
        elif isinstance(name, str):
            return cls._get_month_by_string(name)
        elif isinstance(name, datetime):
            return cls._get_month_by_date(name)
        else:
            raise TypeError("name must be int or str")

    @classmethod
    def is_valid_month(cls, month: int) -> bool:
        """
        检查给定的月份是否有效

        Example:
        -------
        >>> Month.check_valid_month(1)
        True
        >>> Month.check_valid_month(13)
        False

        Parameters
        ----------
        month : int
            月份数字

        Returns
        -------
        bool
            True: 有效, False: 无效
        """
        return Month.get_min_value() <= month <= Month.get_max_value()

    def get_name(self) -> str:
        """
        获取月份枚举的完整英文名称

        Returns
        -------
        str
            表示月份枚举的完整英文名称
        """
        return self.value.name

    def get_chinese_format(self) -> str:
        """
        获取表示月份的中文名称

        Returns
        -------
        str
            表示月份的中文名称
        """
        return self.value.chinese_name

    def get_alias(self) -> str:
        """
        表示月份的英文简称

        Returns
        -------
        str
            表示月份的英文简称
        """
        return self.value.alias

    def get_value(self) -> int:
        """
        返回月份的数字表示

        Returns
        -------
        int
            月份的数字表示
        """
        return self.value.calendar_value

    def get_last_day(self, year: int | datetime) -> int:
        """
        返回给定年份的该月份的天数

        Parameters
        ----------
        year : int
            给定的年

        Returns
        -------
        int
            给定年份的该月的天数
        """

        if isinstance(year, datetime):
            year = year.year

        return self._get_last_day_of_month_by_number(year)

    def is_first_month(self) -> bool:
        """
        判断当前月份是否为第一月

        Returns
        -------
        bool
            True: 当前月份为第一月, False: 当前月份不是第一月
        """
        return self == Month.JANUARY

    def is_last_month(self) -> bool:
        """
        判断当前月份是否为最后一月

        Returns
        -------
        bool
            True: 当前月份为最后一月, False: 当前月份不是最后一月
        """
        return self == Month.DECEMBER

    def _get_last_day_of_month_by_number(self, year: int) -> int:
        month = self.get_value()
        if month == 2:
            return 29 if calendar.isleap(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    @classmethod
    def _get_month_by_date(cls, dt: datetime) -> Optional["Month"]:
        return cls._get_month_by_numerical_string(f"{dt.month}")

    @classmethod
    def _get_month_by_string(cls, name: str) -> Optional["Month"]:
        if not name.endswith("月"):
            return cls._get_month_by_alias_or_total_name(name)

        month_expression, _, _ = name.partition("月")
        return cls._get_month_by_numerical_string(month_expression)

    @classmethod
    def _get_month_by_alias_or_total_name(cls, name: str) -> Optional["Month"]:
        name = name.lower().strip()
        return next(
            (obj for obj in Month if obj.get_alias().lower() == name or obj.get_name().lower() == name),
            None,
        )

    @classmethod
    def _get_month_by_number(cls, month_number: int) -> Optional["Month"]:
        return cls._get_month_by_numerical_string(f"{month_number}")

    @classmethod
    def _get_month_by_numerical_string(cls, s: str) -> Optional["Month"]:
        if s in {"1", "一"}:
            return Month.JANUARY
        elif s in {"2", "二"}:
            return Month.FEBRUARY
        elif s in {"3", "三"}:
            return Month.MARCH
        elif s in {"4", "四"}:
            return Month.APRIL
        elif s in {"5", "五"}:
            return Month.MAY
        elif s in {"6", "六"}:
            return Month.JUNE
        elif s in {"7", "七"}:
            return Month.JULY
        elif s in {"8", "八"}:
            return Month.AUGUST
        elif s in {"9", "九"}:
            return Month.SEPTEMBER
        elif s in {"10", "十"}:
            return Month.OCTOBER
        elif s in {"11", "十一"}:
            return Month.NOVEMBER
        elif s in {"12", "十二"}:
            return Month.DECEMBER
        else:
            return None


class Week(Enum):
    MONDAY = WeekTuple("MONDAY", "一", "mon", calendar.MONDAY, 1)
    TUESDAY = WeekTuple("TUESDAY", "二", "tue", calendar.TUESDAY, 2)
    WEDNESDAY = WeekTuple("WEDNESDAY", "三", "wed", calendar.WEDNESDAY, 3)
    THURSDAY = WeekTuple("THURSDAY", "四", "thu", calendar.THURSDAY, 4)
    FRIDAY = WeekTuple("FRIDAY", "五", "fri", calendar.FRIDAY, 5)
    SATURDAY = WeekTuple("SATURDAY", "六", "sat", calendar.SATURDAY, 6)
    SUNDAY = WeekTuple("SUNDAY", "日", "sun", calendar.SUNDAY, 7)

    @staticmethod
    def get_max_value() -> int:
        return Week.SUNDAY.get_iso8601_value()

    @staticmethod
    def get_min_value() -> int:
        return Week.MONDAY.get_iso8601_value()

    @classmethod
    def get_week(cls, name: int | str | datetime) -> Optional["Week"]:
        """
        根据给定的参数获取周枚举实例

        Example:
        -------
        >>> Week.get_week(1)
        <Week.MONDAY: WeekTuple(name='MONDAY', chinese_name='一', alias='mon', calendar_value=1, iso8601_value=1)>
        >>> Week.get_week("1")
        <Week.MONDAY: WeekTuple(name='MONDAY', chinese_name='一', alias='mon', calendar_value=1, iso8601_value=1)>
        >>> Week.get_week("一")
        <Week.MONDAY: WeekTuple(name='MONDAY', chinese_name='一', alias='mon', calendar_value=1, iso8601_value=1)>
        >>> Week.get_week(datetime(2024, 1, 1))
        <Week.MONDAY: WeekTuple(name='MONDAY', chinese_name='一', alias='mon', calendar_value=1, iso8601_value=1)>

        Parameters
        ----------
        name : int | str | datetime
            整数、字符串或日期对象

        Returns
        -------
        Week 枚举实例
            Week枚举实例, 如果参数错误则返回None

        Raises
        ------
        TypeError
            如果给定的参数类型错误, 则抛出TypeError异常
        """
        if isinstance(name, int):
            return cls._get_week_by_number(name)
        elif isinstance(name, str):
            return cls._get_week_by_string(name)
        elif isinstance(name, datetime):
            return cls._get_week_by_date(name)
        else:
            raise TypeError("name must be int or str")

    @classmethod
    def is_valid_weekday(cls, weekday: int) -> bool:
        """
        检查给定的星期是否有效

        Example:
        -------
        >>> Week.is_valid_weekday(1)
        True
        >>> Week.is_valid_weekday(8)
        False

        Parameters
        ----------
        weekday : int
            星期数字

        Returns
        -------
        bool
            True: 有效, False: 无效
        """
        return Week.get_min_value() <= weekday <= Week.get_max_value()

    def get_name(self) -> str:
        """
        获取周枚举的完整英文名称

        Returns
        -------
        str
            周枚举的完整英文名称
        """
        return self.value.name

    def get_value(self) -> int:
        """
        返回calendar模块中表示周的数字表示

        Returns
        -------
        int
            calendar模块中表示周的数字表示
        """
        return self.value.calendar_value

    def get_iso8601_value(self) -> int:
        """
        返回 ISO 8601 标准中表示周的数字表示

        Returns
        -------
        int
            ISO 8601 标准中表示周的数字表示
        """
        return self.value.iso8601_value

    def get_chinese_format(self, prefix: str = "星期") -> str:
        """
        根据给定的前缀返回表示周的中文名称

        Example:
        -------
        >>> Week.MONDAY.get_chinese_format()
        '星期一'
        >>> Week.TUESDAY.get_chinese_format()
        '星期二'
        >>> Week.Monday.get_chinese_format("周")
        '周一'

        Parameters
        ----------
        prefix : str, optional
            前缀, by default "星期"

        Returns
        -------
        str
            表示周的中文名称
        """
        return prefix + self.value.chinese_name

    def get_alias(self) -> str:
        """
        返回表示周的英文简称

        Returns
        -------
        str
            表示周的英文简称
        """
        return self.value.alias

    def is_first_day_of_week(self) -> bool:
        """
        判断当前星期是否为星期一

        Returns
        -------
        bool
            True: 当前星期为星期一, False: 当前星期不是星期一
        """
        return self == Week.MONDAY

    def is_last_day_of_week(self) -> bool:
        """
        判断当前星期是否为星期日

        Returns
        -------
        bool
            True: 当前星期为星期日, False: 当前星期不是星期日
        """
        return self == Week.SUNDAY

    @classmethod
    def _get_week_by_date(cls, dt: datetime) -> Optional["Week"]:
        return cls._get_week_by_number(dt.weekday() + 1)

    @classmethod
    def _get_week_by_string(cls, name: str) -> Optional["Week"]:
        if name.startswith("星期") or name.startswith("周"):
            return cls._get_week_by_numerical_string(name[-1])
        else:
            return cls._get_week_by_alias_or_total_name(name)

    @classmethod
    def _get_week_by_alias_or_total_name(cls, name: str) -> Optional["Week"]:
        name = name.lower().strip()
        return next(
            (obj for obj in Week if obj.get_alias().lower() == name or obj.get_name().lower() == name),
            None,
        )

    @classmethod
    def _get_week_by_number(cls, last_value: int) -> Optional["Week"]:
        return cls._get_week_by_numerical_string(str(last_value))

    @classmethod
    def _get_week_by_numerical_string(cls, last_value: str) -> Optional["Week"]:
        if last_value in {"一", "1"}:
            return Week.MONDAY
        elif last_value in {"二", "2"}:
            return Week.TUESDAY
        elif last_value in {"三", "3"}:
            return Week.WEDNESDAY
        elif last_value in {"四", "4"}:
            return Week.THURSDAY
        elif last_value in {"五", "5"}:
            return Week.FRIDAY
        elif last_value in {"六", "6"}:
            return Week.SATURDAY
        elif last_value in {"日", "7"}:
            return Week.SUNDAY
        else:
            return None


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
