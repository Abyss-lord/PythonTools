#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   string_validator_test.py
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

import allure  # type: ignore
from faker import Faker

from .context_test import (
    RandomUtil,
    StringUtil,
    StringValidator,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.feature("字符串正则匹配")
@allure.description("字符串正则匹配测试")
@allure.tag("util")
class TestStringValidator:
    BASIC_TEST_ROUND = 1000

    @allure.title("测试是否为Json字符串")
    def test_is_json_str(cls):
        with allure.step("步骤1:测试Json字符串"):
            assert StringValidator.is_json("{}")
            assert StringValidator.is_json("[]")
            assert StringValidator.is_json('{"name": "Peter"}')
            assert StringValidator.is_json("[1, 2, 3]")
            assert StringValidator.is_json('{"name": "Peter", "age": 30}')
            assert StringValidator.is_json(
                '{"name": "Peter", "relations": {"name":"Jack", "age": 25}, \
                    "age": 30, "hobbies": ["reading", "swimming"]}'
            )

        with allure.step("步骤2:测试非Json字符串"):
            assert not StringValidator.is_json("{nope}")
            assert not StringValidator.is_json("nope")
            assert not StringValidator.is_json("")
            assert not StringValidator.is_json(None)

    @allure.title("测试是字符串相关")
    def test_string(self):
        with allure.step("步骤1:测试是否为给定长度字符串"):
            static_str = "1234567890"
            assert StringValidator.is_general_string_with_length(static_str, 1, 20)
            assert not StringValidator.is_general_string_with_length(static_str, 1, 2)

        with allure.step("步骤2:测试随机长度字符串"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                random_length = RandomUtil.get_random_val_from_range(1, 20)
                random_str = StringUtil.get_random_strs(random_length)
                random_test_length = RandomUtil.get_random_val_from_range(1, 20)
                if random_test_length >= random_length:
                    assert StringValidator.is_general_string_with_length(random_str, 1, random_test_length)
                else:
                    assert not StringValidator.is_general_string_with_length(random_str, 1, random_test_length)

        with allure.step("步骤3:测试边界参数"):
            static_str = "1234567890"
            assert StringValidator.is_general_string_with_length(static_str, 1, -1)
            assert StringValidator.is_general_string_with_length(static_str, -1, -10)

    @allure.title("测试是否是钱币")
    def test_is_money(cls) -> None:
        with allure.step("步骤1:测试正确的钱币"):
            # PERF 搞清楚这个正则表达式
            assert StringValidator.is_money("456.789")

    @allure.title("测试是否为邮编")
    def test_is_zip_code(cls) -> None:
        with allure.step("步骤1:测试正确的邮编"):
            for test_obj in ["210018", "210001", "210009", "210046"]:
                assert StringValidator.is_zip_code(test_obj)

    @allure.title("测试是否为手机号")
    def test_is_mobile(self) -> None:
        with allure.step("步骤1:测试正确的手机号"):
            correct_phones = ["13912345678", "15012345678", "18612345678", "17161193307"]
            for phone in correct_phones:
                assert StringValidator.is_mobile(phone)

        with allure.step("步骤2:测试错误的手机号"):
            incorrect_phones = ["1716119330"]
            for phone in incorrect_phones:
                assert not StringValidator.is_mobile(phone)

        with allure.step("步骤3:测试随机生成的手机号"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                phone = BASIC_CHINESE_FAKE.phone_number()
                assert StringValidator.is_mobile(phone)

    @allure.title("测试是否为邮箱")
    def test_is_email(self) -> None:
        with allure.step("步骤1:测试正确的邮箱"):
            correct_emails = [
                "user@example.com",
                "firstname.lastname@example.com",
                "user+mailbox@example.com",
                "user.name+tag+sorting@example.com",
                "user@example.co.uk",
                "user_name@example.com",
                "user-name@example.com",
                "user.name@subdomain.example.com",
                "user_name+123@example.com",
                "user@domain.com.",
                "user@123.123.123.123",
                "user@domain-with-dash.com",
                "user@domain-with-dash.com",
                "user@123.123.123.123",
            ]

            for correct_email in correct_emails:
                assert StringValidator.is_email(correct_email)

        with allure.step("步骤2:测试错误的邮箱"):
            incorrect_emails = [
                "plainaddress",
                "@missingusername.com",
                "user@.com.my",
                "user@domain..com",
                "user@-domain.com",
            ]

            for incorrect_email in incorrect_emails:
                assert not StringValidator.is_email(incorrect_email)

        with allure.step("步骤3:测试随机生成的邮箱"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                mail = BASIC_FAKE.email()
                assert StringValidator.is_email(mail)

    @allure.title("测试是否为16进制字符串")
    def test_is_hex(self) -> None:
        with allure.step("步骤1:测试正确的16进制字符串"):
            correct_hex = [
                "1A2B3C",  # 常见的十六进制字符串
                "abcdef",  # 小写字母
                "ABCDEF",  # 大写字母
                "123",  # 单一的有效十六进制数字
                "0x123ABC",
                "ff",  # 最小有效的两位十六进制数字
                "7F",  # 一字节的十六进制数值
                "000001",  # 具有前导零的有效十六进制字符串
                "DEADBEEF",  # 经典的十六进制字符串
            ]

            for correct_str in correct_hex:
                assert StringValidator.is_hex(correct_str)

        with allure.step("步骤2:测试错误的16进制字符串"):
            incorrect_hex = [
                "G123",  # 非十六进制字符
                "123Z",  # 非十六进制字符
                "0xGHIJKL",  # 前缀但包含非十六进制字符
                "123ABC!"  # 包含非十六进制字符
                "1.2.3",  # 包含点号的无效格式
                "123 456",  # 包含空格的无效格式
                "",  # 空字符串
                "0x123 456",  # 带有空格的前缀十六进制字符串
            ]

            for incorrect_str in incorrect_hex:
                assert not StringValidator.is_hex(incorrect_str)

    @allure.title("测试中国汽车车牌")
    def test_is_chinese_vehicle_number(self) -> None:
        with allure.step("步骤1:测试正确的车牌号"):
            correct_vins = [
                "京A12345",  # 北京市的车牌号
                "沪B23456",  # 上海市的车牌号
                "粤C34567",  # 广东省的车牌号
                "苏D45678",  # 江苏省的车牌号
                "浙E56789",  # 浙江省的车牌号
                "川H12345",  # 四川省的车牌号
                "桂K12345",  # 广西省的车牌号
            ]

            for correct_vin_str in correct_vins:
                assert StringValidator.is_chinese_vehicle_number(correct_vin_str)

        with allure.step("步骤2:测试错误的车牌号"):
            incorrect_vins = [
                "AB12345",  # 无效的车牌号格式（省份代码错误）
                "京123456",  # 车牌号长度超出有效范围
                "粤C3456",  # 车牌号长度不足
                "苏1234",  # 缺少省份代码
                "浙E5678AB",  # 包含无效字符
                "鲁F123456",  # 车牌号长度超出有效范围
                "晋5678",  # 缺少省份代码
                "川H123456",  # 车牌号长度超出有效范围
                "鄂J123",  # 车牌号长度不足
                "桂K1234567",  # 车牌号长度超出有效范围
            ]

            for incorrect_vin_str in incorrect_vins:
                assert not StringValidator.is_chinese_vehicle_number(incorrect_vin_str)

    @allure.title("测试是否是ipv4地址")
    def test_is_ip(self) -> None:
        with allure.step("步骤1:测试随机生成的ipv4地址"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                ipv4 = BASIC_FAKE.ipv4_private()
                assert StringValidator.is_ipv4(ipv4)

        with allure.step("步骤2:测试随机生成的ipv6地址"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                ipv6 = BASIC_FAKE.ipv6()
                assert StringValidator.is_ipv6(ipv6)

    @allure.title("测试是否为中文")
    def test_is_chinese(self) -> None:
        with allure.step("步骤1:测试随机的中文单词"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                cn_word = BASIC_CHINESE_FAKE.word()
                assert StringValidator.is_chinese(cn_word)
                us_word = BASIC_US_FAKE.word()
                assert not StringValidator.is_chinese(us_word)

        with allure.step("步骤2:测试随机的中文句子"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                cn_sentence = BASIC_CHINESE_FAKE.sentence()
                assert StringValidator.is_chinese(cn_sentence)
                us_sentence = BASIC_US_FAKE.sentence()
                assert not StringValidator.is_chinese(us_sentence)

        with allure.step("步骤3:测试随机的中文段落"):
            for _ in range(TestStringValidator.BASIC_TEST_ROUND):
                cn_paragraph = BASIC_CHINESE_FAKE.paragraph()
                assert StringValidator.is_chinese(cn_paragraph)
                us_paragraph = BASIC_US_FAKE.paragraph()
                assert not StringValidator.is_chinese(us_paragraph)

    @allure.title("测试是否包含英文字母")
    def test_has_no_letter(self) -> None:
        # TODO 修正示例
        pass
        # assert StringValidator.has_no_letter("1233231412")
        # assert not StringValidator.has_no_letter("Hello, World!")
        # assert StringValidator.has_no_letter("你好，世界！")

    @allure.title("测试是否是中文省份名称")
    def test_is_chinese_province_name(self) -> None:
        assert StringValidator.is_chinese_province_name("浙江")
        assert StringValidator.is_chinese_province_name("北京")
        assert not StringValidator.is_chinese_province_name("Beijing")
        assert StringValidator.is_chinese_province_name("上海")

    @allure.title("测试是否是微信号")
    def test_is_wechat_name(self) -> None:
        assert StringValidator.is_wechat_account("wxid_1234")
        assert StringValidator.is_wechat_account("abc123456")
        assert StringValidator.is_wechat_account("a_bc-def")
        assert not StringValidator.is_wechat_account("user@name")
        assert not StringValidator.is_wechat_account("ab")
        assert not StringValidator.is_wechat_account("thisisaveryl2213213123ongweixinidtoolong")

    @allure.title("测试是否是24小时制时间")
    def test_is_24_hour_time(self) -> None:
        assert StringValidator.is_time_in_24_hour_format("01:02:00")
        assert StringValidator.is_time_in_24_hour_format("12:00")
        assert StringValidator.is_time_in_24_hour_format("23:59:59")
        assert not StringValidator.is_time_in_24_hour_format("24:00")
        assert not StringValidator.is_time_in_24_hour_format("24:00:00")

    @allure.title("测试是否是12小时制时间")
    def test_is_12_hour_time(self) -> None:
        assert StringValidator.is_time_in_12_hour_format("01:02:00 AM")
        assert StringValidator.is_time_in_12_hour_format("12:00 PM")
        assert StringValidator.is_time_in_12_hour_format("11:59:59 PM")
        assert not StringValidator.is_time_in_12_hour_format("23:00 AM")
        assert not StringValidator.is_time_in_12_hour_format("13:00 AM")
        assert not StringValidator.is_time_in_12_hour_format("23:00:00")

    @allure.title("测试是否是车次号")
    def test_is_train_number(self) -> None:
        assert StringValidator.is_train_number("G35")
        assert StringValidator.is_train_number("G143")
        assert StringValidator.is_train_number("T09")
        assert StringValidator.is_train_number("D5")
        assert not StringValidator.is_train_number("G123422")
        assert not StringValidator.is_train_number("K789012")

    @allure.title("测试数值匹配")
    def test_number_match(self) -> None:
        with allure.step("步骤1:测试数值匹配"):
            assert StringValidator.is_number("123")
            assert StringValidator.is_number("123.456")

        with allure.step("步骤2:测试非负整数匹配"):
            assert StringValidator.is_non_negative_integer("123")
            assert not StringValidator.is_non_negative_integer("-123")

        with allure.step("步骤3:测试非正整数匹配"):
            assert StringValidator.is_non_positive_integer("-123")
            assert not StringValidator.is_non_positive_integer("123")

        with allure.step("步骤4:测试非负浮点数匹配"):
            assert StringValidator.is_non_negative_float("123.456")
            assert StringValidator.is_non_negative_float("0.000")

        with allure.step("步骤5:测试非正浮点数匹配"):
            assert StringValidator.is_non_positive_float("-123.456")
            assert StringValidator.is_non_positive_float("0.000")

    @allure.title("测试是否是密码")
    def test_is_password(self) -> None:
        assert StringValidator.is_password("Abcdef1@")
        assert StringValidator.is_password("StrongPass1!")
        assert StringValidator.is_password("P@ssw0rd")
        assert not StringValidator.is_password("password")
        assert not StringValidator.is_password("123456")
        assert not StringValidator.is_password("abcdefg1@")

    @allure.title("测试是否是腾讯QQ号")
    def test_is_tencent_code(self) -> None:
        assert StringValidator.is_tencent_code("123456789")
        assert StringValidator.is_tencent_code("851979198")
        assert not StringValidator.is_tencent_code("0123")
