#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   iso8601.py
@Date       :   2024/09/03
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/03
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import datetime as dt_lib
from datetime import UTC, date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from pythontools.core.constants.pattern_pool import PatternPool
from pythontools.core.errors import DatetimeParseError
from pythontools.core.utils.basicutils import DatetimeUtil, ReUtil
from pythontools.core.validators.datetime_validator import DatetimeValidator
from pythontools.date.format.baseformat import BaseFormat
from pythontools.date.format.datepattern import DatePattern


class ISO8601(BaseFormat):
    PATTERN = DatePattern.ISO8601_PATTERN

    @classmethod
    def parse_timezone(
        cls,
        matches: dict[str, str],
        default_timezone: timezone | None = UTC,
    ) -> timezone | None:
        """
        将ISO 8601时区规范解析为tzinfo偏移量

        Parameters
        ----------
        matches : dict[str, str]
            匹配对象, :py:class:`Match`.groupdict()返回值
        default_timezone : timezone | None, optional
            默认时区, by default UTC

        Returns
        -------
        timezone | None
            时区偏移量
        """
        tz = matches.get("timezone")
        if tz == "Z":
            return UTC

        if tz is None:
            return default_timezone
        sign = matches.get("tz_sign")
        hours = int(matches.get("tz_hour", 0))
        minutes = int(matches.get("tz_minute", 0))
        description = f"{sign}{hours:02d}:{minutes:02d}"
        if sign == "-":
            hours = -hours
            minutes = -minutes
        return cls._FixedOffset(hours, minutes, description)

    @classmethod
    def parse_date(
        cls,
        date_string: str,
        default_timezone: timezone | None = UTC,
    ) -> datetime:
        """
        解析 ISO 8601 日期字符串为 datetime 对象

        Parameters
        ----------
        date_string : str
            ISO 8601 日期字符串
        default_timezone : timezone | None, optional
            没有时区信息时使用的时区, by default UTC

        Returns
        -------
        datetime
            完成解析后的 datetime 对象

        Raises
        ------
        DatetimeParseError
            如果日期字符串格式不正确则抛出该异常，
        """
        try:
            if not cls.is_match(date_string):
                raise DatetimeParseError(f"Invalid date string {date_string!r}")
        except Exception as e:
            raise DatetimeParseError from e

        groups: dict[str, Any] | None = ReUtil.get_match_group(PatternPool.ISO8601, date_string)

        if groups is None:
            return datetime(year=dt_lib.MINYEAR, month=1, day=1)
        groups = {k: v for k, v in groups.items() if v is not None}
        try:
            return datetime(
                year=int(groups.get("year", 0)),
                month=int(groups.get("month", groups.get("monthdash", 1))),
                day=int(groups.get("day", groups.get("daydash", 1))),
                hour=int(groups.get("hour", 0)),
                minute=int(groups.get("minute", 0)),
                second=int(groups.get("second", 0)),
                microsecond=int(Decimal(f"0.{groups.get('second_fraction', 0)}") * Decimal("1000000.0")),
                tzinfo=cls.parse_timezone(groups, default_timezone=default_timezone),
            )
        except Exception as e:
            raise DatetimeParseError from e

    @classmethod
    def format_date(
        cls,
        date_obj: datetime | date,
    ) -> str:
        """
        将 datetime 对象格式化为 ISO 8601 日期字符串

        Parameters
        ----------
        date_obj : datetime
            datetime 对象

        Returns
        -------
        str
            ISO 8601 日期字符串
        """
        datetime_obj = DatetimeUtil.get_cleaned_datetime(date_obj)
        if datetime_obj.tzinfo is None:
            date_obj = datetime_obj.replace(tzinfo=UTC)
        return date_obj.strftime(cls.get_pattern_string())

    @classmethod
    def _FixedOffset(
        cls,
        offset_hours: float,
        offset_minutes: float,
        name: str,
    ) -> timezone:
        return timezone(
            timedelta(
                hours=offset_hours,
                minutes=offset_minutes,
            ),
            name,
        )

    @classmethod
    def is_match(cls, date_string: str) -> bool:
        """
        判断给定的日期字符串是否匹配 ISO 8601 日期格式

        Parameters
        ----------
        date_string : str
            给定的日期字符串

        Returns
        -------
        bool
            如果匹配 ISO 8601 日期格式则返回 True，否则返回 False
        """
        return DatetimeValidator.is_iso8601_datetime(date_string)
