#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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

import random
import re
from datetime import date, datetime, timedelta

import pytest
from loguru import logger

from .context import (
    BooleanUtil,
    CollectionUtil,
    DatetimeUtil,
    DatetimeValidator,
    IDCardUtil,
    OsUtil,
    PatternPool,
    RadixUtil,
    RandomUtil,
    ReUtil,
    SequenceUtil,
    StringUtil,
    StringValidator,
    SysUtil,
    ValidationError,
)


class TestStringUtil:
    @classmethod
    def test_is_blank(cls):
        assert StringUtil.is_blank(None)
        assert StringUtil.is_blank("")
        assert StringUtil.is_blank(" \t\n")
        assert not StringUtil.is_blank("abc")

    @classmethod
    def test_all_blank(cls):
        pass

    @classmethod
    def test_center(cls):
        a = StringUtil.get_center_msg("hello world", "=", 40)
        b = StringUtil.get_center_msg("hello world", "=", 1)
        logger.debug(a)
        logger.debug(b)

    @classmethod
    def test_and_all_with_correct_arguments(cls) -> None:
        assert not BooleanUtil.and_all(True, False, False, True)
        assert not BooleanUtil.and_all(False, False, False, False)
        assert BooleanUtil.and_all(True, True, True, True)
        assert not BooleanUtil.and_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.and_all(True, "", True, True, strict_mode=False)

    @classmethod
    def test_and_all_with_incorrect_argumens(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.and_all()

    @classmethod
    def test_or_all_with_correct_arguments(cls) -> None:
        assert BooleanUtil.or_all(True, False, False, True)
        assert not BooleanUtil.or_all(False, False, False, False)
        assert BooleanUtil.or_all(True, True, True, True)
        assert BooleanUtil.or_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.or_all(False, "", False, False, strict_mode=False)

    @classmethod
    def test_or_all_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.or_all()

    @classmethod
    def test_resize(cls) -> None:
        lst = [1, 2, 3]
        new_lst = SequenceUtil.resize(lst, -1)
        logger.debug(new_lst)

    def test_validate(self):
        assert DatetimeValidator.is_valid_birthday("19980424")
        assert not DatetimeValidator.is_valid_birthday("19981424")

    def test_id_valid(self):
        assert IDCardUtil.is_valid_id_18("110105199804246510")
        assert not IDCardUtil.is_valid_id_18("110105199804246511")

    def test_date_sub(self):
        now = datetime.now() + timedelta(days=1)
        res = now - datetime.now()
        logger.debug(type(res))


class TestDateTimeUtil:
    TEST_ROUND = 10

    @classmethod
    def test_get_random_datetime_with_no_args(cls):
        for _ in range(cls.TEST_ROUND):
            res = DatetimeUtil.get_random_datetime()
            logger.debug(f"{res=}")

    @classmethod
    def test_get_random_datetime_with_no_args_include_tz(cls):
        for _ in range(cls.TEST_ROUND):
            res = DatetimeUtil.get_random_datetime(random_tz=True)
            logger.debug(f"{res=}")

    @classmethod
    def test_get_random_date_with_no_args(cls):
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date())

    @classmethod
    def test_get_random_date_with_one_args(cls):
        start = date(1998, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date(start))

    @classmethod
    def test_get_random_date_with_two_args(cls):
        start = datetime(1998, 4, 24)
        end = datetime(2021, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DatetimeUtil.get_random_date(start, end))

    @classmethod
    def test_get_random_date_with_wrong_args(cls):
        with pytest.raises(ValueError):
            end = datetime(1998, 4, 24)
            start = datetime(2021, 4, 24)
            logger.debug(DatetimeUtil.get_random_date(start, end))

        with pytest.raises(ValueError):
            start = datetime(1998, 4, 24)
            end = datetime(1998, 4, 24)
            logger.debug(DatetimeUtil.get_random_date(start, end))

    @classmethod
    def test_get_this_year(cls):
        for _ in range(cls.TEST_ROUND):
            assert DatetimeUtil.this_year() == 2024
            assert not DatetimeUtil.this_year() == 2025

    @classmethod
    def test_get_this_month(cls):
        for _ in range(cls.TEST_ROUND):
            assert DatetimeUtil.this_month() == 7
            assert not DatetimeUtil.this_month() == 9

    @classmethod
    def test_get_this_day(cls):
        DatetimeUtil.this_day()

    @classmethod
    def test_get_this_hour(cls):
        DatetimeUtil.this_hour()

    @classmethod
    def test_get_this_minute(cls):
        DatetimeUtil.this_minute()

    @classmethod
    def test_get_this_second(cls):
        DatetimeUtil.this_second()

    @classmethod
    def test_is_leap_year(cls):
        assert DatetimeUtil.is_leap_year(2024)
        assert not DatetimeUtil.is_leap_year(2025)
        assert not DatetimeUtil.is_leap_year(1900)
        assert not DatetimeUtil.is_leap_year(2100)

    @classmethod
    def test_is_same_quarter(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime()
            d2 = DatetimeUtil.get_random_datetime()
            res = DatetimeUtil.is_same_quarter(d1, d2)
            logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

    @classmethod
    def test_is_same_week(cls):
        for _ in range(cls.TEST_ROUND):
            d1 = DatetimeUtil.get_random_datetime(
                datetime(2024, 12, 1), datetime(2024, 12, 15)
            )
            d2 = DatetimeUtil.get_random_datetime(
                datetime(2024, 12, 1), datetime(2024, 12, 15)
            )
            res = DatetimeUtil.is_same_week(d1, d2)
            logger.debug(f"d1={repr(d1)}, d2={repr(d2)}, {res=}")

    @classmethod
    def test_get_age(cls):
        dt = datetime(1998, 4, 24)
        res = DatetimeUtil.get_age(dt)
        logger.debug(f"{res=}")

    @classmethod
    def test_time_unit_convert(cls):
        for i in range(cls.TEST_ROUND):
            duration = i * 1000
            res = DatetimeUtil.nanos_to_millis(duration)
            res_second = DatetimeUtil.nanos_to_seconds(duration * 1000)
            logger.debug(f"{i=}, {res=}, {res_second=}")

    @classmethod
    def test_second_to_time(cls):
        for i in range(cls.TEST_ROUND):
            val = random.randrange(1000, 10000, 1000)
            res = DatetimeUtil.second_to_time(val)
            logger.debug(f"{i=}, {val=}, {res=}")


class TestIdUtil:
    TEST_ROUND = 10000

    @classmethod
    def test_generate_random_id(cls):
        for _ in range(cls.TEST_ROUND):
            id_str = IDCardUtil.generate_random_valid_id()
            IDCardUtil.generate_random_valid_id(code_length=15)
            logger.debug(id_str)
            assert IDCardUtil.is_valid_id(id_str)

        with pytest.raises(ValueError):
            IDCardUtil.generate_random_valid_id(code_length=21321)

    @classmethod
    def test_generate_random_idcard(cls):
        for _ in range(cls.TEST_ROUND):
            id_obj = IDCardUtil.generate_random_valid_card()
            logger.debug(id_obj)

    @classmethod
    def test_get_birthday_from_id_with_wrong_args(cls):
        assert IDCardUtil.get_birthday_from_id("") is None
        assert IDCardUtil.get_birthday_from_id(1) is None
        assert IDCardUtil.get_birthday_from_id("1") is None
        assert IDCardUtil.get_birthday_from_id("adac") is None
        assert IDCardUtil.get_birthday_from_id("110105199804246511") is None

    @classmethod
    def test_is_valid_id_18(cls):
        assert IDCardUtil.is_valid_id_18("110105199804246510")
        assert not IDCardUtil.is_valid_id_18("1101051998042465")
        assert not IDCardUtil.is_valid_id_18("a10105199804246510")
        assert not IDCardUtil.is_valid_id_18("110105199813246510")

    @classmethod
    def test_is_valid_id(cls):
        id = "123456789012345"
        with pytest.raises(NotImplementedError):
            IDCardUtil.is_valid_id(id)


class TestSysUtil:
    @classmethod
    def test_list_file(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        res = OsUtil.list_files(p, check_exist=False)
        logger.debug(res)

        res = OsUtil.list_files(p, check_exist=True)
        logger.debug(res)

    @classmethod
    def test_is_windows(cls):
        assert not SysUtil.is_windows_platform()

    @classmethod
    def test_is_mac(cls):
        assert SysUtil.is_mac_platform()

    @classmethod
    def test_is_linux(cls):
        assert not SysUtil.is_linux_platform()

    @classmethod
    def test_is_python3(cls):
        assert SysUtil.is_py3()

    @classmethod
    def test_is_python2(cls):
        assert not SysUtil.is_py2()

    @classmethod
    def test_get_system_var(cls):
        assert "/Users/panchenxi" == SysUtil.get_system_property("HOME")
        assert "panchenxi" == SysUtil.get_system_property("USER")
        assert "/bin/zsh" == SysUtil.get_system_property("SHELL")

        assert SysUtil.get_system_property("dadsdsaadsa", None) is None
        assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1)
        assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1, quiet=True)
        assert 1 == SysUtil.get_system_property("dadsdsaadsa", 1, quiet=False)


