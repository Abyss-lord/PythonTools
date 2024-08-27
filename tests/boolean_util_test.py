#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   boolean_util_test.py
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

import allure  # type: ignore
import pytest
from faker import Faker

from .context_test import (
    BooleanUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("布尔工具类")
@allure.description("布尔工具类，用于处理布尔值相关的操作")
@allure.tag("util")
class TestBooleanUtil:
    @allure.story("布尔值转换")
    @allure.description("测试布尔值True和False的转换")
    class TestTriggerBoolean:
        @allure.title("测试布尔值转换")
        def test_negate_with_correct_arguments(cls) -> None:
            with allure.step("步骤1:测试布尔值取反"):
                assert not BooleanUtil.negate(True)
                assert BooleanUtil.negate(False)
                assert not BooleanUtil.negate(1)  # type: ignore
                assert BooleanUtil.negate(0)  # type: ignore

            with allure.step("步骤2:测试布尔值转换，输入错误参数"):
                assert not BooleanUtil.negate(1, raise_exception=False)  # type: ignore
                with pytest.raises(TypeError):
                    BooleanUtil.negate(1, raise_exception=True)  # type: ignore

    @allure.story("布尔值逻辑运算")
    class TestBooleanLogic:
        @allure.title("测试与运算")
        def test_and(cls) -> None:
            assert BooleanUtil.and_all(True, True)
            assert not BooleanUtil.and_all(True, False)
            assert not BooleanUtil.and_all(False, True)
            assert not BooleanUtil.and_all(False, False)

        @allure.title("测试异或运算")
        def test_xor(self):
            assert BooleanUtil.xor(True, False)
            assert not BooleanUtil.xor(True, False, True)
            assert BooleanUtil.xor(True, False, False)
            assert not BooleanUtil.xor(True, True)

        @allure.title("测试或运算")
        def test_or(self):
            assert BooleanUtil.or_all(True, True)
            assert BooleanUtil.or_all(True, False)
            assert BooleanUtil.or_all(False, True)
            assert not BooleanUtil.or_all(False, False)
            assert not BooleanUtil.or_all(0, 0, 0)

    @allure.story("布尔值转换")
    class TestBooleanConversion:
        @allure.title("测试布尔值转换为整数")
        def test_boolean_to_int_with_correct_arguments(cls) -> None:
            with allure.step("步骤1:测试布尔值转换为整数,输入正确参数"):
                assert BooleanUtil.boolean_to_int(True) == 1
                assert BooleanUtil.boolean_to_int(False) == 0

            with allure.step("步骤2:测试布尔值转换为整数,输入错误参数"):
                with pytest.raises(ValueError):
                    BooleanUtil.boolean_to_int(1, strict_mode=True) == 1

        @allure.title("测试布尔值转换为字符串")
        def test_boolean_to_str(self):
            with allure.step("步骤1:测试布尔值转换为True和False"):
                assert BooleanUtil.to_str_true_and_false(True) == "TRUE"
                assert BooleanUtil.to_str_true_and_false(False) == "FALSE"

            with allure.step("步骤2:测试布尔值转换为Yes和No"):
                assert BooleanUtil.to_str_yes_no(True) == "YES"
                assert BooleanUtil.to_str_yes_no(False) == "NO"

            with allure.step("步骤3:测试布尔值转换为是和否"):
                assert BooleanUtil.to_chinese_str(True) == "是"
                assert BooleanUtil.to_chinese_str(False) == "否"

            with allure.step("步骤4:测试布尔值转换为ON和OFF"):
                assert BooleanUtil.to_str_on_and_off(True) == "ON"
                assert BooleanUtil.to_str_on_and_off(False) == "OFF"

            with allure.step("步骤5:测试布尔值转换为自定义字符串"):
                assert BooleanUtil.to_string(True, "|", "?") == "|"
                assert BooleanUtil.to_string(False, "|", "?") == "?"

        @allure.title("测试字符串转换为布尔值")
        def test_str_to_boolean(self):
            with allure.step("步骤1:测试英文字符串转换为布尔值"):
                assert BooleanUtil.str_to_boolean("True")
                assert BooleanUtil.str_to_boolean("ok")
                assert not BooleanUtil.str_to_boolean("false")
                assert not BooleanUtil.str_to_boolean("no")
                assert not BooleanUtil.str_to_boolean("×")

            with allure.step("步骤2:测试中文字符串转换为布尔值"):
                assert BooleanUtil.str_to_boolean("对")
                assert not BooleanUtil.str_to_boolean("错")
                assert BooleanUtil.str_to_boolean("是")
                assert not BooleanUtil.str_to_boolean("否")

            with allure.step("步骤3:测试数字字符串转换为布尔值"):
                assert not BooleanUtil.str_to_boolean("0")
                assert BooleanUtil.str_to_boolean("1")

            with allure.step("步骤4:测试空字符串转换为布尔值"):
                assert not BooleanUtil.str_to_boolean("")
