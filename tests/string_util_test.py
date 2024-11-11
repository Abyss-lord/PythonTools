#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   string_util_test.py
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
import random

import allure  # type: ignore
import pytest
from faker import Faker
from loguru import logger

from .context_test import (
    StringUtil,
    StringValidator,
)

BASIC_FAKE = Faker()
BASIC_CHINESE_FAKE = Faker("zh_CN")
BASIC_TW_FAKE = Faker("zh_TW")
BASIC_US_FAKE = Faker("en-US")


@allure.story("字符串工具类")
@allure.story("判断字符串的相关状态")
@allure.description("测试判断字符串的相关状态,例如是否为空等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestStringState:
    @allure.title("测试判断字符串是否相等")
    @pytest.mark.parametrize(
        "text1,text2,expected",
        [
            ("hello", "hello", True),
            ("hello", "HELLO", True),
            ("hello", "world", False),
            ("", None, False),
            (None, "", False),
            (None, None, False),
        ],
    )
    def test_equals_without_setting(
        self,
        text1,
        text2,
        expected,
    ):
        assert StringUtil.equals(text1, text2) == expected

    @allure.title("测试判断字符串是否相等,不忽略大小写")
    @pytest.mark.parametrize(
        "text1,text2,expected",
        [
            ("hello", "hello", True),
            ("hello", "HELLO", False),
            ("hello", "world", False),
            ("", None, False),
            (None, "", False),
            (None, None, False),
        ],
    )
    def test_equals_with_setting(
        self,
        text1,
        text2,
        expected,
    ):
        assert StringUtil.equals(text1, text2, case_insensitive=False) == expected

    @allure.title("判断字符串 s 等于任何一个给定的字符串 args 中的字符串")
    def test_equals_any(self):
        assert StringUtil.equals_any("hello", "hello world", "hello")
        assert not StringUtil.equals_any("hello", "hello world", "world")

    @allure.title("测试字符串不想等")
    def test_not_equals(self):
        assert StringUtil.not_equals("hello", "world")
        assert not StringUtil.not_equals("hello", "hello")

    @allure.title("测试字符串是否包含数字")
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("hello123world", True),
            ("helloworld", False),
        ],
    )
    def test_contains_digit(
        self,
        text,
        expected,
    ):
        assert StringUtil.contain_digit(text) == expected

    @allure.title("测试字符串是否为空")
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("", True),
            (" ", True),
            ("\t\n", True),
            ("hello", False),
            (None, True),
            ("1231", False),
            ("abc", False),
            ("你好", False),
        ],
    )
    def test_is_blank(
        self,
        text,
        expected,
    ):
        assert StringUtil.is_blank(text) == expected
        assert StringUtil.is_not_blank(text) != expected

    @allure.title("测试is_all_blank方法")
    @pytest.mark.parametrize(
        "args,expected",
        [
            (["", " ", "  ", "\t\n"], True),
            (["", "s", "b"], False),
            (["s", "b"], False),
            (["", "", ""], True),
            (["", "", "s", "b"], False),
            (["s", "b", ""], False),
            ([], True),
        ],
    )
    def test_is_all_blank(
        self,
        args,
        expected,
    ):
        assert StringUtil.is_all_blank(*args) == expected

    @allure.title("测试给定的多个字符串中是否包含空格")
    @pytest.mark.parametrize(
        "args,expected",
        [
            (["hello world", "hello python", "hello "], False),
            (["programming", "progress", "progr"], False),
            (["hello world", "world hello", ""], True),
            (["hello world", "world hello", ""], True),
            (["", " ", "  ", "\t\n"], True),
            (["", "s", "b"], True),
            (["s", "b"], False),
            (["", "", ""], True),
            (["", "", "s", "b"], True),
            (["s", "b", ""], True),
            ([], True),
        ],
    )
    def test_has_whitespace(
        self,
        args,
        expected,
    ) -> None:
        assert StringUtil.has_blank(*args) == expected

    @allure.title("测试字符串的开头是否为指定字符")
    @pytest.mark.parametrize(
        "base,prefix,expected",
        [
            ("hello world", "h", True),
            ("hello world", "he", True),
            ("hello world", "hello", True),
            ("hello world", "world", False),
            ("hello world", "l", False),
            ("", "", True),
        ],
    )
    def test_starts_with(
        self,
        base,
        prefix,
        expected,
    ) -> None:
        assert StringUtil.starts_with(base, prefix) == expected

    @allure.title("测试字符串的结尾是否为指定字符")
    @pytest.mark.parametrize(
        "base,suffix,expected",
        [
            ("hello world", "d", True),
            ("hello world", "ld", True),
            ("hello world", "world", True),
            ("hello world", "he", False),
            ("hello world", "o", False),
            ("", "", True),
        ],
    )
    def test_ends_with(
        self,
        base,
        suffix,
        expected,
    ) -> None:
        assert StringUtil.ends_with(base, suffix) == expected

    @allure.title("测试字符串是否包含指定字符")
    @pytest.mark.parametrize(
        "base,args,expected",
        [
            ("hello world", ["hello", "o"], True),
            ("hello world", ["l", "d"], False),
        ],
    )
    def test_starts_with_any(
        self,
        base,
        expected,
        args,
    ) -> None:
        assert StringUtil.starts_with_any(base, *args) == expected

    @allure.title("测试字符串结尾包含指定字符")
    @pytest.mark.parametrize(
        "base,args,expected",
        [
            ("hello world", ["d", "world"], True),
            ("hello world", ["l", "s"], False),
        ],
    )
    def test_ends_with_any(
        self,
        base,
        expected,
        args,
    ) -> None:
        assert StringUtil.ends_with_any(base, *args) == expected

    @allure.title("测试字符串是否被指定前后缀包裹")
    def test_is_surround(self) -> None:
        assert StringUtil.is_surround("hello world", "hello", "world")
        assert not StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=False)
        assert StringUtil.is_surround("hello world", "Hello", "world", case_insensitive=True)

    @allure.title("测试字符串所有字符都是空白")
    def test_is_all_whitespace(self) -> None:
        assert StringUtil.is_all_whitespace("")
        assert StringUtil.is_all_whitespace(" \t\n")
        assert not StringUtil.is_all_whitespace("hello")

    @allure.title("测试字符串是否是unicode字符串")
    def test_is_unicode_str(self) -> None:
        assert StringUtil.is_unicode_str("h")

    @allure.title("测试字符串是否是文件分隔符")
    def test_is_file_separator(self) -> None:
        assert StringUtil.is_file_separator("/")
        assert StringUtil.is_file_separator("\\")
        assert not StringUtil.is_file_separator(" ")
        with pytest.raises(ValueError):
            assert not StringUtil.is_file_separator("")

    @allure.title("测试字符串是否同时包含大小写")
    def test_is_mixed_case(self) -> None:
        with allure.step("步骤1:测试字符串是否同时包含大小写"):
            assert StringUtil.is_mixed_case("Hello World")
            assert StringUtil.is_mixed_case("hElLo wOrld")
            assert not StringUtil.is_mixed_case("hello world")
            assert not StringUtil.is_mixed_case("")

        with allure.step("步骤2:测试字符串是否包含大写字符"):
            assert StringUtil.has_uppercase("Hello World")
            assert StringUtil.has_uppercase("hElLo wOrld")
            assert not StringUtil.has_uppercase("hello world")
            assert not StringUtil.has_uppercase("")

        with allure.step("步骤3:测试字符串是否包含小写字符"):
            assert StringUtil.has_lowercase("Hello World")
            assert StringUtil.has_lowercase("hElLo wOrld")
            assert not StringUtil.has_lowercase("HELLO")
            assert not StringUtil.has_lowercase("")

    @allure.title("测试字符串在字母表的位置")
    def test_is_half_of_alphabet(self) -> None:
        with allure.step("步骤1:测试字符串是否在字母表的前半部分"):
            assert StringUtil.is_half_of_alphabet("abcdefg")
            assert StringUtil.is_half_of_alphabet("ABCDEFG")
            assert not StringUtil.is_half_of_alphabet("OPi")

        with allure.step("步骤2:测试字符串是否在字母表的后半部分"):
            assert StringUtil.is_last_half_of_alphabet("mnopqrstuvwxyz")
            assert StringUtil.is_last_half_of_alphabet("MNOPQRSTUVWXYZ")
            assert not StringUtil.is_last_half_of_alphabet("aada")


