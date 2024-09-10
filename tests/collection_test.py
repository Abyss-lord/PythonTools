#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   collection_test.py
@Date       :   2024/09/10
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/10
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

import allure
from faker import Faker
from loguru import logger

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


# here put the import lib
from .context_test import CollectionUtil


@allure.feature("CollectionUtil 工具类测试")
class TestCollectionUtil:
    @allure.title("测试flatten方法")
    def test_flatten(self):
        res = CollectionUtil.flatten(
            [
                [[1, 2, 3], (42, None)],
                [4, 5],
                [6],
                7,
            ]
        )

        logger.debug(list(res))
