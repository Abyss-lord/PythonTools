#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   sys_util_test.py
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
from loguru import logger

from .context_test import (
    EnvUtil,
)


@allure.feature("系统工具类")
@allure.description("系统工具类测试")
@allure.tag("util")
class TestSysUtil:
    @allure.title("测试平台判断")
    def test_platform(self) -> None:
        with allure.step("步骤1:测试是否在windows平台"):
            logger.debug(EnvUtil.is_windows_platform())

        with allure.step("步骤2:测试是否在mac平台"):
            logger.debug(EnvUtil.is_mac_platform())

        with allure.step("步骤3:测试是否在linux平台"):
            logger.debug(EnvUtil.is_linux_platform())

    @allure.title("python版本判断")
    def test_python_version(self) -> None:
        with allure.step("步骤1:测试python版本是否为3.x"):
            assert EnvUtil.is_py3()

        with allure.step("步骤2:测试python版本是否为2.x"):
            assert not EnvUtil.is_py2()

    @allure.title("测试获取已经系统变量")
    def test_get_system_var(self) -> None:
        with allure.step("步骤1:测试获取所有的环境变量"):
            for k, v in EnvUtil.get_system_properties().items():
                logger.debug(f"k={k}, v={v}")
        with allure.step("步骤2:测试获取HOME环境变量"):
            assert EnvUtil.get_system_property("HOME")
            assert EnvUtil.get_system_property("USER")
