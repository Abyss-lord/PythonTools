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
from pythontools.core.convert.convertor import BasicConvertor
from pythontools.core.utils.datetimeutils import DatetimeUtil  # type: ignore
from pythontools.core.utils.reutils import ReUtil


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

        if _ := ReUtil.is_match(PatternPool.BIRTHDAY_PATTERN, birthday):
            year = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 1))
            month = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 3))
            day = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 5))
            return DatetimeUtil.is_valid_date(year, month, day)  # type: ignore
        return False
