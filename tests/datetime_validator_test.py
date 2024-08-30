#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   datetime_validator_test.py
@Date       :   2024/08/27
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/27
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import allure
from faker import Faker

from .context_test import (
    DatetimeValidator,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("日期时间验证器测试")
@allure.description("日期、时间验证器")
@allure.tag("validator", "datetime")
class TestValidator:
    @allure.title("验证给定的生日是否有效")
    def test_is_valid_birthday(self) -> None:
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
