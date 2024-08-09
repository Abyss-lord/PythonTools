#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   validator.py
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

__all__ = ["DatetimeValidator"]

import datetime

from ..basicutils import DatetimeUtil
from ..convert.convertor import BasicConvertor
from ..pattern_pool import PatternPool


class DatetimeValidator:
    @classmethod
    def is_valid_birthday(cls, birthday: str) -> bool:
        """
        验证是否为生日, 目前支持yyyy-MM-dd、yyyyMMdd、yyyy/MM/dd、yyyy.MM.dd、yyyy年MM月dd日

        Example:
        ----------
        >>> Validator.is_valid_birthday('1990-01-01') # returns True
        >>> Validator.is_valid_birthday('19900101') # returns True
        >>> Validator.is_valid_birthday('1990/01/01') # returns True
        >>> Validator.is_valid_birthday('1990.01.01') # returns True
        >>> Validator.is_valid_birthday('1990年01月01日') # returns True
        >>> Validator.is_valid_birthday('1990-13-01') # returns False
        >>> Validator.is_valid_birthday('1990-02-29') # returns False (非闰年)
        >>> Validator.is_valid_birthday('1990-02-30') # returns False (非30天的月份)

        Parameters
        ----------
        birthday : str
            待检测日期

        Returns
        -------
        bool
            如果是合法的生日, 则返回True, 否则返回False
        """

        # PERF 增加更多支持的日期格式
        matched = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        if matched:
            year = BasicConvertor.to_int(matched.group(1))
            month = BasicConvertor.to_int(matched.group(3))
            day = BasicConvertor.to_int(matched.group(5))
            return cls.is_valid_date(year, month, day)  # type: ignore
        return False

    @classmethod
    def is_valid_date(cls, year: int, month: int, day: int) -> bool:
        """
        验证是否为生日

        Example:
        ----------
        >>> Validator.is_valid_date(1990, 1, 1) # returns True
        >>> Validator.is_valid_date(1990, 13, 1) # returns False

        Parameters
        ----------
        year : int
            年
        month : int
            月
        day : int
            日

        Returns
        -------
        bool
            如果是合法的日期, 则返回True, 否则返回False
        """
        # 判断年
        # NOTE datetime.MINYEAR的值是1, 这里的逻辑是否要修改
        if year < datetime.MINYEAR or year > DatetimeUtil.this_year():
            return False

        # 判断月
        if month < 1 or month > 12:
            return False

        # 单独判断天
        if day < 1 or day > 31:
            return False

        # 处理30天的月
        if day > 30 and month in [4, 6, 9, 11]:
            return False

        # 处理闰年的情况
        if month == 2:
            return day < 29 or (day < 30 and DatetimeUtil.is_leap_year(year))

        return True
