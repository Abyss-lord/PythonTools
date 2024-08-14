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
import pytest
from loguru import logger

from .context import GrayCode


class TestGrayCode:
    @classmethod
    def test_generate_gray_code(cls) -> None:
        test_code_width_1 = 0

        generator = GrayCode.gray_code_generator(test_code_width_1)

        for i in generator:
            logger.debug(i)

        test_code_width_2 = 1

        generator = GrayCode.gray_code_generator(test_code_width_2)

        for i in generator:
            logger.debug(i)

        test_code_width_3 = 3

        generator = GrayCode.gray_code_generator(test_code_width_3)

        for i in generator:
            logger.debug(i)

        with pytest.raises(ValueError):
            for i in GrayCode.gray_code_generator(-1):
                logger.debug(i)
