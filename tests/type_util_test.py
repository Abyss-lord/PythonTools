#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   type_util_test.py
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

import inspect

import allure  # type: ignore
from faker import Faker
from loguru import logger

from .context_test import (
    StringUtil,
    TypeUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("类型工具类")
@allure.description("类型工具类，用于获取一个对象的父类, 获取、显示函数信息等")
@allure.tag("util")
class TestTypeUtil:
    @classmethod
    def test_get_class_names(cls) -> None:
        test_1_obj = MoreDerived()
        res = TypeUtil.get_class_mro(test_1_obj)
        logger.debug(res)

        test_2_obj = Derived
        res = TypeUtil.get_class_mro(test_2_obj)
        logger.debug(res)

    @classmethod
    def test_get_class_tree(cls) -> None:
        res = inspect.getclasstree(MoreDerived())
        logger.debug(res)

    @classmethod
    def test_get_function_info(cls) -> None:
        def test_func(a: int, b: str, c: int = 1, *args, **kwargs):
            pass

        res = TypeUtil.get_function_info(test_func)
        logger.debug(res)

    @classmethod
    def test_show_function_info(cls) -> None:
        TypeUtil.show_function_info(StringUtil.get_common_suffix, show_detail=True)

    @classmethod
    def test_get_class_name(cls) -> None:
        res = TypeUtil.get_class_name(StringUtil)
        logger.debug(res)


class Base:
    pass


class Derived(Base):
    pass


class MoreDerived(Derived, list):
    pass
