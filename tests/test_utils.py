#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     test_utils
   Description :
   date：          2024/7/16
-------------------------------------------------
   Change Activity:
                   2024/7/16:
-------------------------------------------------
"""
from datetime import datetime, timedelta

from loguru import logger
import pytest
from .context import StringUtil, BooleanUtil, SequenceUtil, Validator, IDCardUtil, DateUtil, \
    FileUtil


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
        now = (datetime.now() + timedelta(days=1))
        res = now - datetime.now()
        logger.debug(type(res))


class TestDateUtil:
    TEST_ROUND = 10

    @classmethod
    def test_get_random_date_with_no_args(cls):
        for _ in range(cls.TEST_ROUND):
            logger.debug(DateUtil.get_random_date())

    @classmethod
    def test_get_random_date_with_one_args(cls):
        start = datetime(1998, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DateUtil.get_random_date(start))

    @classmethod
    def test_get_random_date_with_two_args(cls):
        start = datetime(1998, 4, 24)
        end = datetime(2021, 4, 24)
        for _ in range(cls.TEST_ROUND):
            logger.debug(DateUtil.get_random_date(start, end))

    @classmethod
    def test_get_random_date_with_wrong_args(cls):
        with pytest.raises(ValueError):
            end = datetime(1998, 4, 24)
            start = datetime(2021, 4, 24)
            logger.debug(DateUtil.get_random_date(start, end))

        with pytest.raises(ValueError):
            start = datetime(1998, 4, 24)
            end = datetime(1998, 4, 24)
            logger.debug(DateUtil.get_random_date(start, end))

    @classmethod
    def test_get_this_year(cls):
        for _ in range(cls.TEST_ROUND):
            assert DateUtil.this_year() == 2024
            assert not DateUtil.this_year() == 2025

    @classmethod
    def test_get_this_month(cls):
        for _ in range(cls.TEST_ROUND):
            assert DateUtil.this_month() == 7
            assert not DateUtil.this_month() == 9

    @classmethod
    def test_is_leap_year(cls):
        assert DateUtil.is_leap_year(2024)
        assert not DateUtil.is_leap_year(2025)
        assert not DateUtil.is_leap_year(1900)
        assert not DateUtil.is_leap_year(2100)


class TestIdUtil:
    TEST_ROUND = 10

    @classmethod
    def test_generate_random_id(cls):
        for _ in range(cls.TEST_ROUND):
            id_str = IDCardUtil.generate_random_valid_id()
            logger.debug(id_str)
            assert IDCardUtil.is_valid_id(id_str)

    @classmethod
    def test_generate_random_idcard(cls):
        for _ in range(cls.TEST_ROUND):
            id_obj = IDCardUtil.generate_random_valid_card()
            logger.debug(id_obj)


class TestFileUtil:
    @classmethod
    def test_list_file(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools"
        res = FileUtil.list_files(p, check_exist=False)
        logger.debug(res)

        res = FileUtil.list_files(p, check_exist=True)
        logger.debug(res)

    @classmethod
    def test_is_windows(cls):
        assert not FileUtil.is_windows()

    @classmethod
    def test_is_unix(cls):
        assert FileUtil.is_unix_like()

    @classmethod
    def test_is_contain_hidden_dir(cls):
        assert FileUtil.is_contain_hidden_dir("/.git")
        assert FileUtil.is_contain_hidden_dir(".git")
        assert FileUtil.is_contain_hidden_dir(".svn/sad/")
        assert FileUtil.is_contain_hidden_dir("/tmp/__pychache__")
        assert FileUtil.is_contain_hidden_dir("/tmp/__pychache__/pancx")
        assert FileUtil.is_contain_hidden_dir("__pycache__")
        assert not FileUtil.is_contain_hidden_dir("/hidden")
        assert not FileUtil.is_contain_hidden_dir("hidden")
        assert not FileUtil.is_contain_hidden_dir("usr/local/")
        assert not FileUtil.is_contain_hidden_dir("/ust/local/security/")

    @classmethod
    def test_is_exist(cls):
        assert not FileUtil.is_exist("")
        assert not FileUtil.is_exist("")
        assert FileUtil.is_exist("/")
        assert FileUtil.is_exist("/tmp")
        assert FileUtil.is_exist(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")
        assert FileUtil.is_exist("/Users/")
        assert not FileUtil.is_exist("dsaddaasawdasdwa")

    @classmethod
    def test_is_dir(cls):
        assert not FileUtil.is_dir("")
        assert FileUtil.is_dir("/")
        assert FileUtil.is_dir("/tmp")
        assert FileUtil.is_dir(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")

        assert not FileUtil.is_dir("/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
                                   "/PythonTools/pythontools/component/basic_utils.py",
                                   raise_exception=False)
        with pytest.raises(Exception):
            FileUtil.is_dir("dsaddaasawdasdwa", raise_exception=True)

    @classmethod
    def test_is_file(cls):
        assert not FileUtil.is_file("")
        assert not FileUtil.is_file("/tmp")
        assert FileUtil.is_file("/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
                                "/PythonTools/pythontools/component/basic_utils.py",
                                raise_exception=False)

        with pytest.raises(ValueError):
            FileUtil.is_file("dsaddaasawdasdwa", raise_exception=True)

    @classmethod
    def test_get_file_create_time(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
        FileUtil.get_file_create_time(p)
        with pytest.raises(FileNotFoundError):
            FileUtil.get_file_create_time(p + "dadada", check_exist=True)

    @classmethod
    def test_list_dirs(cls):
        res = FileUtil.list_dirs(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")
        logger.debug(res)

        FileUtil.list_dirs(
            "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools",
            check_exist=True)

    @classmethod
    def test_get_extension_from_path(cls):
        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
        extension = FileUtil.get_extension_from_path(p)
        assert '.py' == extension

    @classmethod
    def test_is_match_extension(cls):
        with pytest.raises(ValueError):
            FileUtil.is_match_extension(".tm", '')

        p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"
        assert FileUtil.is_match_extension(p, 'py')
        assert FileUtil.is_match_extension(p, '.py')

    @classmethod
    def test_get_file_from_dir_by_extension(cls):
        p = ("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools"
             "/component/")
        res = FileUtil.get_file_from_dir_by_extension(p, extension="py")
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
