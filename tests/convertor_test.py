#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   convertor_test.py
@Date       :   2024/08/27
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/27
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import allure  # type: ignore
import pytest
from faker import Faker

from .context_test import (
    BasicConvertor,
    ConversionError,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("基础转换器")
@allure.description("基础转换器，支持安全、便捷地类型转换")
@allure.tag("basic", "util")
class TestConvertor:
    @allure.story("基础类型转换")
    @allure.description("基础类型转换, 基础类型包括 str, int, float, bool")
    class TestBasicConvertor:
        @allure.title("测试其他类型转换 str 类型转换")
        def test_convert_to_str(self) -> None:
            assert BasicConvertor.to_str(123) == "123"
            assert BasicConvertor.to_str(123.456) == "123.456"
            assert BasicConvertor.to_str(True) == "True"
            assert BasicConvertor.to_str(False) == "False"
            assert BasicConvertor.to_str(None) == ""
            assert BasicConvertor.to_str("abc") == "abc"
            assert BasicConvertor.to_str([1, 2, 3]) == "123"
            assert BasicConvertor.to_str((1, 2, 3)) == "123"
            assert BasicConvertor.to_str({"a": 1, "b": 2}) == "ab"

        @allure.title("测试其他类型转换 int 类型转换")
        def test_convert_to_int(self) -> None:
            assert BasicConvertor.to_int("123") == 123
            assert BasicConvertor.to_int("123.456") == 123
            assert BasicConvertor.to_int(True) == 1
            assert BasicConvertor.to_int(False) == 0
            assert BasicConvertor.to_int(None) == 0
            assert BasicConvertor.to_int("abc") == 0
            assert BasicConvertor.to_int([1, 2, 3]) == 0
            assert BasicConvertor.to_int((1, 2, 3)) == 0
            assert BasicConvertor.to_int({"a": 1, "b": 2}) == 0

            assert BasicConvertor.to_int("123", 100) == 123
            assert BasicConvertor.to_int("abc", 100) == 100
            with pytest.raises(ConversionError):
                BasicConvertor.to_int("sda", raise_exception=True)

        @allure.title("测试其他类型转换 float 类型转换")
        def test_convert_to_float(self) -> None:
            assert BasicConvertor.to_float("123") == 123.0
            assert BasicConvertor.to_float("123.456") == 123.456
            assert BasicConvertor.to_float(True) == 1.0
            assert BasicConvertor.to_float(False) == 0.0
            assert BasicConvertor.to_float(None) == 0.0
            assert BasicConvertor.to_float("abc") == 0.0
            assert BasicConvertor.to_float([1, 2, 3]) == 0.0
            assert BasicConvertor.to_float((1, 2, 3)) == 0.0
            assert BasicConvertor.to_float({"a": 1, "b": 2}) == 0.0

            assert BasicConvertor.to_float("123", 100.0) == 123.0
            assert BasicConvertor.to_float("abc", 100.0) == 100.0
            with pytest.raises(ConversionError):
                BasicConvertor.to_float("sda", raise_exception=True)

        @allure.title("测试其他类型转换 bool 类型转换")
        def test_convert_to_bool(cls) -> None:
            assert BasicConvertor.to_bool("123")
            assert BasicConvertor.to_bool("123.456")
            assert BasicConvertor.to_bool(True)
            assert not BasicConvertor.to_bool(False)
            assert BasicConvertor.to_bool("真")
            assert BasicConvertor.to_bool("√")
