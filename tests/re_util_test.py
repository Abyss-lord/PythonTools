#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   re_util_test.py
@Date       :   2024/08/28
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/28
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import re

import allure
from loguru import logger

from .context_test import (
    PatternPool,
    ReUtil,
)


@allure.feature("正则工具类")
@allure.description("正则工具类，提供正则匹配、替换等功能")
@allure.tag("util")
class TestReUtil:
    @allure.title("测试匹配方法")
    def test_is_match_regex(cls) -> None:
        assert ReUtil.is_match(re.compile(r"\d+"), "123456")
        words = "...words, words..."
        pattern = re.compile(r"(\W+)")
        assert ReUtil.is_match(pattern, words)
        res = ReUtil.get_group_1(pattern, words)
        logger.debug(f"{res=}")

    @allure.title("测试获取第一匹配组")
    def test_get_group_0(cls):
        birthday = "20221201"
        _ = PatternPool.BIRTHDAY_PATTERN.findall(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.search(birthday)
        res3 = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = res3.groups()

    @allure.title("测试match方法")
    def test_match_method(cls):
        m = PatternPool.ISO8601.match("2022-12-01T12:34:56Z")
        groups: dict[str, str] = {k: v for k, v in m.groupdict().items() if v is not None}
        logger.debug(f"{groups=}")
