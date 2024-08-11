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

from .context import StrJoiner


class TestJoiner:
    @classmethod
    def test_join_list_with_prefix_and_suffix(cls):
        joiner = StrJoiner(",", prefix="(", suffix=")")
        joiner.append("hello")
        joiner.append("world")
        assert joiner.get_merged_string() == "(hello,world)"
        joiner.append(*[1, 2, 3]).append("4")
        assert joiner.get_merged_string() == "(1,2,3,4)"
