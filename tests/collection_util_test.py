#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_utils.py
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

import allure
from faker import Faker
from loguru import logger

from .context_test import (
    CollectionUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("集合工具类")
@allure.description("集合工具类，提供集合相关的工具方法")
@allure.tag("collection", "util")
class TestCollectionUtil:
    @allure.title("测试组合")
    def test_powerset(cls):
        s = [1, 2, 3]
        for subset in CollectionUtil.get_powerset(s):
            for j in subset:
                logger.debug(j)

    @allure.title("测试嵌套字典迭代")
    def test_nested_dict_iter(cls):
        d = {"a": {"a": {"y": 2}}, "b": {"c": {"a": 5}}, "x": {"a": 6}}
        logger.debug(list(CollectionUtil.nested_dict_iter(d)))
