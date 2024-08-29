#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   sequence_test.py
@Date       :   2024/08/29
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/29
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import allure
import pytest
from faker import Faker

from .context_test import (
    SequenceUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("序列工具类")
@allure.description("序列工具类, 用于处理序列相关的操作")
@allure.tag("Sequence", "util")
class TestSequenceUtil:
    @allure.title("测试按子集数量切分序列")
    def test_split_sequence(cls) -> None:
        test_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_sequence(test_seq, 3) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 1) == [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 10) == [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
        SequenceUtil.split_sequence(test_seq, 4) == [[1, 2], [3, 4], [5, 6], [7, 8, 9]]
        with pytest.raises(ValueError):
            assert SequenceUtil.split_sequence(test_seq, 0) == []

    @allure.title("测试切分序列为两半")
    def test_split_half(cls) -> None:
        test_seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_half(test_seq_1) == [[1, 2, 3, 4], [5, 6, 7, 8, 9]]
        test_seq_2 = [1, 2, 3, 4, 5, 6, 7, 8]
        assert SequenceUtil.split_half(test_seq_2) == [[1, 2, 3, 4], [5, 6, 7, 8]]
