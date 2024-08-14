#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   reutils.py
@Date       :   2024/07/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import re

from ..constants.pattern_pool import RegexPool
from ..errors import ValidationError
from .basicutils import SequenceUtil, StringUtil


class ReUtil:
    # 正则表达式匹配中文汉字
    RE_CHINESE = RegexPool.CHINESE
    # 正则表达式匹配中文字符串
    RE_CHINESES = RegexPool.CHINESES
    # 正则中需要被转义的关键字
    RE_KEY = {
        "$",
        "(",
        ")",
        "*",
        "+",
        ".",
        "[",
        "]",
        "?",
        "\\",
        "^",
        "{",
        "}",
        "|",
        ":",
        "<",
        ">",
        "=",
    }

    @classmethod
    def get_group_1(cls, pattern: re.Pattern, s: str) -> str | None:
        """
        获取匹配的第一个分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回第一个分组的字符串, 否则返回None

        Notes
        ----------
        1. 依赖于`get_matched_group_by_idx`方法
        """
        cls.is_match(pattern, s, raise_exception=False)
        return cls.get_matched_group_by_idx(pattern, s, 1)

    @classmethod
    def get_group_2(cls, pattern: re.Pattern, s: str) -> str | None:
        """
        获取匹配的第二个分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回第二个分组的字符串, 否则返回None

        Notes
        ----------
        1. 依赖于`get_matched_group_by_idx`方法
        """
        cls.is_match(pattern, s, raise_exception=False)
        return cls.get_matched_group_by_idx(pattern, s, 2)

    @classmethod
    def get_matched_group_by_idx(
        cls,
        pattern: re.Pattern,
        s: str,
        group_index: int = 1,
    ) -> str | None:
        """
        获取指定的分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串
        group_index : int, optional
            分组序号, by default 0

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回指定分组的字符串, 否则返回None

        Notes
        ----------
        1. 如果没有匹配, 返回None, 如果给定的分组序号大于分组数量-1, 也返回None
        2. 如果字符串为空, 也返回None
        """
        if StringUtil.is_blank(s):
            return None
        res = cls.get_matched_groups(pattern, s)
        return SequenceUtil.get_item_by_idx(res, group_index - 1)

    @classmethod
    def get_matched_groups(cls, pattern: re.Pattern, s: str) -> tuple[str, ...]:
        """
        获取所有匹配的分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串

        Returns
        -------
        _type_
            所有匹配的分组
        """
        matched = pattern.match(s)
        if matched is None:
            return tuple()
        return matched.groups()

    @classmethod
    def is_match(cls, pattern: re.Pattern, s: str, *, raise_exception: bool = False) -> bool:
        """
        检查是否匹配

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串
        raise_exception : bool, optional
            如果匹配失败, 是否抛出异常, by default False

        Returns
        -------
        bool
            如果匹配成功, 返回True, 如果匹配失败, 且raise_error为True, 抛出异常, 否则返回False

        Raises
        ------
        TypeError
            如果pattern不是re.Pattern对象抛出异常
        ValueError
            如果raise_error为True, 且匹配失败, 抛出ValueError异常
        """

        if not isinstance(pattern, re.Pattern):
            raise TypeError("pattern must be a re.Pattern object")

        res = pattern.search(s)
        if res is None and raise_exception:
            raise ValidationError(pattern, s, f"pattern {pattern} not match string {s}")

        return res is not None

    @classmethod
    def is_match_reg(cls, s: str, reg: str, *, raise_exception: bool = False) -> bool:
        """
        是否匹配正则表达式

        Parameters
        ----------
        s : str
            待匹配字符串
        reg : str
            待匹配正则表达式
        raise_exception : bool, optional
            匹配不成功是否引发异常, by default False

        Returns
        -------
        bool
            是否匹配成功
        """
        pattern = re.compile(reg)
        return cls.is_match(pattern, s, raise_exception=raise_exception)

    @classmethod
    def find_all(cls, pattern: re.Pattern, s: str, from_index: int = 0) -> list[str]:
        """
        找到所有匹配的字符串

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串

        Returns
        -------
        list[str]
            所有匹配的字符串列表
        """
        res = pattern.findall(s, from_index)
        return res
