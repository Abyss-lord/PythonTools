#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   pattern_pool.py
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

import re


class RegexPool(object):
    # 生日
    BIRTHDAY = "^(\\d{2,4})([/\\-.年]?)(\\d{1,2})([/\\-.月]?)(\\d{1,2})日?$"
    # 十五位身份证号表达式
    ID_NUMBER_15_REGEX = (
        r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"
    )
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_REGEX = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
    # JSON 字符串
    JSON_REGEX = r"^\s*[\[{]\s*(.*)\s*[\}\]]\s*$"
    # 单个中文汉字
    CHINESE = "[\u2e80-\u2eff\u2f00-\u2fdf\u31c0-\u31ef\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\ud840\udc00-\ud869\udedf\ud869\udf00-\ud86d\udf3f\ud86d\udf40-\ud86e\udc1f\ud86e\udc20-\ud873\udeaf\ud87e\udc00-\ud87e\ude1f]"
    CHINESES = CHINESE + "+"


class PatternPool:
    # 十五位身份证号表达式
    ID_NUMBER_15_PATTERN = re.compile(RegexPool.ID_NUMBER_15_REGEX)
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_PATTERN = re.compile(RegexPool.ID_NUMBER_18_REGEX)
    # 生日
    BIRTHDAY_PATTERN = re.compile(RegexPool.BIRTHDAY)
    # JSON 字符串
    JSON_WRAPPER_PATTERN = re.compile(RegexPool.JSON_REGEX, re.MULTILINE | re.DOTALL)
