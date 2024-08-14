#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_text.py
@Date       :   2024/08/09
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/09
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import pytest
from loguru import logger

from .context_test import (
    AbstractStrFinder,
    CharsetUtil,
    FnvHash,
    NullMode,
    PasswdStrengthUtil,
    PatternFinder,
    PatternPool,
    StrFinder,
    StringUtil,
    StrJoiner,
    UnsupportedOperationError,
)


class TestJoiner:
    @classmethod
    def test_join_list_with_prefix_and_suffix(cls):
        joiner = StrJoiner(",", prefix="(", suffix=")")
        joiner.append("hello")
        joiner.append("world")
        assert joiner.get_merged_string() == "(hello,world)"
        joiner.append(*[1, 2, 3]).append("4")
        assert joiner.get_merged_string() == "(1,2,3,4)"

    @classmethod
    def test_join_list_with_separator(cls):
        joiner = StrJoiner(" ")
        joiner.append("hello")
        joiner.append("world")
        assert joiner.get_merged_string() == "hello world"

    @classmethod
    def test_get_instance(cls):
        joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
        test_new_joiner_1 = StrJoiner.get_instance_from_joiner(joiner)
        test_new_joiner_1.append("hello")
        test_new_joiner_1.append("world")
        assert test_new_joiner_1.get_merged_string() == "(hello,world)"

        test_new_joiner_2 = StrJoiner.get_instance(" ")
        test_new_joiner_2.append("hello")
        test_new_joiner_2.append("world")

        assert test_new_joiner_2.get_merged_string() == "hello world"

    @classmethod
    def test_not_initialized_joiner(cls):
        joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
        joiner.__initialized = False
        assert joiner.get_merged_string() == StringUtil.EMPTY

    @classmethod
    def test_set_params(cls):
        joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
        joiner.set_delimiter("|").set_prefix("[").set_suffix("]").set_empty_result("NULL").set_null_mode(NullMode.EMPTY)
        joiner.append("hello").append("world")
        assert joiner.get_merged_string() == "[hello|world]"

    @classmethod
    def test_null_mode(cls):
        joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
        joiner.set_null_mode(NullMode.IGNORE)
        joiner.append("hello").append(None).append(None)
        assert joiner.get_merged_string() == "(hello)"

        joiner.reset()
        joiner.set_null_mode(NullMode.EMPTY)
        joiner.append("hello").append(None).append(None)
        assert joiner.get_merged_string() == "(hello,,)"

        joiner.reset()
        joiner.set_null_mode(NullMode.NULL_STRING)
        joiner.append("hello").append(None).append(None)
        assert joiner.get_merged_string() == "(hello,NONE,NONE)"

        with pytest.raises(ValueError):
            joiner.set_null_mode("invalid_null_mode")
            joiner.append("hello").append(None).append(None)


class TestFinder:
    @classmethod
    def test_finder(cls) -> None:
        test_finder_1 = StrFinder("abcabc", "ab")
        test_finder_1.set_case_insensitive(True)
        start_idx = test_finder_1.start(0)

        assert start_idx == 0
        assert test_finder_1.success
        assert test_finder_1.end(start_idx) == 1

        test_finder_1.reset()
        assert not test_finder_1.success
        assert test_finder_1.end_idx == -1
        assert test_finder_1.text == ""

        test_finder_1.set_reverse(True).set_text("abcabc")
        assert test_finder_1.start(0) == 3

        test_finder_2 = StrFinder("abcabc", "assb")
        start_idx = test_finder_2.set_case_insensitive(True).start(0)
        assert start_idx == -1

        test_finder_2.reset()
        test_finder_2.set_text("assbassb").set_case_insensitive(False)
        start_idx = test_finder_2.start(3)

        assert start_idx == 4
        assert test_finder_2.success
        assert test_finder_2.end(start_idx) == 7

    @classmethod
    def test_create_abstract_finder_instance(cls) -> None:
        with pytest.raises(TypeError):
            AbstractStrFinder("abc")  # type: ignore

    @classmethod
    def test_PatternFinder(cls) -> None:
        finder = PatternFinder("SSSS13812345678", PatternPool.MOBILE)
        assert finder.start(3) == 4


class TestPasswd:
    @classmethod
    def test_passwd(cls) -> None:
        test_passwd_1 = "2hAj5#mne-ix.86H"
        assert PasswdStrengthUtil.get_strength_score(test_passwd_1) == 13
        test_passwd_2 = "123456"
        assert PasswdStrengthUtil.get_strength_score(test_passwd_2) == 0


class TestHash:
    @classmethod
    def test_hash(cls) -> None:
        test_cases = [
            "",  # 空字符串
            "a",  # 单个字符
            "abc",  # 短字符串
            "Hello, World!",  # 常见短语
            "1234567890",  # 数字字符串
            "The quick brown fox jumps over the lazy dog",  # 长句子
            "aaaaaa",  # 重复字符
            "😀",  # Emoji 表情
            "Hello, 世界",  # 包含Unicode字符
            " " * 1000,  # 长空格字符串
        ]
        print("32-bit Hash Results:")
        h = FnvHash()
        for i, case in enumerate(test_cases):
            hash_value_32 = h.hash_32(case)
            _ = h.hash_64(case)
            _ = h.hash_128(case)
            logger.debug(f"32-bit Hash value: {hash_value_32}")

        with pytest.raises(UnsupportedOperationError):
            h.hash("sdadsa")

        h.hash_32("hello world".encode(CharsetUtil.UTF_8))