class TestOsUtil:
    @classmethod
    def test_is_contain_hidden_dir(cls):
        assert OsUtil.is_contain_hidden_dir("/.git")
        assert OsUtil.is_contain_hidden_dir(".git")
        assert OsUtil.is_contain_hidden_dir(".svn/sad/")
        assert OsUtil.is_contain_hidden_dir("/tmp/__pychache__")
        assert OsUtil.is_contain_hidden_dir("/tmp/__pychache__/pancx")
        assert OsUtil.is_contain_hidden_dir("__pycache__")
        assert not OsUtil.is_contain_hidden_dir("/hidden")
        assert not OsUtil.is_contain_hidden_dir("hidden")
        assert not OsUtil.is_contain_hidden_dir("usr/local/")
        assert not OsUtil.is_contain_hidden_dir("/ust/local/security/")

    @classmethod
    def test_is_exist(cls):
        assert not OsUtil.is_exist("")
        assert not OsUtil.is_exist("")
        assert OsUtil.is_exist("/")
        assert OsUtil.is_exist("/tmp")
        assert OsUtil.is_exist(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        )
        assert OsUtil.is_exist("/Users/")
        assert not OsUtil.is_exist("dsaddaasawdasdwa")

    @classmethod
    def test_is_dir(cls):
        assert not OsUtil.is_dir("")
        assert OsUtil.is_dir("/")
        assert OsUtil.is_dir("/tmp")
        assert OsUtil.is_dir(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        )

        assert not OsUtil.is_dir(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
            "/PythonTools/pythontools/component/basic_utils.py",
            raise_exception=False,
        )
        with pytest.raises(Exception):
            OsUtil.is_dir("dsaddaasawdasdwa", raise_exception=True)

    @classmethod
    def test_is_file(cls):
        assert not OsUtil.is_file("")
        assert not OsUtil.is_file("/tmp")
        assert OsUtil.is_file(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/core/basicutils.py",
            raise_exception=False,
        )

        with pytest.raises(ValueError):
            OsUtil.is_file("dsaddaasawdasdwa", raise_exception=True)

    @classmethod
    def test_get_file_create_time(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
        OsUtil.get_file_create_time(p)
        with pytest.raises(FileNotFoundError):
            OsUtil.get_file_create_time(p + "dadada", check_exist=True)

    @classmethod
    def test_list_dirs(cls):
        res = OsUtil.list_dirs(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        )
        logger.debug(res)

        OsUtil.list_dirs(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools",
            check_exist=True,
        )

    @classmethod
    def test_get_extension_from_path(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
        extension = OsUtil.get_extension_from_path(p)
        assert ".py" == extension

    @classmethod
    def test_is_match_extension(cls):
        with pytest.raises(ValueError):
            OsUtil.is_match_extension(".tm", "")

        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
        assert OsUtil.is_match_extension(p, "py")
        assert OsUtil.is_match_extension(p, ".py")

    @classmethod
    def test_get_file_from_dir_by_extension(cls):
        p = (
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools"
            "/component/"
        )
        res = OsUtil.get_file_from_dir_by_extension(p, extension="py")
        logger.debug(res)


class TestValidator:
    @classmethod
    def test_is_general_str(cls):
        s = "seda"
        StringValidator.is_general_string(s)
        with pytest.raises(ValidationError):
            StringValidator.is_general_string("123@", raise_exception=True)

    @classmethod
    def test_is_valid_date(cls):
        assert DatetimeValidator.is_valid_date(2022, 12, 1)
        assert DatetimeValidator.is_valid_date(2024, 2, 29)
        assert DatetimeValidator.is_valid_date(1900, 2, 28)
        assert DatetimeValidator.is_valid_date(2022, 3, 31)
        assert not DatetimeValidator.is_valid_date(2022, 12, 33)
        assert not DatetimeValidator.is_valid_date(2022, 13, 1)
        assert not DatetimeValidator.is_valid_date(2022, 2, 29)
        assert not DatetimeValidator.is_valid_date(1900, 2, 29)
        assert not DatetimeValidator.is_valid_date(0, 1, 1)
        assert not DatetimeValidator.is_valid_date(2022, 4, 31)

    @classmethod
    def test_is_valid_birthday(cls):
        assert DatetimeValidator.is_valid_birthday("20221201")
        assert DatetimeValidator.is_valid_birthday("20240229")
        assert DatetimeValidator.is_valid_birthday("19000228")
        assert not DatetimeValidator.is_valid_birthday("2022331")
        assert DatetimeValidator.is_valid_birthday("2024年4月24日")
        assert not DatetimeValidator.is_valid_birthday("2022131")
        assert not DatetimeValidator.is_valid_birthday("20221233")
        assert not DatetimeValidator.is_valid_birthday("2022229")
        assert not DatetimeValidator.is_valid_birthday("19000229")
        assert not DatetimeValidator.is_valid_birthday("011")
        assert not DatetimeValidator.is_valid_birthday("20220431")

    @classmethod
    def test_is_json_str(cls):
        assert StringValidator.is_json('{"name": "Peter"}')
        assert StringValidator.is_json("[1, 2, 3]")
        assert not StringValidator.is_json("{nope}")
        assert not StringValidator.is_json("nope")
        assert not StringValidator.is_json("")
        assert not StringValidator.is_json(None)


class TestReUtil(object):
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
        res = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        res2 = PatternPool.BIRTHDAY_PATTERN.search(birthday)
        res3 = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        r = res3.groups()
        print(matched)


class TestRadixUtil(object):
    @classmethod
    def test_decimal_to_any(cls):
        assert RadixUtil.convert_base("1011", 2, 10) == "11"
        assert RadixUtil.convert_base("11", 10, 2) == "1011"
        assert RadixUtil.convert_base("A", 16, 2) == "1010"
        assert RadixUtil.convert_base("1010", 2, 16) == "A"
        assert RadixUtil.convert_base("255", 10, 16) == "FF"
        assert RadixUtil.convert_base("FF", 16, 10) == "255"
        assert RadixUtil.convert_base("10101010", 2, 16) == "AA"
        assert RadixUtil.convert_base("AA", 16, 2) == "10101010"
        assert RadixUtil.convert_base("10101010", 2, 8) == "252"
        assert RadixUtil.convert_base("252", 8, 2) == "10101010"


class TestBooleanUtil(object):
    @classmethod
    def test_negate_with_correct_arguments(cls) -> None:
        assert not BooleanUtil.negate(True)
        assert BooleanUtil.negate(False)

    @classmethod
    def test_negate_with_incorrect_arguments(cls) -> None:
        with pytest.raises(TypeError):
            BooleanUtil.negate(1, raise_exception=True)

        assert not BooleanUtil.negate(1, raise_exception=False)

    @classmethod
    def test_negate_with_incorrect_arguments_and_default_value(cls) -> None:
        assert not BooleanUtil.negate(1)
        assert BooleanUtil.negate(0)

    @classmethod
    def test_xor_with_correct_arguments(cls) -> None:
        assert BooleanUtil.xor(True, False)
        assert not BooleanUtil.xor(True, False, True)
        assert BooleanUtil.xor(True, False, False)
        assert not BooleanUtil.xor(True, True)

    @classmethod
    def test_xor_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.xor()

    @classmethod
    def test_boolean_to_int_with_correct_arguments(cls) -> None:
        state = True
        assert BooleanUtil.boolean_to_int(state) == 1
        assert BooleanUtil.boolean_to_int(not state) == 0

    @classmethod
    def test_boolean_to_int_with_incorrect_arguments(cls) -> None:
        with pytest.raises(ValueError):
            BooleanUtil.boolean_to_int(1, strict_mode=True) == 1

        assert BooleanUtil.boolean_to_int(1, strict_mode=False) == 1
        assert BooleanUtil.boolean_to_int(1) == 1

    @classmethod
    def test_str_to_boolean(cls) -> None:
        assert not BooleanUtil.str_to_boolean("")
        assert BooleanUtil.str_to_boolean("True")
        assert BooleanUtil.str_to_boolean("对")
        assert BooleanUtil.str_to_boolean("ok")
        assert not BooleanUtil.str_to_boolean("false")
        assert not BooleanUtil.str_to_boolean("no")
        assert not BooleanUtil.str_to_boolean("0")
        assert not BooleanUtil.str_to_boolean("错")
        assert not BooleanUtil.str_to_boolean("×")

    @classmethod
    def test_to_str_true_and_false(cls) -> None:
        assert BooleanUtil.to_str_true_and_false(True) == "TRUE"
        assert BooleanUtil.to_str_true_and_false(False) == "FALSE"

    @classmethod
    def test_to_str_yes_no(cls) -> None:
        assert BooleanUtil.to_str_yes_no(True) == "YES"
        assert BooleanUtil.to_str_yes_no(False) == "NO"


class TestRandomUtil(object):
    TEST_ROUND = 100

    @classmethod
    def test_random_str(cls):
        res = RandomUtil.get_random_chinese()
        for _ in range(cls.TEST_ROUND):
            assert 0x4E00 <= ord(res) < 0x9FA5

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
    def test_get_random_chineses(cls):
        for _ in range(cls.TEST_ROUND):
            random_chinese_string = RandomUtil.get_random_chinese()
            assert StringValidator.is_chinese(random_chinese_string)

    @classmethod
    def test_get_random_float(cls):
        for _ in range(cls.TEST_ROUND):
            random_float = RandomUtil.get_random_float()
            assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_correct_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            random_generator = RandomUtil.get_random_floats_with_range_and_precision(
                0.0, 1.0, precision=2, length=5
            )
            for random_float in random_generator:
                assert 0.0 <= random_float <= 1.0 and isinstance(random_float, float)

    @classmethod
    def test_get_random_floats_with_range_and_precision_and_incorrect_arguments(cls):
        for _ in range(cls.TEST_ROUND):
            with pytest.raises(ValueError):
                random_generator = (
                    RandomUtil.get_random_floats_with_range_and_precision(
                        1.0, 0.0, precision=2, length=5
                    )
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
        random_generator = RandomUtil.get_random_complexes_with_range_and_precision(
            (0, 1), (-1, 1)
        )
        lst = list(random_generator)
        assert len(lst) == 10
        for i in random_generator:
            real_part = i.real
            imag_part = i.imag

            assert 0 <= real_part <= 1
            assert -1 <= imag_part <= 1

    @classmethod
    def test_get_random_date(cls):
        for _ in range(cls.TEST_ROUND):
            random_val = RandomUtil.get_random_date()
            assert isinstance(random_val, date)

    @classmethod
    def test_get_random_datetime(cls):
        for _ in range(cls.TEST_ROUND):
            random_val = RandomUtil.get_random_datetime()
            assert isinstance(random_val, datetime)

    @classmethod
    def test_get_random_str_upper(cls):
        for _ in range(cls.TEST_ROUND):
            length = RandomUtil.get_random_val_from_range(1, 10)
            random_str = RandomUtil.get_random_str_upper(length)
            assert len(random_str) == length
            assert random_str.upper() == random_str

    @classmethod
    def test_get_random_str_lower(cls) -> None:
        for _ in range(cls.TEST_ROUND):
            length = RandomUtil.get_random_val_from_range(1, 10)
            random_str = RandomUtil.get_random_str_lower(length)
            assert len(random_str) == length
            assert random_str.lower() == random_str

    @classmethod
    def test_get_random_str_capitalized(cls) -> None:
        for _ in range(cls.TEST_ROUND):
            length = RandomUtil.get_random_val_from_range(1, 10)
            random_str = RandomUtil.get_random_str_capitalized(length)
            assert len(random_str) == length
            assert random_str.capitalize() == random_str


class TestSequenceUtil(object):
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
        assert SequenceUtil.is_all_ele_equal([1, 1, 1, 1])  # True
        assert not SequenceUtil.is_all_ele_equal([1, 2, 1, 1])  # False


class TestCollectionUtil(object):
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
