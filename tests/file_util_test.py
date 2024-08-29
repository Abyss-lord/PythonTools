#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   file_util_test.py
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
from faker import Faker
from loguru import logger

from .context_test import (
    FileUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("文件工具类")
@allure.description("文件工具类测试")
@allure.tag("util")
class TestFileUtil:
    BASIC_TEST_ROUND = 10000

    @allure.title("测试文件、文件夹是否存在")
    def test_exist(self) -> None:
        with allure.step("步骤1:测试文件是否存在"):
            assert FileUtil.is_exist(__file__)
            assert not FileUtil.is_exist("dsadadadad")

    # @allure.title("测试随机文件名称")
    # def test_random_file_name(self) -> None:
    #     with allure.step("步骤1:测试随机文件名称"):
    #         for _ in range(TestFileUtil.BASIC_TEST_ROUND):
    #             new_file_name = FileUtil.generate_random_file_name("test.sql")
    #             logger.debug(new_file_name)

    @allure.title("测试获取最后修改时间")
    def test_get_last_modify_time(cls) -> None:
        with allure.step("步骤1:测试获取文件最后修改时间(字符串)"):
            format_str = FileUtil.get_last_modify_time_in_string_format(__file__)

        with allure.step("步骤2:测试获取文件最后修改时间(时间格式)"):
            seconds = FileUtil.get_last_modify_time_in_seconds(__file__)
            milliseconds = FileUtil.get_last_modify_time_in_milliseconds(__file__)
            nanoseconds = FileUtil.get_last_modify_time_in_nanoseconds(__file__)

        logger.debug(seconds)
        logger.debug(milliseconds)
        logger.debug(nanoseconds)
        logger.debug(format_str)


# class TestSysUtil:
#     @classmethod
#     def test_list_file(cls):
#         from pathlib import Path

#         p = Path(__file__).parent.parent
#         res = OsUtil.list_files(p, check_exist=False)
#         logger.debug(res)

#         res = OsUtil.list_files(p, check_exist=True)
#         logger.debug(res)


# class TestOsUtil:
#     @classmethod
#     def test_is_contain_hidden_dir(cls):
#         assert OsUtil.is_contain_ignore("/.git")
#         assert OsUtil.is_contain_ignore(".git")
#         assert OsUtil.is_contain_ignore(".svn/sad/")
#         assert OsUtil.is_contain_ignore("/tmp/__pychache__")
#         assert OsUtil.is_contain_ignore("/tmp/__pychache__/pancx")
#         assert OsUtil.is_contain_ignore("__pycache__")
#         assert not OsUtil.is_contain_ignore("/hidden")
#         assert not OsUtil.is_contain_ignore("hidden")
#         assert not OsUtil.is_contain_ignore("usr/local/")
#         assert not OsUtil.is_contain_ignore("/ust/local/security/")

#     @classmethod
#     def test_is_exist(cls):
#         assert OsUtil.is_exist("")
#         assert OsUtil.is_exist("/")
#         assert OsUtil.is_exist("/tmp")
#         assert OsUtil.is_exist("/Users/")
#         assert not OsUtil.is_exist("dsaddaasawdasdwa")

#     @classmethod
#     def test_is_dir(cls):
#         assert OsUtil.is_dir("")
#         assert OsUtil.is_dir("/")
#         assert OsUtil.is_dir("/tmp")
#         assert OsUtil.is_dir("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")

#         assert not OsUtil.is_dir(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own"
#             "/PythonTools/pythontools/component/basic_utils.py",
#             raise_exception=False,
#         )
#         with pytest.raises(Exception):
#             OsUtil.is_dir("dsaddaasawdasdwa", raise_exception=True)

#     @classmethod
#     def test_is_file(cls):
#         assert not OsUtil.is_file("")
#         assert not OsUtil.is_file("/tmp")
#         assert not OsUtil.is_file(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/core/basicutils.py",
#             raise_exception=False,
#         )

#         with pytest.raises(ValueError):
#             OsUtil.is_file("dsaddaasawdasdwa", raise_exception=True)

#     @classmethod
#     def test_get_file_create_time(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
#         OsUtil.get_create_time_in_string_format(p)
#         with pytest.raises(ValueError):
#             OsUtil.get_create_time_in_string_format(p + "dadada", check_exist=True)

#     @classmethod
#     def test_list_dirs(cls):
#         res = OsUtil.list_dirs("/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools")
#         logger.debug(res)

#         OsUtil.list_dirs(
#             "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools",
#             check_exist=True,
#         )

#     @classmethod
#     def test_get_extension_from_path(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools/component/constant.py"  # noqa: E501
#         extension = OsUtil.get_extension_from_path(p)
#         assert ".py" == extension

#     @classmethod
#     def test_is_match_extension(cls):
#         with pytest.raises(ValueError):
#             OsUtil.is_match_extension(".tm", "")

#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/tests/context.py"
#         assert OsUtil.is_match_extension(p, "py")
#         assert OsUtil.is_match_extension(p, ".py")

#     @classmethod
#     def test_get_file_from_dir_by_extension(cls):
#         p = "/Users/panchenxi/Work/project/work/长期项目和学习/python/own/PythonTools/pythontools" "/component/"
#         res = OsUtil.get_file_from_dir_by_extension(p, extension="py")
#         logger.debug(res)

#     @classmethod
#
