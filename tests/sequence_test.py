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

from typing import Literal

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
@allure.story("分割序列")
@allure.description("序列工具类, 用于处理序列相关的操作")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Sequence", "util")
class TestSequenceUtil:
    @allure.title("测试按子集数量切分序列")
    @pytest.mark.parametrize(
        "base,cnt,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 1, [[1, 2, 3, 4, 5, 6, 7, 8, 9]]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10, [[1], [2], [3], [4], [5], [6], [7], [8], [9]]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[1, 2], [3, 4], [5, 6], [7, 8, 9]]),
            pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, [], marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_split_sequence(cls, base, cnt, expected) -> None:
        assert SequenceUtil.split_seq(base, cnt) == expected

    @allure.title("测试按照每组元素数切分")
    @pytest.mark.parametrize(
        "lst,n,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[1, 2, 3, 4], [5, 6, 7, 8], [9]]),
        ],
    )
    def test_get_chunks(
        self,
        lst,
        n,
        expected,
    ):
        assert list(SequenceUtil.get_chunks(lst, n)) == expected

    @allure.title("测试切分序列为两半")
    @pytest.mark.parametrize(
        "base,left,right",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4], [5, 6, 7, 8, 9]),
            ([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4], [5, 6, 7, 8]),
            ([1, 2, 3, 4, 5, 6, 7], [1, 2, 3], [4, 5, 6, 7]),
        ],
    )
    def test_split_half(cls, base, left, right) -> None:
        assert SequenceUtil.split_half(base)[0] == left
        assert SequenceUtil.split_half(base)[1] == right


@allure.feature("序列工具类")
@allure.story("判断序列状态")
@allure.description("判断序列的状态，是否有序，是否重复，是否为空等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Sequence", "util")
class TestSequenceStatus:
    @allure.title("测试判断序列是否为空")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([], True),
            ([1, 2, 3], False),
            ([1, 2, 3, 3], False),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], False),
        ],
    )
    def test_is_empty(
        self,
        base,
        expected,
    ) -> None:
        assert SequenceUtil.is_empty(base) == expected
        assert SequenceUtil.is_not_empty(base) != expected

    @allure.title("测试子序列是否相同")
    @pytest.mark.parametrize(
        "main_seq,sub_seq,split_length,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 15, 16, 17, 18, 19], 5, False),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8], 4, True),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, True),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 10], 5, True),
            ([], [1, 2, 3], 3, False),
            ([1, 2, 3], [], 3, False),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 10], 5, True),
        ],
    )
    def test_is_sub_equal(
        self,
        main_seq: list[int],
        sub_seq: list[int],
        split_length: int,
        expected: Literal[5],
    ):
        assert SequenceUtil.is_sub_equal(main_seq, 0, sub_seq, 0, split_length) == expected
        assert not SequenceUtil.is_sub_equal(main_seq, -1, sub_seq, 0, split_length)
        assert not SequenceUtil.is_sub_equal(main_seq, 0, sub_seq, -1, split_length)

    @allure.title("判断序列中是否包含 None")
    @pytest.mark.parametrize(
        "seq, expected",
        [
            ([1, 2, 3], False),
            ([1, 2, None, 3], True),
            ([None, 2, 3], True),
            ([None, None, None], True),
            ([], False),
        ],
    )
    def test_has_none_has_none(self, seq, expected):
        assert SequenceUtil.has_none(seq) == expected

    @allure.title("判断序列是否包含多个指定元素之一")
    @pytest.mark.parametrize(
        "base,values,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3], True),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 10, 8, 99], True),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [11, 10, 81, 99], False),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [], False),
        ],
    )
    def test_contains_any(self, base, values, expected):
        assert SequenceUtil.contains_any(base, *values) == expected

    @allure.title("测试判断序列是否有序")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], True),
            ([1, 2, 3, 4, 5, 6, 7, 8], True),
            ([1, 2, 3, 4, 5, 6, 7], True),
            ([1, 2, 3, 4, 5, 6, 10, 9], False),
            ([1, 2, 3, 4, 5, 6, 7, 11, 10], False),
            ([1, 2, 13, 4, 5, 6, 7, 8, 9, 10], False),
            ([], True),
        ],
    )
    def test_is_sorted(
        self,
        base,
        expected,
    ):
        assert SequenceUtil.is_sorted(base) == expected


