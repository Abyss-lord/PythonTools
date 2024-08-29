#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   idcard_util_test.py
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

from datetime import datetime

import allure  # type: ignore
import pytest
from faker import Faker
from loguru import logger

from .context_test import (
    IDCardUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("IDCard工具类")
@allure.description("IDCard工具类，用于判断ID是否有效、生成随机ID等")
@allure.tag("util")
class TestIdUtil:
    TEST_ROUND = 10000

    @allure.story("生成随机有效身份证号")
    @allure.description("生成随机有效的18位和15位身份证号")
    class TestGenerateRandomValidId:
        @allure.title("测试生成随机有效身份证号")
        def test_generate_random_id(self):
            with allure.step("步骤1:测试生成随机有效身份证号"):
                for _ in range(TestIdUtil.TEST_ROUND):
                    id_str = IDCardUtil.generate_random_valid_id()
                    assert IDCardUtil.is_valid_id(id_str)

            with allure.step("步骤2:测试生成18位随机有效身份证号"):
                for _ in range(TestIdUtil.TEST_ROUND):
                    id_str = IDCardUtil.generate_random_valid_id(code_length=18)
                    assert IDCardUtil.is_valid_id(id_str)

            with allure.step("步骤3:测试生成15位随机有效身份证号"):
                for _ in range(TestIdUtil.TEST_ROUND):
                    id_str = IDCardUtil.generate_random_valid_id(code_length=15)
                    assert IDCardUtil.is_valid_id_15(id_str)

            with allure.step("步骤4:测试生成身份证号长度不正确"):
                with pytest.raises(ValueError):
                    IDCardUtil.generate_random_valid_id(code_length=21321)

        @allure.title("测试生成身份证Card对象")
        def test_generate_random_id_card_obj(cls):
            id_obj = IDCardUtil.generate_random_valid_card()
            logger.debug(id_obj)

    @allure.story("判断身份证号是否有效")
    @allure.description("判断身份证号是否有效")
    class TestCheckValidId:
        @allure.title("测试15位判断身份证号是否有效")
        def test_is_valid_id_15(cls) -> None:
            for _ in range(TestIdUtil.TEST_ROUND):
                id_str_15 = IDCardUtil.generate_random_valid_id(code_length=15)
                assert IDCardUtil.is_valid_id_15(id_str_15)

        @allure.title("测试18位判断身份证号是否有效")
        def test_is_valid_id_18(cls) -> None:
            with allure.step("步骤1:测试18位判断身份证号是否有效"):
                for _ in range(TestIdUtil.TEST_ROUND):
                    id_str_18 = IDCardUtil.generate_random_valid_id(code_length=18)
                    assert IDCardUtil.is_valid_id(id_str_18)

            with allure.step("步骤2:手动输入18位ID"):
                assert IDCardUtil.is_valid_id_18("420902200505081317")
                assert not IDCardUtil.is_valid_id_18("1101051998042465")
                assert not IDCardUtil.is_valid_id_18("a10105199804246510")
                assert not IDCardUtil.is_valid_id_18("110105199813246510")

    @allure.story("身份证号转换")
    @allure.description("身份证号转换，支持18位和15位身份证号之间的相互转换")
    class TestIdConvert:
        @allure.title("测试18位身份证号转换为15位")
        def test_convert_id_18_to_15(cls) -> None:
            with allure.step("步骤1:测试18位身份证号转换为15位, 正确输入"):
                assert IDCardUtil.is_valid_id_15(IDCardUtil.convert_18_to_15("42010019110218601X"))
                assert not IDCardUtil.is_valid_id("623021000229381")

            with allure.step("步骤2:测试18位身份证号转换为15位, 错误输入"):
                with pytest.raises(ValueError):
                    IDCardUtil.convert_18_to_15("522201200810135714")

        @allure.title("测试15位身份证号转换为18位")
        def test_convert_id_15_to_18(cls) -> None:
            for _ in range(TestIdUtil.TEST_ROUND):
                id_str_15 = IDCardUtil.generate_random_valid_id(code_length=15)
                id_str_18 = IDCardUtil.convert_15_to_18(id_str_15)
                assert IDCardUtil.is_valid_id(id_str_18)

    @allure.story("获取身份证号生日相关信息")
    class TestGetBirthday:
        @allure.title("测试获取身份证号生日 datetime 对象")
        def test_get_birthday(cls) -> None:
            with allure.step("步骤1:测试获取身份证号生日 datetime 对象, 15位身份证号"):
                dt = IDCardUtil.get_birthday_from_id_15("630121370928661")
                assert dt == datetime(1937, 9, 28)
                dt = IDCardUtil.get_birthday_from_id_15("622700410218861")
                assert dt == datetime(1941, 2, 18)
                dt = IDCardUtil.get_birthday_from_id_15("513224510626811")
                assert dt == datetime(1951, 6, 26)
                dt = IDCardUtil.get_birthday_from_id_15("431023730316191")
                assert dt == datetime(1973, 3, 16)
                dt = IDCardUtil.get_birthday_from_id_15("640302580304711")
                assert dt == datetime(1958, 3, 4)

            with allure.step("步骤2:测试获取身份证号生日 datetime 对象, 18位身份证号"):
                dt = IDCardUtil.get_birthday_from_id_18("331023195203187114")
                assert dt == datetime(1952, 3, 18)
                dt = IDCardUtil.get_birthday_from_id_18("35010219600101001X")
                assert dt == datetime(1960, 1, 1)
                dt = IDCardUtil.get_birthday_from_id_18("36042519700101001X")
                assert dt == datetime(1970, 1, 1)
                dt = IDCardUtil.get_birthday_from_id_18("370902194311104514")
                assert dt == datetime(1943, 11, 10)
                dt = IDCardUtil.get_birthday_from_id_18("370124198503168611")
                assert dt == datetime(1985, 3, 16)

            with allure.step("步骤3:测试获取身份证号生日 datetime 对象"):
                dt = IDCardUtil.get_birthday_from_id("630121370928661")
                assert dt == datetime(1937, 9, 28)
                dt = IDCardUtil.get_birthday_from_id("622700410218861")
                assert dt == datetime(1941, 2, 18)
                dt = IDCardUtil.get_birthday_from_id("513224510626811")
                assert dt == datetime(1951, 6, 26)
                dt = IDCardUtil.get_birthday_from_id("431023730316191")
                assert dt == datetime(1973, 3, 16)
                dt = IDCardUtil.get_birthday_from_id("640302580304711")
                assert dt == datetime(1958, 3, 4)

                dt = IDCardUtil.get_birthday_from_id("331023195203187114")
                assert dt == datetime(1952, 3, 18)
                dt = IDCardUtil.get_birthday_from_id("330382195801305112")
                assert dt == datetime(1958, 1, 30)
                dt = IDCardUtil.get_birthday_from_id("36042519700101001X")
                assert dt == datetime(1970, 1, 1)
                dt = IDCardUtil.get_birthday_from_id("370902194311104514")
                assert dt == datetime(1943, 11, 10)
                dt = IDCardUtil.get_birthday_from_id("370124198503168611")
                assert dt == datetime(1985, 3, 16)

            with allure.step("步骤4:测试获取身份证号生日 datetime 对象, 错误输入"):
                assert IDCardUtil.get_birthday_from_id("") is None
                assert IDCardUtil.get_birthday_from_id(1) is None
                assert IDCardUtil.get_birthday_from_id("1") is None
                assert IDCardUtil.get_birthday_from_id("adac") is None
                assert IDCardUtil.get_birthday_from_id("110105199804246511") is None

        @allure.title("测试获取身份证号年份信息")
        def test_get_year_from_id(self) -> None:
            assert IDCardUtil.get_year_from_id("630121370928661") == 1937
            assert IDCardUtil.get_year_from_id("622700410218861") == 1941
            assert IDCardUtil.get_year_from_id("513224510626811") == 1951
            assert IDCardUtil.get_year_from_id("431023730316191") == 1973
            assert IDCardUtil.get_year_from_id("331023195203187114") == 1952
            assert IDCardUtil.get_year_from_id("330382195801305112") == 1958

        @allure.title("测试获取身份证号月份信息")
        def test_get_month_from_id_18(self) -> None:
            assert IDCardUtil.get_month_from_id("331023195203187114") == 3
            assert IDCardUtil.get_month_from_id("622700410218861") == 2
            assert IDCardUtil.get_month_from_id("513224510626811") == 6
            assert IDCardUtil.get_month_from_id("431023730316191") == 3
            assert IDCardUtil.get_month_from_id("331023195203187114") == 3
            assert IDCardUtil.get_month_from_id("330382195801305112") == 1

        @allure.title("测试获取身份证号日信息")
        def test_get_day_from_id_18(self) -> None:
            assert IDCardUtil.get_day_from_id("331023195203187114") == 18
            assert IDCardUtil.get_day_from_id("622700410218861") == 18
            assert IDCardUtil.get_day_from_id("513224510626811") == 26
            assert IDCardUtil.get_day_from_id("431023730316191") == 16
