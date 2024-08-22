#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   datetimeutils.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import calendar
import time
from collections.abc import Generator
from datetime import date, datetime, timedelta, tzinfo

import pytz

from pythontools.core.constants.datetime_constant import Month, Quarter, TimeUnit, Week
from pythontools.core.utils.randomutils import RandomUtil


class DatetimeUtil:
    UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "D": "days", "W": "weeks"}
    WTB = [
        "sun",
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "gmt",
        "ut",
        "utc",
        "est",
        "edt",
        "cst",
        "cdt",
        "mst",
        "mdt",
        "pst",
        "pdt",
    ]

    @classmethod
    def this_year(cls) -> int:
        """
        返回当前年份
        :return: 当前年份
        """
        return datetime.now().year

    @classmethod
    def this_quarter(cls) -> int:
        """

        :return:
        """
        dt = datetime.now()
        quarter = Quarter.get_quarter(dt)
        return quarter.value.val

    @classmethod
    def this_month(cls) -> int:
        """
        返回当前月份
        :return: 当前月份
        """
        return datetime.now().month

    @classmethod
    def this_day(cls) -> int:
        """
        返回当前天
        :return: 当前天
        """
        return datetime.now().day

    @classmethod
    def this_hour(cls) -> int:
        """
        返回当前小时
        :return: 当前小时
        """
        return datetime.now().hour

    @classmethod
    def this_minute(cls) -> int:
        """
        返回当前分钟数
        :return: 当前分钟
        """
        return datetime.now().minute

    @classmethod
    def this_second(cls) -> int:
        """
        返回当前分钟数
        :return: 当前分钟
        """
        return datetime.now().second

    @classmethod
    def this_millisecond(cls) -> int | float:
        """
        返回当前毫秒数

        Returns
        -------
        int | float
            当前毫秒数
        """
        current_seconds = time.time()
        return cls.convert_time(current_seconds, TimeUnit.SECONDS, TimeUnit.MILLISECONDS)

    @classmethod
    def this_ts(cls) -> float:
        """

        :return:
        """
        return datetime.now().timestamp()

    @classmethod
    def tomorrow(cls) -> date:
        """
        返回明天的日期

        Returns
        -------
        date
            明天的日期
        """
        return cls.get_next_day_by_dt(datetime.now())

    @classmethod
    def get_next_day_by_dt(cls, dt: datetime) -> datetime:
        """
        根据给定的 datetime 对象返回下一天日趋

        Parameters
        ----------
        dt : datetime
            给定的 datetime 日期

        Returns
        -------
        datetime
            下一天日期对象
        """
        return dt + timedelta(days=1)

    @classmethod
    def yesterday(cls) -> datetime:
        """
        返回昨天的日期

        Returns
        -------
        datetime
            代表昨天的日期
        """
        return cls.get_last_day_by_dt(datetime.now())

    @classmethod
    def get_last_day_by_dt(cls, dt: datetime) -> datetime:
        """
        返回给定日期对象的上一天

        Parameters
        ----------
        dt : datetime
            给定的日期独享

        Returns
        -------
        datetime
            给定日期对象的上一天
        """
        if not isinstance(dt, date):
            raise ValueError("dt must be a date object")
        return dt - timedelta(days=1)

    @classmethod
    def is_leap_year(cls, year: int) -> bool:
        """
        判断给定年份是否是闰年, 闰年是指年份不能被4整除或者 \n
        年份能被100整除但不能被400整除
        :param year: 待检测年份
        :return: 是否是闰年
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @classmethod
    def is_same_year(cls, date1: date, date2: date) -> bool:
        """
        检查给定的两个对象是否是同一年
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一年
        """
        if date1 is None or date2 is None:
            return False
        return date1.year == date2.year

    @classmethod
    def is_same_quarter(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一个季度
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否在同一个季度
        """
        q1 = Quarter.get_quarter(date1)
        q2 = Quarter.get_quarter(date2)

        return date1.year == date2.year and q1 == q2

    @classmethod
    def is_same_month(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一个月
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一个月
        """
        if date1 is None or date2 is None:
            return False
        return cls.is_same_year(date1, date2) and date1.month == date2.month

    @classmethod
    def is_same_week(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一周
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return:是否在同一周
        """
        _, week_num1, _ = date1.isocalendar()
        _, week_num2, _ = date2.isocalendar()
        return cls.is_same_year(date1, date2) and week_num1 == week_num2

    @classmethod
    def is_same_day(cls, date1, date2) -> bool:
        """
        检查给定的两个日期是否是同一个天
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一天
        """
        if date1 is None or date2 is None:
            return False

        return cls.is_same_month(date1, date2) and date1.day == date2.day

    @classmethod
    def is_weekend_by_dt(cls, dt: datetime) -> bool:
        """
        返回给定日期对象是否是周末

        Parameters
        ----------
        dt : datetime
            待检测日期对象

        Returns
        -------
        bool
            如果给定日期是周末, 则返回True,  否则返回False
        """
        week_obj = cls.get_day_of_week(dt)
        return week_obj == Week.SATURDAY or week_obj == Week.SUNDAY

    @classmethod
    def is_weekend(
        cls,
        year: int,
        month: int,
        day: int,
    ) -> bool:
        """
        判断给定的日期是否是周末

        Parameters
        ----------
        year : int
            给定年
        month : int
            给定月
        day : int
            给定日

        Returns
        -------
        bool
            如果是周末则返回True, 否则返回False
        """
        return cls.is_weekend_by_dt(datetime(year, month, day))

    @classmethod
    def is_weekday_by_dt(cls, dt: datetime) -> bool:
        """
        返回是给定的dt对象是否是周一到周五

        Parameters
        ----------
        dt : datetime
            待检测dt对象

        Returns
        -------
        bool
            如果是周一到周五这返回True, 否则返回False
        """
        return not cls.is_weekend_by_dt(dt)

    @classmethod
    def is_weekday(cls, year: int, month: int, day: int) -> bool:
        """
        判断给定的日期是否是周一到周五

        Parameters
        ----------
        year : int
            给定年
        month : int
            给定月
        day : int
            给定日

        Returns
        -------
        bool
            如果是周一到周五这返回True, 否则返回False
        """
        return cls.is_weekday_by_dt(datetime(year, month, day))

    @classmethod
    def has_tz(cls, dt: datetime) -> bool:
        """
        返回给定的日期对象是否含有时区信息

        Parameters
        ----------
        dt : datetime
            待判断日期对象

        Returns
        -------
        bool
            如果日期对象含有时区信息返回True, 否则返回False

        Notes:
        -------
        ref: https://github.com/RhetTbull/datetime-utils/blob/main/datetime_tzutils.py
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be a datetime object, but got {type(dt)}")
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None

    @classmethod
    def local_to_utc(cls, dt: datetime) -> datetime:
        """
        将 datetime 对象(带时区信息)转换成UTC时间

        Parameters
        ----------
        dt : datetime
            待转换的datetime对象

        Returns
        -------
        datetime
            转换后的datetime对象(UTC时间)

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 类型, 则抛出 TypeError 异常
        ValueError
            如果给定的对象没有时区信息, 则抛出 ValueError 异常

        Notes:
        -------
        ref: https://github.com/RhetTbull/datetime-utils/blob/main/datetime_tzutils.py
        """

        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        if cls.has_tz(dt):
            return dt.astimezone(tz=pytz.timezone("UTC"))
        else:
            raise ValueError("dt does not have timezone info")

    @classmethod
    def datetime_remove_tz(cls, dt: datetime) -> datetime:
        """
        删除时区信息

        Parameters
        ----------
        dt : datetime
            待删除的 datetime 对象

        Returns
        -------
        datetime
            删除时区信息后的 datetime 对象

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 对象, 则抛出异常
        """

        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        return dt.replace(tzinfo=None)

    @classmethod
    def utc_offset_seconds(cls, dt: datetime) -> int:
        """
        针对含有时区信息的 datetime 对象，以秒为单位返回与UTC的偏移量

        Parameters
        ----------
        dt : datetime
            待检测 datetime 对象

        Returns
        -------
        int
            以秒为单位返回与UTC的偏移量

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 对象, 则抛出异常
        ValueError
            如果 datetime 对象不包含时区信息, 则抛出异常
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        if cls.has_tz(dt):
            return dt.tzinfo.utcoffset(dt).total_seconds()  # type: ignore
        else:
            raise ValueError("dt does not have timezone info")

    @classmethod
    def get_random_tz(cls) -> tzinfo:
        """
        获取随机时区
        :return: 随机时区
        """
        timezones = pytz.all_timezones

        random_tz = RandomUtil.get_random_item_from_sequence(timezones)
        return pytz.timezone(random_tz)  # type: ignore

    @classmethod
    def get_local_tz(cls) -> tzinfo | None:
        """
        获取默认时区
        :return: timezone实例
        """
        # 获取当前时间的UTC时间
        utc_time = datetime.now(pytz.utc)

        # 获取当前时区的时间
        local_time = utc_time.astimezone()

        # 获取当前时区
        return local_time.tzinfo

    @classmethod
    def get_random_date(cls, start: date | None = None, end: date | None = None) -> date:
        """
        返回随机日期

        *Example*

        >>> cls.get_random_date(date(1998, 4, 24)) # 2014-12-05
        >>> cls.get_random_date(date(1998, 4, 24)) # 2012-05-24
        >>> cls.get_random_date(date(1998, 4, 24)) # 1998-08-25

        :param start: 开始日期
        :param end: 结束日期
        :return: 随机日期
        """
        if start is not None and end is not None and end <= start:
            raise ValueError(f"{start} must be less than {end}")
        if start is None:
            start = date(1900, 1, 1)
        if end is None:
            end = date.today()

        days_between = (end - start).days
        random_num_of_days = RandomUtil.get_random_val_from_range(0, days_between)
        random_date = start + timedelta(days=random_num_of_days)
        return random_date

    @classmethod
    def get_random_datetime(
        cls,
        start: datetime | None = None,
        end: datetime | None = None,
        *,
        random_tz: bool = False,
    ) -> datetime:
        """
        生成一个随机的 datetime 对象, 支持指定时间范围和随机时区。

        *Example*

        >>> cls.get_random_datetime(random_tz=True)
        datetime.datetime(1947, 12, 21, 9, 9, 39, tzinfo=<DstTzInfo 'Kwajalein' LMT+11:09:00 STD>)
        >>> cls.get_random_datetime() # datetime.datetime(1981, 7, 28, 13, 14, 35)
        >>> cls.get_random_datetime(random_tz=False) # datetime.datetime(1947, 12, 21, 9, 9, 39)

        :param start: 随机日期时间的开始范围
        :param end: 随机日期时间的结束范围。
        :param random_tz: 是否生成带有随机时区信息的 datetime 对象。如果为 True, 则生成带有随机时区的 datetime 对象。
        :return: 随机 datetime 对象
        """

        # NOTE 获取随机Date对象, 依赖于 get_random_date 方法
        start_date = start.date() if start is not None else start
        end_date = end.date() if end is not None else end
        random_date = cls.get_random_date(start_date, end_date)
        random_datetime = datetime.combine(random_date, datetime.min.time())

        # 获取时间部分随机值
        random_hour = RandomUtil.get_random_val_from_range(0, 24)
        random_minute = RandomUtil.get_random_val_from_range(0, 60)
        random_second = RandomUtil.get_random_val_from_range(0, 60)

        # 拼接 datetime 对象
        random_datetime = random_datetime.replace(hour=random_hour, minute=random_minute, second=random_second)
        if random_tz:
            tz_info = cls.get_random_tz()
            random_datetime = random_datetime.replace(tzinfo=tz_info)

        return random_datetime

    @classmethod
    def sleep(cls, seconds: float) -> None:
        """
        更加精确的Sleep方法
        :param seconds: 要睡眠的时间, 单位秒
        :return: None
        """
        start = time.time()
        seconds = seconds * (datetime.resolution * 1e6).seconds
        left = seconds
        while True:
            time.sleep(left)
            left = seconds - (time.time() - start)
            if left <= 0:
                break

    @classmethod
    def utc_now(cls) -> datetime:
        """
        获取当前 UTC 时间
        :return: 表示当前 UTC 时间的 datetime 对象
        """
        return datetime.now(pytz.UTC)

    @classmethod
    def utc_to_local(cls, date_obj: datetime, tz: str) -> datetime:
        """
        UTC 时间转指定时区时间
        :param date_obj: 待转换的 Datetime 对象, 表示一个 UTC 时间
        :param tz: 指定的时区
        :return: 转换后的 Datetime 对象
        """
        if not isinstance(date_obj, datetime):
            raise TypeError(f"date_obj must be datetime.datetime, not {type(date_obj)}")

        return date_obj.astimezone(pytz.timezone(tz))

    @classmethod
    def days_in_month(cls, year: int, month: int) -> int:
        """
        获取指定年份指定月多少天
        :param year: 指定年份
        :param month: 指定月
        :return: 该月一共多少天
        """
        assert 1 <= month <= 12, month
        _, days_in_month = calendar.monthrange(year, month)
        return days_in_month

    @classmethod
    def get_age(cls, birthday: datetime, *, use_float_format: bool = False) -> int | float:
        """
        根据给定生日返回年龄
        :param birthday: 给定生日
        :param use_float_format: 是否采用浮点数显示
        :return: 年龄
        """
        if birthday is None:
            raise ValueError("birthday cannot be None")

        now = datetime.now() + timedelta(days=1)
        if use_float_format:
            sub_days = (now - birthday).days
            age = round(sub_days / 365, 1)
            return age

        age = now.year - birthday.year

        # NOTE 根据月、日判断是否对年龄 -1
        # ISSUE-1, 如果生日是闰年2-29, 则构建datetime对象时报错。
        # 这里的问题是如果是闰年，会出现2月29日，那么使用 9999-02-29 构建 datetime 对象会报错
        # 改为单独对月和日进行判断，不再构建datetime对象
        # birth_dt_with_fix_year = datetime(9999, birthday.month, birthday.day)
        # now_dt_with_fix_year = datetime(9999, now.month, now.day)

        if birthday.month > now.month or (birthday.month == now.month and birthday.day > now.day):
            age -= 1

        return age

    @classmethod
    def nanos_to_seconds(cls, duration: int) -> float:
        """
        纳秒转秒
        :param duration: 时长
        :return: 秒
        """
        return cls.convert_time(duration, TimeUnit.NANOSECONDS, TimeUnit.SECONDS)

    @classmethod
    def nanos_to_millis(cls, duration: int) -> float:
        """
        纳秒转毫秒
        :param duration: 时长
        :return: 毫秒
        """
        return cls.convert_time(duration, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS)

    @classmethod
    def second_to_time(cls, seconds: int) -> str:
        """
        秒数转为时间格式(HH:mm:ss)
        :param seconds: 需要转换的秒数
        :return: 转换后的字符串
        """
        # PERF 取余符号效率低, 应该优化
        # PERF 1 使用整除代替除法
        hour = seconds // 3600
        other = seconds % 3600
        minute = other / 60
        seconds = other % 60

        res_dt = datetime.now() + timedelta(hours=hour, minutes=minute, seconds=seconds)
        return res_dt.strftime("%H:%M:%S")

    @classmethod
    def get_day_of_week(cls, dt: datetime) -> Week | None:
        """
        根据日期获取星期枚举实例

        Parameters
        ----------
        dt : datetime
            待检测日期对象

        Returns
        -------
        Week | None
            根据日期对象返回的星期枚举实例, 如果日期对象为 None或者日期不合法, 则返回 None
        """
        if dt is None:
            return None
        day_of_week = dt.weekday()

        return Week.get_week(day_of_week + 1)

    @classmethod
    def convert_time(cls, value: int | float, from_unit: TimeUnit, to_unit: TimeUnit) -> int | float:
        if value is None or from_unit is None or to_unit is None:
            raise ValueError("value cannot be None")

        return value * from_unit.value.unit_val_in_ns / to_unit.value.unit_val_in_ns

    @classmethod
    def datetime_to_ISO8601(cls, dt: datetime) -> str:
        """
        将datetime对象转换为ISO8601格式的字符串

        Parameters
        ----------
        dt : datetime
            待转换的datetime对象

        Returns
        -------
        str
            转换后的字符串
        """
        if dt is None:
            raise TypeError("dt cannot be None")

        return dt.isoformat()

    @classmethod
    def parse_period(cls, period: str) -> timedelta:
        """
        解析周期字符串, 如 "1D" 表示1天, "2W" 表示2周, "3M" 表示3个月, "4Y" 表示4年

        Examples
        --------
        >>> parse_period("1D")
        datetime.timedelta(days=1)
        >>> parse_period("2W")
        datetime.timedelta(days=14)
        >>> parse_period("15m")
        timedelta(minutes=15)
        >>> parse_period("1W")
        timedelta(weeks=1)

        Parameters
        ----------
        period : str
            代表时间间隔的字符串

        Returns
        -------
        timedelta
            timedelta对象,表示时间间隔

        Notes
        -----
        ref: https://gist.github.com/dsakovych/c1714d0c17ac0955c4b3149d42f34af5
        """
        value = int(period[:-1])
        unit = period[-1].lower()
        if unit not in cls.UNITS:
            raise ValueError(f"Invalid unit: {unit}")
        kwargs = {cls.UNITS[unit]: value}
        return timedelta(**kwargs)

    @classmethod
    def generate_dt_range(
        cls,
        start: str,
        end: str,
        period: str,
    ) -> Generator[datetime, None, None]:
        """
        产生时间 datetime 序列

        Parameters
        ----------
        start : str
            起始时间，格式为 ISO 8601
        end : str
            结束时间，格式为 ISO 8601
        period : str
            时间周期

        Yields
        ------
        Generator[datetime, None, None]
            datetime 对象生成器
        """
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        period_delta = cls.parse_period(period)

        current_dt = start_dt

        while current_dt < end_dt:
            yield current_dt
            current_dt = min(current_dt + period_delta, end_dt)
            if current_dt >= end_dt:
                break

    @classmethod
    def nth_day_of_month(cls, *, year: int, month: int, weekday: int, n: int) -> date:
        """
        返回给定日期的第n个星期几的日期

        Parameters
        ----------
        year : int
            给定的年
        month : int
            给定的月
        weekday : int
            给定的周记
        n : int
            给定的第n个星期几

        Returns
        -------
        date | None
            给定日期的第n个星期几的日期

        Raises
        ------
        IndexError
            如果月份或星期数不合法, 则抛出异常

        Notes
        -----
        ref: https://github.com/fitnr/convertdate
        """

        if not 0 <= n <= 5:
            raise IndexError(f"Nth day of month must be 0-5. Received: {n}")

        month_obj: Month | None = Month.get_month(month)
        weekday_obj = Week.get_week(weekday)

        if month_obj is None:
            raise IndexError("month is out of range, must be 1-12")

        if weekday_obj is None:
            raise IndexError("weekday is out of range, must be 1-7")

        return cls._nth_day_of_month_obj(year, month_obj, weekday_obj, n)

    @classmethod
    def _nth_day_of_month_obj(cls, year: int, month_obj: Month, weekday_obj: Week, n: int) -> date:
        month = month_obj.value.calendar_value
        weekday = weekday_obj.value.iso8601_value

        first_day, days_in_month = calendar.monthrange(year, month)
        # 获取当月第一个给定 weekday 是几号
        # 例如2024-08 第一个周一是2024-08-05， 第一个周四是1号
        first_weekday_of_kind = 1 + (weekday - first_day) % 7

        if n == 0:
            if first_weekday_of_kind in [1, 2, 3] and first_weekday_of_kind + 28 <= days_in_month:
                n = 5
            else:
                n = 4

        day = first_weekday_of_kind + ((n - 1) * 7)
        if day > days_in_month:
            raise IndexError(f"No {n}th day of month {month}")

        return date(year, month, day)
