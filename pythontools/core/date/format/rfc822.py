#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   rfc822.py
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
from datetime import UTC, date, datetime, timezone

from pythontools.core.date.format.baseformat import BaseFormat
from pythontools.core.date.format.datepattern import DatePattern
from pythontools.core.errors import DatetimeParseError
from pythontools.core.utils.datetimeutils import DatetimeUtil
from pythontools.core.validators.datetime_validator import DatetimeValidator


class RFC822(BaseFormat):
    """
    RFC 822 格式


    """

    PATTERN = DatePattern.RFC822_PATTERN

    @classmethod
    def parse_date(cls, date_string: str, default_timezone: timezone | None = None) -> datetime:
        try:
            if not cls.is_match(date_string):
                raise DatetimeParseError(f"Invalid date string {date_string!r}")
        except Exception as e:
            raise DatetimeParseError from e

        return (
            datetime.strptime(date_string, cls.get_pattern_string())
            if default_timezone is None
            else datetime.strptime(date_string, cls.get_pattern_string()).astimezone(default_timezone)
        )

    @classmethod
    def format_date(cls, date_obj: datetime | date) -> str:
        datetime_obj = DatetimeUtil.get_cleaned_datetime(date_obj)
        if datetime_obj.tzinfo is None:
            date_obj = datetime_obj.replace(tzinfo=UTC)

        return datetime_obj.strftime(cls.PATTERN.get_value())

    @classmethod
    def is_match(cls, date_string: str) -> bool:
        return DatetimeValidator.is_rfc822_datetime(date_string)
