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
@allure.story("布尔值转换")
@allure.description("测试布尔值True和False的转换")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "boolean")
class TestTriggerBoolean:
    @allure.title("测试布尔值转换")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, False),
            (False, True),
            (1, False),
            (0, True),
        ],
    )
    def test_negate_with_correct_arguments(self, input_value, expected_output) -> None:
        assert BooleanUtil.negate(input_value) == expected_output

    @allure.title("测试布尔值转换,输入错误参数")
    @pytest.mark.parametrize(
        "input_value",
        [
            1,
        ],
    )
    def test_negate_with_wrong_arguments(self, input_value):
        with pytest.raises(TypeError):
            BooleanUtil.negate(input_value, raise_exception=True)  # type: ignore


@allure.feature("布尔工具类")
@allure.story("布尔值逻辑运算")
@allure.description("测试布尔值逻辑运算")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "boolean")
class TestBooleanLogic:
    @allure.title("测试与运算")
    @pytest.mark.parametrize(
        "values, expected_output",
        [
            ([True, True], True),
            ([True, False], False),
            ([False, True], False),
            ([False, False], False),
            pytest.param([], False, marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_and(
        cls,
        values,
        expected_output,
    ) -> None:
        assert BooleanUtil.and_all(*values) == expected_output

    @allure.title("测试异或运算")
    @pytest.mark.parametrize(
        "values, expected_output",
        [
            ([True, True], False),
            ([True, False], True),
            ([False, True], True),
            ([False, False], False),
            pytest.param([], False, marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_xor(
        self,
        values,
        expected_output: bool,
    ) -> None:
        assert BooleanUtil.xor_all(*values) == expected_output

    @allure.title("测试或运算")
    @pytest.mark.parametrize(
        "values, expected_output",
        [
            ([True, True], True),
            ([True, False], True),
            ([False, True], True),
            ([False, False], False),
            pytest.param([], False, marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_or(
        self,
        values,
        expected_output,
    ):
        assert BooleanUtil.or_all(*values) == expected_output

    @allure.title("测试判断状态")
    @pytest.mark.parametrize(
        "state, expected",
        [
            (True, True),
            (False, False),
            (1, True),
            (0, False),
        ],
    )
    def test_is_true(
        self,
        state,
        expected,
    ):
        assert BooleanUtil.is_true(state) == expected
        assert BooleanUtil.is_false(state) != expected


@allure.feature("布尔工具类")
@allure.story("布尔值和其他类型的转换")
@allure.description("测试布尔值和其他类型的转换")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "boolean")
class TestBooleanConversion:
    @allure.title("测试布尔值转换为整数")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, 1),
            (False, 0),
            pytest.param(1, 1, marks=pytest.mark.xfail),
        ],
    )
    def test_boolean_to_int_with_correct_arguments(cls, input_value, expected_output) -> None:
        assert BooleanUtil.boolean_to_number(input_value) == expected_output

    @allure.title("测试证书转换成布尔值")
    @pytest.mark.parametrize(
        "val, excepted",
        [
            (1, True),
            (0, False),
            (1.2, True),
            (3.4, True),
            pytest.param("a", False, marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_int_to_boolean(
        self,
        val,
        excepted,
    ):
        assert BooleanUtil.number_to_boolean(val) == excepted

    @allure.title("测试获取布尔值")
    @pytest.mark.parametrize(
        "val, default, expected",
        [
            (1, False, 1),
            (1.2, False, 1.2),
            ("a", False, "a"),
            (True, False, True),
            (False, True, False),
            (None, True, True),
            (None, False, False),
        ],
    )
    def test_get_boolean(
        self,
        val,
        default,
        expected,
    ):
        assert BooleanUtil.to_bool_default_if_none(val, default) == expected

    @allure.title("测试布尔值转换为 TRUE、FALSE 字符串")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, "TRUE"),
            (False, "FALSE"),
        ],
    )
    def test_to_str_true_and_false(
        cls,
        input_value,
        expected_output,
    ) -> None:
        assert BooleanUtil.boolean_to_str(input_value) == expected_output

    @allure.title("测试布尔值转换为Yes和No字符串")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, "YES"),
            (False, "NO"),
        ],
    )
    def test_to_str_yes_no(
        self,
        input_value,
        expected_output,
    ):
        assert BooleanUtil.to_str_yes_and_no(input_value) == expected_output

    @allure.title("测试布尔值转换为是和否字符串")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, "是"),
            (False, "否"),
        ],
    )
    def test_to_chinese_str(
        self,
        input_value,
        expected_output,
    ):
        assert BooleanUtil.to_chinese_str(input_value) == expected_output

    @allure.title("测试布尔值转换为 ON 和 OFF 字符串")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            (True, "ON"),
            (False, "OFF"),
        ],
    )
    def test_to_str_on_and_off(
        self,
        input_value,
        expected_output,
    ) -> None:
        assert BooleanUtil.to_str_on_and_off(input_value) == expected_output

    @allure.title("测试布尔值转换为自定义字符串")
    @pytest.mark.parametrize(
        "input_value, true_str, false_str, expected_output",
        [
            (True, "|", "?", "|"),
            (False, "|", "?", "?"),
            (True, "", "", "TRUE"),
            (False, "", "", "FALSE"),
        ],
    )
    def test_to_string(
        self,
        input_value,
        true_str,
        false_str,
        expected_output,
    ) -> None:
        assert BooleanUtil.to_string(input_value, true_str, false_str) == expected_output

    @allure.title("测试字符串转换为布尔值")
    @pytest.mark.parametrize(
        "input_value, expected_output",
        [
            ("True", True),
            ("False", False),
            ("1", True),
            ("0", False),
            ("是", True),
            ("否", False),
            ("ON", True),
            ("OFF", False),
            ("对", True),
            ("错", False),
            ("ok", True),
            ("no", False),
            ("", False),
            pytest.param([1, 2], False, marks=pytest.mark.xfail(raises=TypeError)),
        ],
    )
    def test_str_to_boolean(
        self,
        input_value,
        expected_output,
    ) -> None:
        assert BooleanUtil.str_to_boolean(input_value) == expected_output