@allure.feature("字符串工具类")
@allure.story("获取字符串的属性和方法")
@allure.description("测试获取字符串的属性和方法,例如长度,大小写等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestStringProperties:
    @allure.title("测试获取字符串公共前后缀")
    @pytest.mark.parametrize(
        "text1,text2,expected",
        [
            ("hello world", "hello python", "hello "),
            ("programming", "progress", "progr"),
            ("hello world", "world hello", ""),
            ("hello world", "world hello", ""),
        ],
    )
    def test_get_common_prefix(
        self,
        text1,
        text2,
        expected,
    ) -> None:
        assert StringUtil.get_common_prefix(text1, text2) == expected

    @allure.title("测试获取字符串公共后缀")
    @pytest.mark.parametrize(
        "text1,text2,expected",
        [
            ("hello world", "hello pythonld", "ld"),
            ("programming world", "hello world", " world"),
            ("hello world", "world hello", ""),
            ("hello world", "world hello", ""),
        ],
    )
    def test_get_common_suffix(
        self,
        text1,
        text2,
        expected,
    ) -> None:
        assert StringUtil.get_common_suffix(text1, text2) == expected

    @allure.title("测试获取字符串长度和宽度")
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("hello world", 11),
            ("你好啊", 3),
            ("1234567890", 10),
            ("", 0),
        ],
    )
    def test_get_string_length(
        self,
        text,
        expected,
    ) -> None:
        with allure.step("步骤1:测试获取长度"):
            assert StringUtil.get_length(text) == expected

    @allure.title("测试获取字符串宽度")
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("你好啊", 6),
            ("1234567890", 10),
            ("", 0),
            ("\t", 1),
            ("\r", 1),
            ("\n", 1),
        ],
    )
    def test_get_string_width(
        self,
        text,
        expected,
    ) -> None:
        assert StringUtil.get_width(text) == expected

    @allure.title("测试获取注释后的字符串信息")
    @pytest.mark.parametrize(
        "text,comment_char,expected",
        [
            ("hello world", "--", "-- hello world"),
            ("你好啊", "--", "-- 你好啊"),
            ("", "--", "-- "),
            ("hello world", "#", "# hello world"),
            ("你好啊", "#", "# 你好啊"),
            ("", "#", "# "),
        ],
    )
    def test_get_annotation_str(
        self,
        text,
        comment_char,
        expected,
    ) -> None:
        assert StringUtil.get_annotation_str(text, comment_char) == expected

    @allure.title("测试获取字符串居中信息")
    @pytest.mark.parametrize(
        "text,fill,length,expected",
        [
            ("hello world", "=", 40, "=== hello world ===="),
            ("hello world", "=", 1, " hello world "),
        ],
    )
    def test_center_msg(
        self,
        text,
        fill,
        length,
        expected,
    ) -> None:
        assert StringUtil.get_center_msg(text, fill, length) == expected

    @allure.title("测试获取字符串的元音字母")
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("hello world", "eoo"),
            ("你好啊", ""),
            ("aeiounknknknknkjhknjniaodnwaondwo", "aeiouiaoaoo"),
        ],
    )
    def test_get_vowels_from_str(
        self,
        text,
        expected,
    ) -> None:
        assert StringUtil.get_vowels_from_str(text) == expected

    @allure.title("测试显示unicode字符")
    def test_show_unicode(self) -> None:
        s = "|"
        StringUtil.show_unicode_info(s)