@allure.feature("序列工具类")
@allure.story("修改序列")
@allure.description("修改序列的元素，排序，去重等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Sequence", "util")
class TestChangeSequence:
    @allure.title("倒序序列")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 8, 7, 6, 5, 4, 3, 2, 1]),
            ([1, 2, 3, 4, 5, 6, 7, 8], [8, 7, 6, 5, 4, 3, 2, 1]),
            ([1, 2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2, 1]),
            ([], []),
        ],
    )
    def test_reverse_sequence(self, base, expected) -> None:
        assert SequenceUtil.reverse_sequence(base) == expected

    @allure.title("测试调整序列大小")
    @pytest.mark.parametrize(
        "base,new_size,fill_val,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
            ([1, 2, 3, 4, 5, 6, 7, 8], 6, 0, [1, 2, 3, 4, 5, 6]),
            ([1, 2, 3, 4, 5, 6, 7], 4, 0, [1, 2, 3, 4]),
            ([1, 2, 3, 4, 5, 6, 7], 8, 0, [1, 2, 3, 4, 5, 6, 7, 0]),
            ([1, 2, 3, 4, 5, 6, 7], 0, 0, []),
            ([1, 2, 3, 4, 5, 6, 7], -1, 0, [1, 2, 3, 4, 5, 6, 7]),
            ([1, 2, 3, 4, 5, 6, 7], 8, None, [1, 2, 3, 4, 5, 6, 7, None]),
        ],
    )
    def test_resize_sequence(
        self,
        base,
        new_size,
        fill_val,
        expected,
    ):
        assert SequenceUtil.resize(base, new_size, fill_val=fill_val) == expected

    @allure.title("测试移除序列中所有的 None 元素")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ([1, 2, 3, 4, 5, 6, 7, 8, None, None], [1, 2, 3, 4, 5, 6, 7, 8]),
        ],
    )
    def test_remove_none(
        self,
        base,
        expected,
    ):
        assert SequenceUtil.remove_none(base) == expected

    @allure.title("测试移除序列中所有的布尔元算为假的元素")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([True, True, True], [True, True, True]),
            ([True, False, True], [True, True]),
            ([0, -1, 1], [-1, 1]),
        ],
    )
    def test_remove_false_item(
        self,
        base,
        expected,
    ):
        assert SequenceUtil.remove_false(base) == expected

    @allure.title("测试循环移动序列")
    @pytest.mark.parametrize(
        "base,movement,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 1, [9, 1, 2, 3, 4, 5, 6, 7, 8]),
            ([1, 2, 3, 4, 5, 6, 7, 8], 2, [8, 1, 2, 3, 4, 5, 6, 7]),
            ([1, 2, 3, 4, 5, 6, 7], 3, [7, 1, 2, 3, 4, 5, 6]),
            ([1, 2, 3, 4, 5, 6, 7], -1, [7, 1, 2, 3, 4, 5, 6]),
            ([1, 2, 3, 4, 5, 6, 7], -2, [6, 1, 2, 3, 4, 5, 7]),
            ([1, 2, 3, 4, 5, 6, 7], -3, [5, 1, 2, 3, 4, 6, 7]),
            ([1, 2, 3, 4, 5, 6, 7], -4, [4, 1, 2, 3, 5, 6, 7]),
            ([], 5, []),
            ([1, 2, 3, 4, 5, 6, 7, 8], 17, [8, 1, 2, 3, 4, 5, 6, 7]),
        ],
    )
    def test_cycle_move_sequence(
        self,
        base,
        movement,
        expected,
    ):
        SequenceUtil.cycle_shift(base, movement) == expected

    @allure.title("测试合并多个范围")
    @pytest.mark.parametrize(
        "values,expected",
        [
            ([(1, 3), (2, 4), (5, 6)], [(1, 4), (5, 6)]),
            ([(1, 3), (2, 4), (7, 8)], [(1, 4), (7, 8)]),
            ([(1, 3), (2, 5), (4, 7), (6, 8)], [(1, 8)]),
            ([(10, 20), (15, 25), (30, 40), (35, 45)], [(10, 25), (30, 45)]),
            ([(1, 5), (2, 3), (4, 6)], [(1, 6)]),
            ([], []),
        ],
    )
    def test_merge_ranges(
        self,
        values,
        expected,
    ):
        assert SequenceUtil.merge_ranges(*values) == expected


