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
    DesensitizedUtil,
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


class TestUtil:
    @classmethod
    def test_desensitize_ipv4(cls) -> None:
        ipv4 = "192.0.2.1"
        assert DesensitizedUtil.desensitize_ipv4(ipv4) == "192.*.*.*"
        assert StringUtil.equals(DesensitizedUtil.desensitize_ipv4(ipv4.encode("utf-8")), "192.*.*.*")

    @classmethod
    def test_desensitize_ipv6(cls) -> None:
        ipv6 = "2001:0db8:86a3:08d3:1319:8a2e:0370:7344"
        assert DesensitizedUtil.desensitize_ipv6(ipv6) == "2001:*:*:*:*:*:*:*"
        assert StringUtil.equals(DesensitizedUtil.desensitize_ipv6(ipv6.encode("utf-8")), "2001:*:*:*:*:*:*:*")

    @classmethod
    def test_desensitize_email(cls) -> None:
        email1 = "duandazhi-jack@gmail.com.cn"
        assert DesensitizedUtil.desensitize_email(email1) == "d*************@gmail.com.cn"
        email2 = "duandazhi@126.com"
        assert StringUtil.equals("d********@126.com", DesensitizedUtil.desensitize_email(email2))
        email3 = "duandazhi@gmail.com.cn"
        assert StringUtil.equals("d********@gmail.com.cn", DesensitizedUtil.desensitize_email(email3))
        assert StringUtil.equals("d********@gmail.com.cn", DesensitizedUtil.desensitize_email(email3.encode("utf-8")))
        assert StringUtil.equals("", DesensitizedUtil.desensitize_email(""))

    @classmethod
    def test_desensitize_id_card(cls) -> None:
        id_card = "51343620000320711X"
        assert DesensitizedUtil.desensitize_id_card(id_card) == "513436********711X"
        assert StringUtil.equals(DesensitizedUtil.desensitize_id_card(id_card.encode("utf-8")), "513436********711X")

    @classmethod
    def test_desensitize_bank_card(cls) -> None:
        bank_card1 = "1234 2222 3333 4444 6789 9"
        assert DesensitizedUtil.desensitize_bank_card(bank_card1) == "1234 **** **** **** **** 9"
        bank_card2 = "1234 **** **** **** **** 91"
        assert DesensitizedUtil.desensitize_bank_card(bank_card2) == "1234 **** **** **** **** 91"
        bank_card3 = "1234 2222 3333 4444 6789"
        assert DesensitizedUtil.desensitize_bank_card(bank_card3) == "1234 **** **** **** 6789"
        bank_card4 = "1234 2222 3333 4444 678"
        assert DesensitizedUtil.desensitize_bank_card(bank_card4) == "1234 **** **** **** 678"
        # bytes
        assert StringUtil.equals(
            DesensitizedUtil.desensitize_bank_card(bank_card3.encode("utf-8")), "1234 **** **** **** 6789"
        )
        assert StringUtil.equals(DesensitizedUtil.desensitize_bank_card(""), "")

    @classmethod
    def test_desensitize_mobile_phone(cls) -> None:
        phone1 = "18049531999"
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_mobile_phone(phone1))
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_mobile_phone(phone1.encode("utf-8")))

    @classmethod
    def test_desensitize_fix_phone(cls) -> None:
        fix_phone1 = "09157518479"
        assert StringUtil.equals("091****8479", DesensitizedUtil.desensitize_fix_phone(fix_phone1))
        assert StringUtil.equals("091****8479", DesensitizedUtil.desensitize_fix_phone(fix_phone1.encode("utf-8")))

    @classmethod
    def test_desensitize_car_license(cls) -> None:
        car_license1 = "苏D40000"
        assert StringUtil.equals("苏D4***0", DesensitizedUtil.desensitize_car_license(car_license1))
        car_license2 = "陕A12345D"
        assert StringUtil.equals("陕A1****D", DesensitizedUtil.desensitize_car_license(car_license2))
        car_license3 = "京A123"
        with pytest.raises(ValueError) as _:
            assert StringUtil.equals("京A123", DesensitizedUtil.desensitize_car_license(car_license3))

        assert StringUtil.equals("陕A1****D", DesensitizedUtil.desensitize_car_license(car_license2.encode("utf-8")))
        assert StringUtil.equals("", DesensitizedUtil.desensitize_car_license(""))

    @classmethod
    def test_desensitize_address(cls) -> None:
        address = "北京市海淀区马连洼街道289号"
        assert StringUtil.equals("北京市海淀区马连洼街*****", DesensitizedUtil.desensitize_address(address, 5))
        assert StringUtil.equals("***************", DesensitizedUtil.desensitize_address(address, 50))
        assert StringUtil.equals("北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address, 0))
        assert StringUtil.equals("北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address, -1))
        # butes
        assert StringUtil.equals(
            "北京市海淀区马连洼街道289号", DesensitizedUtil.desensitize_address(address.encode("utf-8"), -1)
        )

    @classmethod
    def test_password(cls) -> None:
        password1 = "password"
        assert StringUtil.equals("********", DesensitizedUtil.desensitize_password(password1))
        assert StringUtil.equals("********", DesensitizedUtil.desensitize_password(password1.encode("utf-8")))

    @classmethod
    def test_desensitize_chineseName(cls) -> None:
        assert StringUtil.equals("段**", DesensitizedUtil.desensitize_chinese_name("段正淳"))
        assert StringUtil.equals("张*", DesensitizedUtil.desensitize_chinese_name("张三"))

    @classmethod
    def test_retain_last(cls) -> None:
        s = "asdasc"
        assert StringUtil.equals("*****c", DesensitizedUtil.retain_last(s))

    @classmethod
    def test_retain_front_and_end(cls) -> None:
        assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("", 3, 4))
        assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("  ", 3, 4))
        with pytest.raises(ValueError):
            assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("sad", 3, 4))

        with pytest.raises(ValueError):
            assert StringUtil.equals("", DesensitizedUtil.retain_front_and_end("sad", 3, -1))

    @classmethod
    def test_desensitize_phone(cls) -> None:
        phone = "18049531999"
        assert StringUtil.equals("180****1999", DesensitizedUtil.desensitize_phone(phone))
