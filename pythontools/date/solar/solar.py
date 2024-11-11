#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   solar.py
@Date       :   2024/08/30
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/30
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from datetime import date, datetime

from pythontools.core.utils.basicutils import DatetimeUtil


class Solar:
    def __init__(self, year, month, day, hour=0, minute=0, second=0) -> None:
        if year == 1582 and month == 10 and 4 < day < 15:
            raise ValueError(f"wrong solar year:{year} month:{month} day:{day}")

        self.year = year
        self.month = DatetimeUtil.check_and_get_month(month)
        self.day = DatetimeUtil.check_and_get_day(year, month, day)
        self.hour = DatetimeUtil.check_and_get_hour(hour)
        self.minute = DatetimeUtil.check_and_get_minute(minute)
        self.second = DatetimeUtil.check_and_get_second(second)


class SolarCalendar:
    @classmethod
    def from_date(cls, dt: datetime | date) -> Solar:
        if isinstance(dt, date):
            dt = datetime(dt.year, dt.month, dt.day)
        return Solar(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    @classmethod
    def from_ymd(cls, year: int, month: int, day: int) -> Solar:
        return cls.from_date(datetime(year, month, day))

    @classmethod
    def from_ymdhms(cls, year: int, month: int, day: int, hour: int, minute: int, second: int) -> Solar:
        return cls.from_date(datetime(year, month, day, hour, minute, second))

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return False
