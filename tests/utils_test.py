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

import inspect
import random
import re

import pytest
from faker import Faker
from loguru import logger

from .context_test import (
    CollectionUtil,
    PatternPool,
    RandomUtil,
    ReUtil,
    SequenceUtil,
    StringUtil,
    TypeUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


class BaseTest:
    TEST_ROUND = 100


class TestReUtil:
    @classmethod
    def test_is_match_regex(cls):
        assert ReUtil.is_match(re.compile(r"\d+"), "123456")
        words = "...words, words..."
        pattern = re.compile(r"(\W+)")
        assert ReUtil.is_match(pattern, words)
        res = ReUtil.get_group_1(pattern, words)
        logger.debug(f"{res=}")

    @classmethod
    def test_get_group_0(cls):
        birthday = "20221201"
        matched = PatternPool.BIRTHDAY_PATTERN.findall(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = PatternPool.BIRTHDAY_PATTERN.search(birthday)
        res3 = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        _ = res3.groups()
        print(matched)


class TestRandomUtil:
    TEST_ROUND = 100

    @classmethod
    def test_get_random_boolean(cls):
        for _ in range(cls.TEST_ROUND):
            assert RandomUtil.get_random_boolean() in [True, False]

    @classmethod
    def test_get_random_val_from_range_with_wrong_arguments(cls):
        with pytest.raises(ValueError):
            RandomUtil.get_random_val_from_range(10, 1)

    @classmethod
    def test_get_random_item_from_sequence(cls):
        sequence = []
        assert RandomUtil.get_random_item_from_sequence(sequence) is None

    @classmethod
    def test_get_random_items_from_sequence_with_correct_arguments(cls):
        empty_sequence = []
        assert RandomUtil.get_random_items_from_sequence(empty_sequence, 1) == []
        sequence = [1, 2, 3, 4, 5]
        random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 3)
        assert SequenceUtil.get_length(random_sequence) == 3

        random_sequence = RandomUtil.get_random_items_from_sequence(sequence, 15)
        assert random_sequence == sequence

    @classmethod
    def test_get_random_items_from_sequence_with_incorrect_arguments(cls):
        sequence = [1, 2, 3, 4, 5]
        with pytest.raises(ValueError):
            RandomUtil.get_random_items_from_sequence(sequence, -1)

    @classmethod
    def test_get_random_booleans(cls):
        for i in RandomUtil.get_random_booleans(5):
            assert isinstance(i, bool)

    @classmethod
    def test_get_random_float(cls):
        for _ in range(cls.TEST_ROUND):
            random_float = RandomUtil.get_random_float()
            assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_correct_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            random_generator = RandomUtil.get_random_floats_with_range_and_precision(0.0, 1.0, precision=2, length=5)
            for random_float in random_generator:
                assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_incorrect_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            with pytest.raises(ValueError):
                random_generator = RandomUtil.get_random_floats_with_range_and_precision(
                    1.0, 0.0, precision=2, length=5
                )
                for i in random_generator:
                    pass

    @classmethod
    def test_get_random_complex(cls):
        for _ in range(cls.TEST_ROUND):
            random_complex = RandomUtil.get_random_complex()
            assert isinstance(random_complex, complex)

    @classmethod
    def test_get_random_complexes_with_range_and_precision(cls):
        random_generator = RandomUtil.get_random_complexes_with_range_and_precision((0, 1), (-1, 1))
        lst = list(random_generator)
        assert len(lst) == 10
        for i in random_generator:
            real_part = i.real
            imag_part = i.imag

            assert 0 <= real_part <= 1
            assert -1 <= imag_part <= 1


class TestSequenceUtil(BaseTest):
    @classmethod
    def test_get_chunks(cls) -> None:
        test_seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks = SequenceUtil.get_chunks(test_seq_1, 3)
        assert next(chunks) == [1, 2, 3]
        assert next(chunks) == [4, 5, 6]
        assert next(chunks) == [7, 8, 9]
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_2 = [1, 2, 3, 4]
        chunks = SequenceUtil.get_chunks(test_seq_2, 3)
        assert next(chunks) == [1, 2, 3]
        assert next(chunks) == [4]
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_3: list[int] = []
        chunks = SequenceUtil.get_chunks(test_seq_3, 3)
        with pytest.raises(StopIteration):
            next(chunks)

        test_seq_4 = None
        chunks = SequenceUtil.get_chunks(test_seq_4, 3)
        with pytest.raises(ValueError):
            next(chunks)

    @classmethod
    def test_(cls) -> None:
        test_seq_1 = [1, [2, 3], 4, [5, [6, 7]]]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_1)
        assert list(flatten_lst) == [1, 2, 3, 4, 5, 6, 7]

        test_seq_2 = [1, [2, 3], 4, [5, [6, 7]]]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_2)
        for i in range(1, 8):
            assert next(flatten_lst) == i

        test_seq_3 = [1, 2, 3, 4, 5]
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_3)
        for i in range(1, 6):
            assert next(flatten_lst) == i

        test_seq_4 = []  # type: ignore
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_4)
        with pytest.raises(StopIteration):
            next(flatten_lst)

        test_seq_5 = None  # type: ignore
        flatten_lst = SequenceUtil.flatten_sequence(test_seq_5)  # type: ignore
        with pytest.raises(TypeError):
            next(flatten_lst)

    @classmethod
    def test_is_not_empty(cls) -> None:
        lst = [1, 2, 3]
        assert SequenceUtil.is_not_empty(lst)
        assert not SequenceUtil.is_not_empty([])

    @classmethod
    def test_reverse_sequence(cls) -> None:
        lst = [1, 2, 3]
        reversed_lst = SequenceUtil.reverse_sequence(lst)
        assert reversed_lst == [3, 2, 1]

    @classmethod
    def test_has_none(cls) -> None:
        assert not SequenceUtil.has_none([1, 2, 3])
        assert SequenceUtil.has_none([1, 2, None])

    @classmethod
    def test_new_list(cls) -> None:
        assert SequenceUtil.new_list(5, 0) == [0, 0, 0, 0, 0]
        assert SequenceUtil.new_list(3) == [None, None, None]

    @classmethod
    def test_contains_any(cls) -> None:
        assert SequenceUtil.contains_any([1, 2, 3], *[2, 3, 4])  # True
        assert not SequenceUtil.contains_any([1, 2, 3], *[4, 5, 6])  # False

    @classmethod
    def test_first_idx_of_none(cls) -> None:
        assert SequenceUtil.first_idx_of_none([1, 2, 3]) == -1
        assert SequenceUtil.first_idx_of_none([1, 2, None]) == 2

    @classmethod
    def test_is_all_ele_equal(cls) -> None:
        assert SequenceUtil.is_all_element_equal([1, 1, 1, 1])  # True
        assert not SequenceUtil.is_all_element_equal([1, 2, 1, 1])  # False

    @classmethod
    def test_move(cls) -> None:
        original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for _ in range(cls.TEST_ROUND):
            move_length = random.randint(0, 100)
            res = SequenceUtil.rotate(original_list, move_length)
            logger.debug(f"{res=}, {move_length=}, {move_length % len(original_list)=}")


