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

from .context import AbstractStrFinder, PatternFinder, PatternPool, StrFinder, StrJoiner


class TestJoiner:
    @classmethod
    def test_join_list_with_prefix_and_suffix(cls):
        joiner = StrJoiner(",", prefix="(", suffix=")")
        joiner.append("hello")
        joiner.append("world")
        assert joiner.get_merged_string() == "(hello,world)"
        joiner.append(*[1, 2, 3]).append("4")
        assert joiner.get_merged_string() == "(1,2,3,4)"


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
