#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   desensitized_util_test.py
@Date       :   2024/08/28
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/28
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib

import allure  # type: ignore
import pytest
from faker import Faker

from .context_test import (
    DesensitizedUtil,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("脱敏工具类")
@allure.description("用于对敏感数据脱敏，例如手机号、邮箱、身份证号、银行卡号、IP地址等")
@allure.tag("util", "desensitized")
class TestDesensitizedUtil:
    @allure.title("对IP进行脱敏")
    def test_desensitize_ipv4(self) -> None:
        with allure.step("测试IPv4地址脱敏"):
            ipv4 = "192.0.2.1"
            assert DesensitizedUtil.desensitize_ipv4(ipv4) == "192.*.*.*"
            assert DesensitizedUtil.desensitize_ipv4(ipv4.encode("utf-8")) == "192.*.*.*"

        with allure.step("测试对IPV6地址进行脱敏"):
            ipv6 = "2001:0db8:86a3:08d3:1319:8a2e:0370:7344"
            assert DesensitizedUtil.desensitize_ipv6(ipv6) == "2001:*:*:*:*:*:*:*"
            assert DesensitizedUtil.desensitize_ipv6(ipv6.encode("utf-8")) == "2001:*:*:*:*:*:*:*"

    @allure.title("测试对邮箱号码进行脱敏")
    def test_desensitize_email(self) -> None:
        email1 = "duandazhi-jack@gmail.com.cn"
        assert DesensitizedUtil.desensitize_email(email1) == "d*************@gmail.com.cn"

        email2 = "duandazhi@126.com"
        assert "d********@126.com" == DesensitizedUtil.desensitize_email(email2)

        email3 = "duandazhi@gmail.com.cn"
        assert "d********@gmail.com.cn" == DesensitizedUtil.desensitize_email(email3)
        assert "d********@gmail.com.cn" == DesensitizedUtil.desensitize_email(email3.encode("utf-8"))
        assert "" == DesensitizedUtil.desensitize_email("")

    @allure.title("测试对ID进行脱敏")
    def test_desensitize_id_card(self) -> None:
        id_card = "51343620000320711X"
        assert DesensitizedUtil.desensitize_id_card(id_card) == "513436********711X"
        assert DesensitizedUtil.desensitize_id_card(id_card.encode("utf-8")) == "513436********711X"

    @allure.title("测试对银行卡号进行脱敏")
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
        assert DesensitizedUtil.desensitize_bank_card(bank_card3.encode("utf-8")) == "1234 **** **** **** 6789"
        assert DesensitizedUtil.desensitize_bank_card("") == ""

    @allure.title("测试对手机号进行脱敏")
    def test_desensitize_mobile_phone(self) -> None:
        phone = "18049531999"
        assert "180****1999" == DesensitizedUtil.desensitize_mobile_phone(phone)
        assert "180****1999" == DesensitizedUtil.desensitize_mobile_phone(phone.encode("utf-8"))

    @allure.title("测试对固定电话进行脱敏")
    def test_desensitize_fix_phone(self) -> None:
        fix_phone1 = "09157518479"
        assert "091****8479" == DesensitizedUtil.desensitize_fix_phone(fix_phone1)
        assert "091****8479" == DesensitizedUtil.desensitize_fix_phone(fix_phone1.encode("utf-8"))

    @allure.title("测试对车牌号进行脱敏")
    def test_desensitize_car_license(self) -> None:
        car_license1 = "苏D40000"
        assert "苏D4***0" == DesensitizedUtil.desensitize_car_license(car_license1)

        car_license2 = "陕A12345D"
        assert "陕A1****D" == DesensitizedUtil.desensitize_car_license(car_license2)

        car_license3 = "京A123"
        with pytest.raises(ValueError) as _:
            assert "京A123" == DesensitizedUtil.desensitize_car_license(car_license3)

        assert "陕A1****D" == DesensitizedUtil.desensitize_car_license(car_license2.encode("utf-8"))
        assert "" == DesensitizedUtil.desensitize_car_license("")

    @allure.title("测试对地址进行脱敏")
    def test_desensitize_address(self) -> None:
        address = "北京市海淀区马连洼街道289号"
        assert "北京市海淀区马连洼街*****" == DesensitizedUtil.desensitize_address(address, 5)
        assert "***************" == DesensitizedUtil.desensitize_address(address, 50)
        assert "北京市海淀区马连洼街道289号" == DesensitizedUtil.desensitize_address(address, 0)
        assert "北京市海淀区马连洼街道289号" == DesensitizedUtil.desensitize_address(address, -1)
        # butes
        assert "北京市海淀区马连洼街道289号" == DesensitizedUtil.desensitize_address(address.encode("utf-8"), -1)

    @allure.title("测试对密码进行脱敏")
    def test_password(self) -> None:
        password = "password"
        assert "********" == DesensitizedUtil.desensitize_password(password)
        assert "********" == DesensitizedUtil.desensitize_password(password.encode("utf-8"))

    @allure.title("测试对中文姓名进行脱敏")
    def test_desensitize_chineseName(self) -> None:
        assert "段**" == DesensitizedUtil.desensitize_chinese_name("段正淳")
        assert "张*" == DesensitizedUtil.desensitize_chinese_name("张三")

    @allure.title("测试只保留最后一个字符")
    def test_retain_last(cls) -> None:
        s = "asdasc"
        assert "*****c" == DesensitizedUtil.retain_last(s)

    @allure.title("测试保留第一个字符")
    def test_retain_first(cls) -> None:
        s = "asdasc"
        assert "a*****" == DesensitizedUtil.retain_first(s)

    @allure.title("测试保留前后字符")
    def test_retain_front_and_end(cls) -> None:
        assert "" == DesensitizedUtil.retain_front_and_end("", 3, 4)
        assert "" == DesensitizedUtil.retain_front_and_end("  ", 3, 4)
        with pytest.raises(ValueError):
            assert "" == DesensitizedUtil.retain_front_and_end("sad", 3, 4)

        with pytest.raises(ValueError):
            assert "" == DesensitizedUtil.retain_front_and_end("sad", 3, -1)
