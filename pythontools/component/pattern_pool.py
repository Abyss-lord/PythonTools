#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     PatternPool
   Description :
   date：          2024/7/17
-------------------------------------------------
   Change Activity:
                   2024/7/17:
-------------------------------------------------
"""
import re


class RegexPool(object):
    # 生日
    BIRTHDAY = "^(\\d{2,4})([/\\-.年]?)(\\d{1,2})([/\\-.月]?)(\\d{1,2})日?$"
    # 十五位身份证号表达式
    ID_NUMBER_15_REGEX = r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_REGEX = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"


class PatternPool():
    # 十五位身份证号表达式
    ID_NUMBER_15_REGEX = re.compile(RegexPool.ID_NUMBER_15_REGEX)
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_REGEX = re.compile(RegexPool.ID_NUMBER_18_REGEX)
    # 生日
    BIRTHDAY = re.compile(RegexPool.BIRTHDAY)