class TestCollectionUtil:
    @classmethod
    def test_powerset(cls):
        s = [1, 2, 3]
        for subset in CollectionUtil.get_powerset(s):
            for j in subset:
                logger.debug(j)

    @classmethod
    def test_nested_dict_iter(cls):
        d = {"a": {"a": {"y": 2}}, "b": {"c": {"a": 5}}, "x": {"a": 6}}
        list(CollectionUtil.nested_dict_iter(d))

    @classmethod
    def test_split_sequence(cls) -> None:
        test_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_sequence(test_seq, 3) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 1) == [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
        assert SequenceUtil.split_sequence(test_seq, 10) == [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
        SequenceUtil.split_sequence(test_seq, 4) == [[1, 2], [3, 4], [5, 6], [7, 8, 9]]
        with pytest.raises(ValueError):
            assert SequenceUtil.split_sequence(test_seq, 0) == []

    @classmethod
    def test_split_half(cls) -> None:
        test_seq_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert SequenceUtil.split_half(test_seq_1) == [[1, 2, 3, 4], [5, 6, 7, 8, 9]]
        test_seq_2 = [1, 2, 3, 4, 5, 6, 7, 8]
        assert SequenceUtil.split_half(test_seq_2) == [[1, 2, 3, 4], [5, 6, 7, 8]]


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