@allure.feature("字符串工具类")
@allure.story("获取字符")
@allure.description("测试获取字符,例如获取随机中文、小写字符等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestGetString:
    @allure.title("测试生成名字序列")
    @pytest.mark.parametrize(
        "prefix",
        [
            ("prefix"),
            ("start"),
        ],
    )
    def test_generate_name_sequence(self, prefix) -> None:
        s = StringUtil.get_name_sequence(prefix)
        i = 0
        while i < 10:
            assert next(s) == f"{prefix}{i}"
            i += 1

    @allure.title("测试get_new_name方法")
    @pytest.mark.parametrize(
        "taken, base, expected, func",
        [
            (["name", "name_1", "name_2", "name_3"], "name_5", "name_5", None),
            (["name", "name_1", "name_2", "name_3"], "name", "name_4", None),
            (["name"], "name", "name_1", None),
            (["name"], "name", "name_new", lambda x: x + "_new"),
            (["name"], "name", "name_suffix", lambda x: x + "_suffix"),
            pytest.param(["name"], None, "name_1", None, marks=pytest.mark.xfail(raises=ValueError)),
        ],
    )
    def test_get_new_name(
        self,
        taken,
        base,
        expected,
        func,
    ) -> None:
        assert StringUtil.get_new_name(taken, base, func) == expected

    @allure.title("测试获取箱体字符串")
    def test_generate_box_string_from_dict_with_chinese(self):
        with allure.step("步骤1:测试带中文字符串的箱体字符串"):
            d = {
                "中文姓名": "李军",
                "英文姓名": "John Smith",
                "年龄": 27,
                "地址": "上海市黄浦区",
                "电话号码": "13987654321",
                "电子邮件": "john.smith@example.com",
                "职业": "软件工程师",
            }

            box_str = StringUtil.generate_box_string_from_dict(d, title="个人信息")
            logger.debug("\n" + box_str)

        with allure.step("步骤2:测试获取不带中文字符串的箱体字符串"):
            d = {
                0: "James Brown",
                1: "Mary Johnson",
                2: "Patricia Smith",
                3: "Robert Williams",
                4: "Linda Jones",
                5: "Michael Brown",
                6: "Elizabeth Garcia",
                7: "David Martinez",
                8: "Barbara Rodriguez",
                9: "Susan Wilson",
            }

            box_str = StringUtil.generate_box_string_from_dict(d)

    @allure.title("测试获取随机字符串")
    def test_get_random_str(self):
        with allure.step("步骤1:测试获取随机小写字符串"):
            n = random.randint(1, 10)
            s = StringUtil.get_random_str_lower(n)
            assert s.islower() and StringUtil.get_length(s) == n

        with allure.step("步骤2:测试获取随机大写字符串"):
            n = random.randint(1, 10)
            s = StringUtil.get_random_str_upper(n)
            assert s.isupper() and StringUtil.get_length(s) == n

        with allure.step("步骤3:测试获取随机capitalized字符串"):
            n = random.randint(1, 10)
            s = StringUtil.get_random_str_capitalized(n)
            assert s[0].isupper() and s[1:].islower() and StringUtil.get_length(s) == n

        with allure.step("步骤4:测试获取随机字符串"):
            n = random.randint(1, 10)
            s = StringUtil.get_random_strs(n)
            assert StringUtil.get_length(s) == n and StringUtil.is_string(s)

        with allure.step("步骤5:测试获取随机中文字符串"):
            n = random.randint(1, 10)
            s = StringUtil.get_random_chinese_generator(n)
            for i in s:
                assert StringValidator.is_chinese(i)

    @allure.title("测试获取罗马字符")
    def test_get_roman_num(self):
        generator = StringUtil.get_roman_range(1, 6)
        next(generator) == "I"
        next(generator) == "II"
        next(generator) == "III"
        next(generator) == "IV"
        next(generator) == "V"

    @allure.title("测试获取圆括号字符串")
    def test_get_parentheses(self) -> None:
        with allure.step("步骤1:测试获取圆括号字符串"):
            assert StringUtil.get_circled_number(1) == "①"
            assert StringUtil.get_circled_number(4) == "④"
        # TODO 更改 get_circled_number 实现
        logger.debug(ord("Ⓐ"))

    @allure.title("测试获取随机16进制字符串")
    def test_get_secure_random_hex_str(self) -> None:
        logger.debug(StringUtil.get_random_secure_hex(16))

    @allure.title("测试获取字符串中最多的字符")
    def test_get_most_frequent_char(self) -> None:
        s = "hello world"
        assert StringUtil.get_most_common_letter(s) == "l"
        s = "a你b好c啊d,b"
        assert StringUtil.get_most_common_letter(s) == "b"
        s = "aaaaa"
        assert StringUtil.get_most_common_letter(s) == "a"
        s = ""
        assert StringUtil.get_most_common_letter(s) == ""

    @allure.title("测试获取字符串各个位置的字符")
    def test_get_char(self) -> None:
        with allure.step("步骤1:测试获取字符右边的字符"):
            s = "abc"
            assert StringUtil.get_right(s, 1) == "c"
            assert StringUtil.get_right(s, 3) == "abc"
            assert StringUtil.get_right(s, 4) == "abc"

        with allure.step("步骤2:测试获取字符右边的字符，错误的输入"):
            with pytest.raises(ValueError):
                assert StringUtil.get_right(s, 0) == ""

    @allure.title("测试获取字符串的字符串-ASCII码对 ")
    def test_get_pair(self) -> None:
        s = "abc"
        res = StringUtil.get_ascii_number_pairs(s)
        assert res == [("a", 97), ("b", 98), ("c", 99)]

    @allure.title("测试字符串乱序获取")
    def test_shuffle_str(self) -> None:
        s = "abc"
        logger.debug(s)


@allure.feature("字符串工具类")
@allure.story("字符串操作")
@allure.description("测试字符串操作,例如字符串截取、替换、分割等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestStringOperation:
    @allure.title("测试字符串按长度分组")
    def test_group_by_length(cls) -> None:
        input_string = "abcdefghij"
        result = StringUtil.group_by_length(input_string, 3)
        assert result == ["abc", "def", "ghi", "j"]

    @allure.title("测试字符串缩写")
    def test_abbreviate_string(cls) -> None:
        assert StringUtil.abbreviate("abcdefg", 6) == "abc..."
        assert StringUtil.abbreviate(None, 7) == ""  # type: ignore
        assert StringUtil.abbreviate("abcdefg", 8) == "abcdefg"
        assert StringUtil.abbreviate("abcdefg", 4) == "a..."

        with pytest.raises(ValueError):
            StringUtil.abbreviate("abcdefg", 0)

    @allure.title("测试获取字符串分隔符之前的字符")
    def test_sub_before(cls) -> None:
        s1 = "2024-08-01"
        assert StringUtil.sub_before(s1, "-", False) == "2024"
        assert StringUtil.sub_before(s1, "-", True) == "2024-08"
        assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
        assert StringUtil.sub_before(None, "", True) == ""
        assert StringUtil.sub_before("", "", True) == ""
        assert StringUtil.sub_before("hello world", "", True) == "hello world"

    @allure.title("测试获取字符串分隔符之后的字符")
    def test_sub_after(cls) -> None:
        s1 = "2024-08-01"
        assert StringUtil.sub_after(s1, "-", False) == "08-01"
        assert StringUtil.sub_after(s1, "-", True) == "01"
        assert StringUtil.sub_before(s1, "年", False) == "2024-08-01"
        assert StringUtil.sub_before(None, "", True) == ""
        assert StringUtil.sub_before("", "", True) == ""
        assert StringUtil.sub_before("hello world", "", True) == "hello world"

    @allure.title("测试字符串移除所有的空白字符")
    def test_remove_blank(self) -> None:
        original = " hello world \n hello"
        res = StringUtil.remove_blank(original)
        assert res == "helloworldhello"

    @allure.title("测试移除前缀、后缀")
    def test_remove_prefix_and_suffix(self) -> None:
        with allure.step("步骤1:测试移除前缀"):
            s1 = "hello world"
            assert StringUtil.remove_prefix(s1, "hello") == " world"
            assert StringUtil.remove_prefix(s1, "world") == "hello world"
            assert StringUtil.remove_prefix(s1, "hello world") == ""

        with allure.step("步骤2:测试移除后缀"):
            s2 = "hello world"
            assert StringUtil.remove_suffix(s2, "world") == "hello "
            assert StringUtil.remove_suffix(s2, "hello") == "hello world"
            assert StringUtil.remove_suffix(s2, "hello world") == ""

    @allure.title("测试移除指定字符串")
    def test_remove_all(self) -> None:
        assert StringUtil.remove_all("hello world", "l", "h") == "eo word"
        assert StringUtil.remove_all("hello world", "l", "h", "w") == "eo ord"
        assert StringUtil.remove_all("hello world", "l", "h", "w", "o", "d") == "e r"

    @allure.title("测试根据空字符串转字符串")
    def test_empty_to_default(self) -> None:
        with allure.step("步骤1:测试空字符串转默认值"):
            assert StringUtil.empty_to_default("", "default") == "default"
            assert StringUtil.empty_to_default(" ", "default") == " "
            assert StringUtil.empty_to_default("s", "default") == "s"
            assert StringUtil.empty_to_default(None, "default") == "default"  # type: ignore

        with allure.step("步骤2:测试空字符串转None"):
            assert StringUtil.empty_to_none("") is None
            assert StringUtil.empty_to_none(" ") is not None
            assert StringUtil.empty_to_none("s") is not None

    @allure.title("测试None转字符串")
    def test_none_to_default(self) -> None:
        with allure.step("步骤1:测试None转默认值"):
            assert StringUtil.none_to_default(None, "default") == "default"  # type: ignore
            assert StringUtil.none_to_default(None, "default") == "default"  # type: ignore
            assert StringUtil.none_to_default("s", "default") == "s"

        with allure.step("步骤2:测试None转空字符串"):
            assert StringUtil.none_to_empty(None) == ""  # type: ignore
            assert StringUtil.none_to_empty("s") == "s"

    @allure.title("测试保留特定类型字符串")
    def test_retain_type_str(self) -> None:
        with allure.step("步骤1:测试保留数字字符串"):
            assert StringUtil.only_numerics("1234567890") == "1234567890"
            assert StringUtil.only_numerics("1234567890hello") == "1234567890"
            assert StringUtil.only_numerics("hello1234sdadsa567sdasd890") == "1234567890"

        with allure.step("步骤2:测试保留ASCII字符串"):
            assert StringUtil.only_ascii("hello world") == "hello world"
            assert StringUtil.only_ascii("hello1234sdadsa567sdasd890") == "hello1234sdadsa567sdasd890"
            assert StringUtil.only_ascii("a你b好c啊d") == "abcd"

        with allure.step("步骤3:测试保留小写字符"):
            assert StringUtil.only_lowercase("hello world") == "helloworld"
            assert StringUtil.only_lowercase("HELLO WORLD") == ""
            assert StringUtil.only_lowercase("a你b好c啊d") == "abcd"

        with allure.step("步骤4:测试保留大写字符"):
            assert StringUtil.only_uppercase("HELLO WORLD") == "HELLOWORLD"
            assert StringUtil.only_uppercase("hello world") == ""

        with allure.step("步骤5:测试保留英文字符"):
            StringUtil.only_alphabetic("hello1234sdadsa567sdasd890") == "hellosdadsasdasd"
            StringUtil.only_alphabetic("a你b好c啊d123213213") == "abcd"

        with allure.step("步骤6:测试保留字母和数字"):
            StringUtil.only_alphanumeric("你好啊, hello world 123") == "hello world 123"
            StringUtil.only_alphanumeric("a你b好c啊d123213213") == "abcd123213213"

        with allure.step("步骤7:测试保留可打印字符"):
            StringUtil.only_printable("你好啊, hello world 123\t\n") == "你好啊, hello world 123"
            StringUtil.only_printable("a你b好c啊\rd123213213") == "abcd123213213"

    @allure.title("测试字符串填充")
    def test_fill_string(self) -> None:
        with allure.step("步骤1:测试填充左侧字符"):
            assert StringUtil.fill_after("hello", "*", 10) == "hello*****"
            assert StringUtil.fill_after("hello", "*", 5) == "hello"
            assert StringUtil.fill_after("", "*", 10) == "**********"

        with allure.step("步骤2:测试填充右侧字符"):
            assert StringUtil.fill_before("hello", "*", 10) == "*****hello"
            assert StringUtil.fill_before("hello", "*", 5) == "hello"
            assert StringUtil.fill_before("", "*", 10) == "**********"

    @allure.title("测试字符串替换")
    def test_replace_string(self) -> None:
        with allure.step("步骤1:测试替换字符串"):
            assert StringUtil.replace_char_at("hello world", 0, "universe") == "universeello world"
            assert StringUtil.replace_char_at("hello world", 5, "universe") == "hellouniverseworld"

        with allure.step("步骤2:测试替换范围"):
            s = StringUtil.replace_range("hello world", "你好", 0)
            assert s == "你好llo world"

    @allure.title("测试字符串折叠")
    def test_string_unwrap(self) -> None:
        assert StringUtil.unwrap("aa", "a") == "a"
        assert StringUtil.unwrap("AABabcBAA", "A") == "ABabcBA"
        assert StringUtil.unwrap("AABabAAAAcBAA", "A") == "ABabAcBA"
        assert StringUtil.unwrap("#A", "#") == "#A"
        assert StringUtil.unwrap("A#", "#") == "A#"

    @allure.title("测试移除字符串中的字符")
    def test_remove_char(self) -> None:
        with allure.step("步骤1:测试根据位置索引移除字符串中的字符"):
            assert StringUtil.remove_char_at("hello world", 0) == "ello world"
            assert StringUtil.remove_char_at("hello world", 5) == "helloworld"
            assert StringUtil.remove_char_at("", 11) == ""

            with pytest.raises(ValueError):
                StringUtil.remove_char_at("hello world", -7)

        with allure.step("步骤2:测试根据范围移除字符串中的字符"):
            s = "abcdefg"
            assert StringUtil.remove_range(s, 0, 3) == "defg"

        with allure.step("步骤3:测试移除字符串中的某些类型的字符"):
            s = "我的世界，Hello World！"
            assert StringUtil.remove_non_ascii(s) == "Hello World"


@allure.feature("字符串工具类")
@allure.story("字符串编码")
@allure.description("测试字符串编码,例如罗马数字编码等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestStringEncode:
    @allure.title("测试字符串解码")
    def test_roman_decode(self) -> None:
        assert StringUtil.roman_decode("VII") == 7
        assert StringUtil.roman_decode("MCMXCIV") == 1994

    @allure.title("测试字符串编码")
    def test_roman_encode(self) -> None:
        assert StringUtil.equals(StringUtil.roman_encode(7), "VII")
        assert StringUtil.equals(StringUtil.roman_encode(1994), "MCMXCIV")
        assert StringUtil.equals(StringUtil.roman_encode(2020), "MMXX")
        assert StringUtil.equals(StringUtil.roman_encode(37), "XXXVII")

    @allure.title("测试字符串编码")
    def test_chinese_encode(self) -> None:
        with allure.step("步骤1:测试英文urf-8编码"):
            assert StringUtil.to_bytes("hello world").decode("utf-8") == "hello world"

        with allure.step("步骤2:测试中文utf-8编码"):
            assert StringUtil.to_bytes("你好啊").decode("utf-8") == "你好啊"

        with allure.step("步骤3:测试英文gbk编码"):
            assert StringUtil.to_str(StringUtil.to_bytes("hello world", "gbk"), "gbk") == "hello world"

        with allure.step("步骤4:测试中文gbk编码"):
            assert StringUtil.to_str(StringUtil.to_bytes("你好啊", "gbk"), "gbk") == "你好啊"

    @allure.title("测试字符串重复")
    def test_repeat_by_length(self) -> None:
        with allure.step("步骤1:测试按长度重复字符串"):
            assert StringUtil.repeat_by_length("hello", 10) == "hellohello"
            assert StringUtil.repeat_by_length("hello", 5) == "hello"
            assert StringUtil.repeat_by_length("", 10) == ""
            assert StringUtil.repeat_by_length("hello", 7) == "hellohe"

        with allure.step("步骤2:测试按数量重复字符串"):
            assert StringUtil.repeat_by_count("hello", 2) == "hellohello"
            assert StringUtil.repeat_by_count("hello", 1) == "hello"
            assert StringUtil.repeat_by_count("", 10) == ""

    @allure.title("测试命名格式之间相互转换")
    def test_name_format_convert(self) -> None:
        with allure.step("步骤1:测试驼峰命名格式转下划线命名格式"):
            assert StringUtil.camel_case_to_snake("HelloWorld") == "hello_world"
            assert StringUtil.camel_case_to_snake("HelloWorld123") == "hello_world123"
            assert StringUtil.camel_case_to_snake("firstTest") == "first_test"

        with allure.step("步骤2:测试下划线命名格式转驼峰命名格式"):
            assert StringUtil.snake_case_to_camel("hello_world") == "helloWorld"
            assert StringUtil.snake_case_to_camel("hello_world", True) == "HelloWorld"


@allure.feature("字符串工具类")
@allure.story("字符串格式化")
@allure.description("测试字符串格式化,例如货币格式化等")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("util", "string")
class TestStringFormat:
    @allure.title("测试字符串按货币格式化")
    def test_format_in_currency(self) -> None:
        assert StringUtil.equals(StringUtil.format_in_currency("123456789"), "123,456,789")
        assert StringUtil.equals(StringUtil.format_in_currency("123456789.45"), "123,456,789.45")
        assert StringUtil.equals(StringUtil.format_in_currency("-123456789.45"), "-123,456,789.45")
        assert StringUtil.equals(StringUtil.format_in_currency("0"), "0")
        assert StringUtil.equals(StringUtil.format_in_currency("-123456789"), "-123,456,789")

    @allure.title("测试字符串对齐")
    def test_align_text(self) -> None:
        s = "hello world, 你好啊"
        assert StringUtil.align_text(s, align="left") == " hello world, 你好啊"
        assert StringUtil.align_text(s, align="center") == " hello world, 你好啊 "
        assert StringUtil.align_text(s, align="right") == "hello world, 你好啊 "