@allure.feature("序列工具类")
@allure.story("获取序列中的元素")
@allure.description("获取序列中的元素，例如获取序列中第3个元素、第一个 None 元素等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("Sequence", "util")
class TestGetElement:
    @allure.title("获取序列中第{index}个元素")
    @pytest.mark.parametrize(
        "base,index,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 1),
            ([1, 2, 3, 4, 5, 6, 7, 8], 1, 2),
        ],
    )
    def test_get_element(self, base, index, expected):
        assert SequenceUtil.get_element(base, index) == expected

    @allure.title("测试获取序列中第一个 None 元素索引")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], -1),
            ([1, 2, 3, 4, 5, 6, 7, 8, None, None], 8),
            ([1, 2, 3, 4, 5, 6, 7, None, 9, None], 7),
            ([1, 2, 3, 4, 5, 6, None, 8, 9, None], 6),
        ],
    )
    def test_get_first_none_index(self, base, expected):
        assert SequenceUtil.first_idx_of_none(base) == expected

    @allure.title("测试获取序列中最后一个 None 元素索引")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], -1),
            ([1, 2, 3, 4, 5, 6, 7, None, 8, 10], 7),
            ([1, 2, 3, 4, 5, 6, 7, None, 9, None], 9),
            ([1, 2, 3, 4, 5, 6, None, 8, 9, None], 9),
        ],
    )
    def test_get_last_none_index(self, base, expected):
        assert SequenceUtil.last_idx_of_none(base) == expected

    @allure.title("测试创建一个新的列表")
    @pytest.mark.parametrize(
        "capacity,fill_val,expected",
        [
            (3, 0, [0, 0, 0]),
            (5, 1, [1, 1, 1, 1, 1]),
            (10, 2, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]),
            (0, 3, []),
        ],
    )
    def test_create_new_list(
        self,
        capacity,
        fill_val,
        expected,
    ):
        assert SequenceUtil.new_list(capacity, fill_val) == expected

    @allure.title("测试展平列表")
    @pytest.mark.parametrize(
        "base,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
        ],
    )
    def test_flatten_list(self, base, expected):
        assert list(SequenceUtil.flatten_sequence(base)) == expected

    @allure.title("测试设置序列中的元素或者向序列添加元素")
    @pytest.mark.parametrize(
        "base,idx,val,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 10, [10, 2, 3, 4, 5, 6, 7, 8, 9]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], -5, 10, [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], -1, 10, [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ([1, 2, 3, 4, 5, 6, 7, 8], 1, 10, [1, 10, 3, 4, 5, 6, 7, 8]),
            ([1, 2, 3, 4, 5, 6, 7], 2, 10, [1, 2, 10, 4, 5, 6, 7]),
            ([1, 2, 3, 4, 5, 6, 7], 7, 10, [1, 2, 3, 4, 5, 6, 7, 10]),
            ([1, 2, 3, 4, 5, 6, 7], 8, 10, [1, 2, 3, 4, 5, 6, 7, 10]),
        ],
    )
    def test_set_or_append(
        self,
        base,
        idx,
        val,
        expected,
    ):
        assert SequenceUtil.set_or_append(base, idx, val) == expected

    @allure.title("测试获取子序列")
    @pytest.mark.parametrize(
        "lst, start, end, include_last, expected",
        [
            ([1, 2, 3, 4, 5], 1, 3, True, [2, 3, 4]),
            ([1, 2, 3, 4, 5], 1, 3, False, [2, 3]),
            ([1, 2, 3, 4, 5], 0, None, False, [1, 2, 3, 4, 5]),
            ([1, 2, 3, 4, 5], 0, 5, True, [1, 2, 3, 4, 5]),
            ([1, 2, 3, 4, 5], 0, 0, True, [1]),
            ([1, 2, 3, 4, 5], 4, 4, False, []),
            pytest.param([1, 2, 3, 4, 5], -1, 3, False, "", marks=pytest.mark.xfail(raises=ValueError)),
            pytest.param([1, 2, 3, 4, 5], 5, 3, False, "", marks=pytest.mark.xfail(raises=ValueError)),
            pytest.param([1, 2, 3, 4, 5], 11, 17, False, "", marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_sub_sequence(
        self,
        lst,
        start,
        end,
        include_last,
        expected,
    ):
        assert SequenceUtil.sub_sequence(lst, start, end, include_last=include_last) == expected

    @allure.title("测试获取序列中前n个元素")
    @pytest.mark.parametrize(
        "base,n,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [1, 2, 3]),
            ([1, 2, 3, 4, 5, 6, 7, 8], 5, [1, 2, 3, 4, 5]),
            ([1, 2, 3, 4, 5, 6, 7], 8, [1, 2, 3, 4, 5, 6, 7]),
            ([1, 2, 3, 4, 5, 6, 7], 0, []),
            pytest.param([1, 2, 3, 4, 5, 6, 7], -1, "", marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_get_first_items(
        self,
        base,
        n,
        expected,
    ):
        assert SequenceUtil.get_first_items(base, n) == expected

    @allure.title("测试获取序列中第一个满足条件的元素")
    @pytest.mark.parametrize(
        "base,func,expected",
        [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], lambda x: x > 5, 6),
            ([1, 2, 3, 4, 5, 6, 7, 8], lambda x: x > 5, 6),
            ([1, 3, 2, 5, 7, 8, 9], lambda x: x % 2 == 0, 2),
        ],
    )
    def test_get_first_match(
        self,
        base,
        func,
        expected,
    ):
        SequenceUtil.get_first_match(base, func) == expected
