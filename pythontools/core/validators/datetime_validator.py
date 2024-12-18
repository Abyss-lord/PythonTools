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


from pythontools.core.constants.pattern_pool import PatternPool
from pythontools.core.utils.basic_utils import (
    ReUtil,
)
from pythontools.core.utils.datetime_utils import DatetimeUtil


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

        return DatetimeUtil.is_valid_birthday(birthday)

    @classmethod
    def is_iso8601_datetime(cls, datetime_str: str) -> bool:
        """
        验证是否为ISO8601格式的日期时间字符串

        Example:
        ----------
        >>> Validator.is_iso8601_datetime('2021-01-01T12:00:00Z') # returns True
        >>> Validator.is_iso8601_datetime('2021-01-01T12:00:00+08:00') # returns True
        >>> Validator.is_iso8601_datetime('2021-01-01T12:00:00') # returns True
        >>> Validator.is_iso8601_datetime('2021-01-01 12:00:00') # returns False

        Parameters
        ----------
        datetime_str : str
            待检测日期时间字符串

        Returns
        -------
        bool
            如果是合法的ISO8601格式的日期时间字符串, 则返回True, 否则返回False
        """

        return bool(_ := ReUtil.is_match(PatternPool.ISO8601, datetime_str))

    @classmethod
    def is_rfc822_datetime(cls, datetime_str: str) -> bool:
        """
        验证是否为RFC822格式的日期时间字符串

        Example:
        ----------
        >>> Validator.is_rfc822_datetime('Thu, 01 Jan 2021 12:00:00 GMT') # returns True
        >>> Validator.is_rfc822_datetime('Thu, 01 Jan 2021 12:00:00 +0800') # returns True
        >>> Validator.is_rfc822_datetime('Thu, 01 Jan 2021 12:00:00') # returns True
        >>> Validator.is_rfc822_datetime('Thu, 01 Jan 2021 12:00:00 +08:00') # returns False

        Parameters
        ----------
        datetime_str : str
            待检测日期时间字符串

        Returns
        -------
        bool
            如果是合法的RFC822格式的日期时间字符串, 则返回True, 否则返回False
        """

        return bool(_ := ReUtil.is_match(PatternPool.RFC822, datetime_str))
