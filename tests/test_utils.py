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
from datetime import date, datetime, timedelta

import pytest
from loguru import logger

from .context import (
    BooleanUtil,
    DatetimeUtil,
    IDCardUtil,
    OsUtil,
    SequenceUtil,
    StringUtil,
    SysUtil,
    Validator,
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
    def test_and_all(cls):
        assert not BooleanUtil.and_all(True, False, False, True)
        assert not BooleanUtil.and_all(False, False, False, False)
        assert BooleanUtil.and_all(True, True, True, True)
        assert not BooleanUtil.and_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.and_all(True, "", True, True, strict_mode=False)

    def test_or_all(cls):
        assert BooleanUtil.or_all(True, False, False, True)
        assert not BooleanUtil.or_all(False, False, False, False)
        assert BooleanUtil.or_all(True, True, True, True)
        assert BooleanUtil.or_all(True, 0, True, True, strict_mode=False)
        assert not BooleanUtil.or_all(False, "", False, False, strict_mode=False)

    def test_resize(self):
        lst = [1, 2, 3]
        new_lst = SequenceUtil.resize(lst, -1)
        logger.debug(new_lst)

    def test_validate(self):
        assert Validator.is_valid_birthday("19980424")
        assert not Validator.is_valid_birthday("19981424")

    def test_id_valid(self):
        assert IDCardUtil.is_valid_id_18("110105199804246510")
        assert not IDCardUtil.is_valid_id_18("110105199804246511")

    def test_date_sub(self):
        now = datetime.now() + timedelta(days=1)
        res = now - datetime.now()
        logger.debug(type(res))


class TestDateUtil:
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
    def test_day_of_month(cls):
        dt = datetime.now()
        res = DatetimeUtil.day_of_month(dt)
        logger.debug(res)

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
    TEST_ROUND = 100

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
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
            "/PythonTools/pythontools/component/basic_utils.py",
            raise_exception=False,
        )

        with pytest.raises(ValueError):
            OsUtil.is_file("dsaddaasawdasdwa", raise_exception=True)

    @classmethod
    def test_get_file_create_time(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
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

        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
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
    def test_is_valid_date(cls):
        assert Validator.is_valid_date(2022, 12, 1)
        assert Validator.is_valid_date(2024, 2, 29)
        assert Validator.is_valid_date(1900, 2, 28)
        assert Validator.is_valid_date(2022, 3, 31)
        assert not Validator.is_valid_date(2022, 12, 33)
        assert not Validator.is_valid_date(2022, 13, 1)
        assert not Validator.is_valid_date(2022, 2, 29)
        assert not Validator.is_valid_date(1900, 2, 29)
        assert not Validator.is_valid_date(0, 1, 1)
        assert not Validator.is_valid_date(2022, 4, 31)

    @classmethod
    def test_is_valid_birthday(cls):
        assert Validator.is_valid_birthday("20221201")
        assert Validator.is_valid_birthday("20240229")
        assert Validator.is_valid_birthday("19000228")
        assert not Validator.is_valid_birthday("2022331")
        assert Validator.is_valid_birthday("2024年4月24日")
        assert not Validator.is_valid_birthday("2022131")
        assert not Validator.is_valid_birthday("20221233")
        assert not Validator.is_valid_birthday("2022229")
        assert not Validator.is_valid_birthday("19000229")
        assert not Validator.is_valid_birthday("011")
        assert not Validator.is_valid_birthday("20220431")

    @classmethod
    def test_is_json_str(cls):
        assert Validator.is_json('{"name": "Peter"}')
        assert Validator.is_json("[1, 2, 3]")
        assert not Validator.is_json("{nope}")
        assert not Validator.is_json("nope")
        assert not Validator.is_json("")
        assert not Validator.is_json(None)
