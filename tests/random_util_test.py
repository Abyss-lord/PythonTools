#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   random_util_test.py
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

import allure  # type: ignore
import pytest
from faker import Faker

from .context_test import (
    RandomUtil,
    SequenceUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("随机工具类")
@allure.description("随机工具类，支持获取随机值")
@allure.tag("random", "util")
class TestRandomUtil:
    TEST_ROUND = 100

    @allure.story("获取随机值")
    @allure.description("测试获取随机值,不需要提供容器对象")
    class TestGetRandomValue:
        @allure.title("测试获取随机布尔值")
        def test_get_random_boolean(cls):
            with allure.step("步骤1:测试获取单个随机布尔值"):
                assert RandomUtil.get_random_boolean() in [True, False]

            with allure.step("步骤2:测试获取多个随机布尔值"):
                random_booleans = RandomUtil.get_random_booleans(10)
                assert all(isinstance(i, bool) for i in random_booleans)

        @allure.title("测试获取随机复数")
        def test_get_random_complex(cls):
            with allure.step("步骤1:测试获取随机复数, 不输入任何参数"):
                random_complex = RandomUtil.get_random_complex()
                assert isinstance(random_complex, complex)

            with allure.step("步骤2:测试获取多个随机复数，输入参数"):
                random_generator = RandomUtil.get_random_complexes_with_range_and_precision((0, 1), (-1, 1), length=1)
                val = next(random_generator)
                assert 0 <= val.real <= 1
                assert -1 <= val.imag <= 1

        @allure.title("测试获取随机浮点数")
        def test_get_random_float(cls):
            with allure.step("步骤1:测试获取随机浮点数, 不输入任何参数"):
                random_float = RandomUtil.get_random_float()
                assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

            with allure.step("步骤2:测试获取多个随机浮点数"):
                random_generator = RandomUtil.get_random_floats_with_range_and_precision(
                    0.0, 1.0, precision=2, length=5
                )

                assert all(0.0 <= random_float <= 1.0 and isinstance(random_float, float) for _ in random_generator)

    @allure.story("从容器中随机获取数据")
    @allure.description("测试从容器中随机获取数据，支持列表、元组、集合")
    class TestGetRandomItemFromContainer:
        @allure.title("测试从列表中随机获取数据")
        def test_get_random_item_from_list(cls):
            with allure.step("步骤1:测试从空列表中获取数据"):
                sequence = []
                assert RandomUtil.get_random_item_from_sequence(sequence) is None

            with allure.step("步骤2:测试从非空列表中获取单个数据"):
                sequence = [1, 2, 3, 4, 5]
                random_item = RandomUtil.get_random_item_from_sequence(sequence)
                assert random_item in sequence

            with allure.step("步骤3:测试从非空列表中获取多个数据"):
                empty_sequence = []
                assert RandomUtil.get_random_items_from_sequence(empty_sequence, 1) == []
                sequence = [1, 2, 3, 4, 5]
                random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 3)
                assert SequenceUtil.get_length(random_sequence) == 3
                random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 15)
                assert random_sequence == sequence

            with allure.step("步骤4:测试从非空列表中获取多个数据，数量参数错误"):
                sequence = [1, 2, 3, 4, 5]
                with pytest.raises(ValueError):
                    RandomUtil.get_random_items_from_sequence(sequence, -1)

    @allure.title("测试从指定范围中随机获取数据")
    def test_get_random_val_from_range(cls):
        with allure.step("步骤1:测试从指定范围中随机获取整数"):
            random_int = RandomUtil.get_random_val_from_range(1, 10)
            assert isinstance(random_int, int) and 1 <= random_int <= 10
        with allure.step("步骤2:测试从指定范围中随机获取整数, 参数错误"):
            with pytest.raises(ValueError):
                RandomUtil.get_random_val_from_range(10, 1)
