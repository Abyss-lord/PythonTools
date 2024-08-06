#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   zodiac.py
@Date       :   2024/08/06
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/06
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from datetime import date

from ..decorator import UnCkeckFucntion

WARNING_ENABLED = True


class Zodiac(object):
    DAY_ARR = [20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 23, 22]
    ZODIACS = [
        "摩羯座",
        "水瓶座",
        "双鱼座",
        "白羊座",
        "金牛座",
        "双子座",
        "巨蟹座",
        "狮子座",
        "处女座",
        "天秤座",
        "天蝎座",
        "射手座",
        "摩羯座",
    ]
    CHINESE_ZODIACS = [
        "鼠",
        "牛",
        "虎",
        "兔",
        "龙",
        "蛇",
        "马",
        "羊",
        "猴",
        "鸡",
        "狗",
        "猪",
    ]

    @classmethod
    @UnCkeckFucntion(WARNING_ENABLED)
    def get_zodiac(cls, month: int, day: int) -> str:
        """
        根据指定月、日获取星座

        Parameters
        ----------
        month : int
            指定月份
        day : int
            指定日

        Returns
        -------
        str
            给定日期所属的星座
        """

        return (
            cls.ZODIACS[month] if day < cls.DAY_ARR[month] else cls.ZODIACS[month + 1]
        )

    @classmethod
    def get_zodiac_by_date(cls, dt: date) -> str:
        """
        根据给定的dt实例获取星座

        Parameters
        ----------
        dt : date
            datetime.date实例

        Returns
        -------
        str
            星座
        """
        _, month, day = dt.year, dt.month, dt.day
        return cls.get_zodiac(month, day)

    @classmethod
    def get_chinese_zodiac(cls, year: int) -> str:
        """
        根据给定的年份获取生肖信息

        Parameters
        ----------
        year : int
            待检测年份

        Returns
        -------
        str
            生肖信息

        Raises
        ------
        ValueError
            给定年份小于1900, 抛出异常
        """
        if year < 1900:
            raise ValueError(f"Invalid year {year}")

        return cls.CHINESE_ZODIACS[(year - 1900) % len(cls.CHINESE_ZODIACS)]

    @classmethod
    def get_chinese_zodiac_by_date(cls, dt: date) -> str:
        """
        根据给定的dt实例获取生肖信息

        Parameters
        ----------
        dt : date
            待检测datetime.date实例

        Returns
        -------
        str
            生肖信息
        """
        year = dt.year
        return cls.get_chinese_zodiac(year)
