#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_security.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import allure
import pytest
from loguru import logger

from .context_test import GrayCode


@allure.feature("格雷码生成器")
@allure.description("格雷码生成器，用于生成格雷码")
class TestGrayCode:
    @allure.title("测试生成格雷码")
    def test_generate_gray_code(cls) -> None:
        with allure.step("步骤1:测试生成0位格雷码"):
            test_code_width_1 = 0
            generator = GrayCode.gray_code_generator(test_code_width_1)

            for i in generator:
                logger.debug(i)
        with allure.step("步骤2:测试生成1位格雷码"):
            test_code_width_2 = 1
            generator = GrayCode.gray_code_generator(test_code_width_2)

            for i in generator:
                logger.debug(i)

        with allure.step("步骤3:测试生成2位格雷码"):
            test_code_width_3 = 2
            generator = GrayCode.gray_code_generator(test_code_width_3)

            for i in generator:
                logger.debug(i)
        with allure.step("步骤4:测试生成3位格雷码"):
            test_code_width_3 = 3
            generator = GrayCode.gray_code_generator(test_code_width_3)

            for i in generator:
                logger.debug(i)

        with allure.step("步骤5:测试错误的格雷码宽度"):
            with pytest.raises(ValueError):
                for i in GrayCode.gray_code_generator(-1):
                    logger.debug(i)
