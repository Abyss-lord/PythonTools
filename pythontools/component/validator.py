#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     validator
   Description :
   date：          2024/7/17
-------------------------------------------------
   Change Activity:
                   2024/7/17:
-------------------------------------------------
"""
from .convertor import BasicConvertor
from .pattern_pool import PatternPool
from .basic_utils import DateUtil, StringUtil
from loguru import logger


class Validator(object):
    @classmethod
    def is_valid_birthday(cls, birthday: str) -> bool:
        """
        验证是否为生日，目前支持yyyy-MM-dd、yyyyMMdd、yyyy/MM/dd、yyyy.MM.dd、yyyy年MM月dd日
        :param birthday: 待测试值
        :return: 是否为生日
        """
        matched = PatternPool.BIRTHDAY.match(birthday)
        if matched:
            year = BasicConvertor.to_int(matched.group(1))
            month = BasicConvertor.to_int(matched.group(3))
            day = BasicConvertor.to_int(matched.group(5))
            logger.debug(f"{year}, {month}, {day}")
            return cls.is_valid_birthday_date(year, month, day)
        return False

    @classmethod
    def is_valid_birthday_date(cls, year: int, month: int, day: int) -> bool:
        """
        验证是否为生日
        :param year: 年
        :param month: 月
        :param day: 日
        :return: 是否为生日
        """
        # 判断年
        if year < 1900 or year > DateUtil.this_year():
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
            return day < 29 or (day < 30 and DateUtil.is_leap_year(year))

        return True
