#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   baseformat.py
@Date       :   2024/09/06
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/06
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from abc import ABC
from datetime import UTC, date, datetime, timezone

from pythontools.date.format.datepattern import DatePattern


class BaseFormat(ABC):
    PATTERN: DatePattern = DatePattern.NORM_YEAR_PATTERN

    @classmethod
    def parse_date(
        cls,
        date_string: str,
        default_timezone: timezone | None = UTC,
    ) -> datetime:
        """
        解析日期字符串为 Datetime 对象

        Parameters
        ----------
        date_string : str
            待解析的日期字符串
        default_timezone : timezone | None, optional
            默认时区, 默认为UTC, by default UTC

        Returns
        -------
        datetime
            返回解析后的 datetime 对象
        """
        raise NotImplementedError()

    @classmethod
    def format_date(
        cls,
        date_obj: datetime | date,
    ) -> str:
        """
        格式化 :py:class:`datetime` 或者 :py:class:`date` 对象为字符串

        Parameters
        ----------
        date_obj : datetime | date
            待格式化对象

        Returns
        -------
        str
            返回格式化后的字符串
        """
        raise NotImplementedError()

    @classmethod
    def is_match(cls, date_string: str) -> bool:
        """
        判断当前日期格式是否匹配日期字符串

        Parameters
        ----------
        date_string : str
            日期字符串

        Returns
        -------
        bool
            如果匹配返回 True, 否则返回 False
        """
        raise NotImplementedError()

    @classmethod
    def get_pattern_string(cls) -> str:
        """
        返回当前日期格式的字符串表示

        Returns
        -------
        str
            当前日期格式的字符串表示
        """
        return cls.PATTERN.get_value()
