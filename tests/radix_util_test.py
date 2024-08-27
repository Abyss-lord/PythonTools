#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   radix_util_test.py
@Date       :   2024/08/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import allure  # type:ignore
from faker import Faker

from .context_test import (
    RadixUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("进制转换工具类")
@allure.description("进制转换工具类,提供进制转换等功能")
class TestRadixUtil:
    @allure.story("进制转换")
    @allure.description("支持任意进制之间的转换")
    class TestConvert:
        @allure.title("测试进制转换")
        def test_convert(cls):
            with allure.step("步骤1:测试2进制转换为任意进制"):
                assert RadixUtil.convert_base("1011", 2, 10) == "11"
                assert RadixUtil.convert_base("1010", 2, 16) == "A"
                assert RadixUtil.convert_base("10101010", 2, 8) == "252"
                assert RadixUtil.convert_base("10101010", 2, 16) == "AA"

            with allure.step("步骤2:测试8进制转换为任意进制"):
                assert RadixUtil.convert_base("252", 8, 2) == "10101010"
                assert RadixUtil.convert_base("26216", 8, 10) == "11406"
                assert RadixUtil.convert_base("154473", 8, 10) == "55611"
                assert RadixUtil.convert_base("154473", 8, 16) == "D93B"

            with allure.step("步骤3:测试10进制转换为任意进制"):
                assert RadixUtil.convert_base("11", 10, 2) == "1011"
                assert RadixUtil.convert_base("255", 10, 16) == "FF"
                assert RadixUtil.convert_base("82782", 10, 8) == "241536"
                assert RadixUtil.convert_base("277587", 10, 8) == "1036123"

            with allure.step("步骤4:测试16进制转换为任意进制"):
                assert RadixUtil.convert_base("A", 16, 2) == "1010"
                assert RadixUtil.convert_base("FF", 16, 10) == "255"
                assert RadixUtil.convert_base("AA", 16, 2) == "10101010"

    @allure.story("获取十进制数i的二进制表示中最后一个1相对于末尾的位置")
    @allure.description("获取十进制数i的二进制表示中最后一个1相对于末尾的位置")
    class TestGetLstOneIdx:
        @allure.title("测试获取十进制数i的二进制表示中最后一个1相对于末尾的位置")
        def test_get_lst_one_idx(cls) -> None:
            assert RadixUtil.get_lst_one_idx(3) == 1
            assert RadixUtil.get_lst_one_idx(5) == 2
            assert RadixUtil.get_lst_one_idx(8) == 3
