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
import datetime
import json

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
        # PERF 增加更多支持的日期格式
        matched = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        if matched:
            year = BasicConvertor.to_int(matched.group(1))
            month = BasicConvertor.to_int(matched.group(3))
            day = BasicConvertor.to_int(matched.group(5))
            return cls.is_valid_date(year, month, day)
        return False

    @classmethod
    def is_valid_date(cls, year: int, month: int, day: int) -> bool:
        """
        验证是否为生日
        :param year: 年
        :param month: 月
        :param day: 日
        :return: 是否为生日
        """
        # 判断年
        # NOTE datetime.MINYEAR的值是1，这里的逻辑是否要修改
        if year < datetime.MINYEAR or year > DateUtil.this_year():
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

    @classmethod
    def is_json(cls, s: str) -> bool:
        """
        判断字符串是否是json字符串

        *Example*

        >>> cls.is_json('{"name": "Peter"}') # returns true
        >>> cls.is_json('[1, 2, 3]') # returns true
        >>> cls.is_json('{nope}') # returns false

        :param s: 待检查字符串
        :return: 是否是JSON字符串
        """
        if StringUtil.is_blank(s):
            return False

        if PatternPool.JSON_WRAPPER_PATTERN.match(s) is None:
            return False

        # PERF 不应该用try-except作为分支逻辑
        try:
            return isinstance(json.loads(s), (dict, list))
        except (TypeError, ValueError, OverflowError):
            pass

        return False
