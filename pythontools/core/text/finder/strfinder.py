#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   strfinder.py
@Date       :   2024/08/11
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/11
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import re
from typing import Self

from pythontools.core.errors import UnsupportedOperationError
from pythontools.core.utils.basicutils import StringUtil
from pythontools.core.utils.reutils import ReUtil

from .finder import Finder


class AbstractStrFinder(Finder):
    """
    Finder基类, 没有实现抽象方法，所以无法直接实例化.

     Attributes
    ----------
    text : str
        待查找的文本
    success : bool
        是否找到
    reverse : bool
        是否反向查找
    end_idx : int
        结束位置索引
    Methods
    -------
    set_text(self, text: str)
        设置待查找的文本
    set_reverse(self, reverse: bool)
        设置是否反向查找
    set_end_idx(self, end_idx: int)
        设置结束位置索引
    """

    def __init__(self, text: str) -> None:
        self.success = False
        self.text = text
        self.reverse = False
        self.end_idx = AbstractStrFinder.INDEX_NOT_FOUND
        super().__init__()

    def set_text(self, text: str) -> Self:
        """
        设置待查找的文本

        Parameters
        ----------
        text : str
            待查找的文本

        Returns
        -------
        Self
            返回 Finder 对象本身, 方便链式调用
        """
        self.text = text
        return self

    def set_reverse(self, reverse: bool) -> Self:
        """
        设置是否反向查找

        Parameters
        ----------
        reverse : bool
            是否反向查找

        Returns
        -------
        Self
            返回 Finder 对象本身, 方便链式调用
        """
        self.reverse = reverse
        return self

    def set_end_idx(self, end_idx: int) -> Self:
        """
        设置结束位置索引

        Parameters
        ----------
        end_idx : int
            给定的结束位置索引

        Returns
        -------
        Self
            返回 Finder 对象本身, 方便链式调用

        Raises
        ------
        ValueError
            end_idx 超出范围, 则抛出 ValueError
        """
        if end_idx < 0:
            self.end_idx = AbstractStrFinder.INDEX_NOT_FOUND
            return self
        if end_idx > StringUtil.get_length(self.text) - 1:
            raise ValueError("end_idx out of range")

        self.end_idx = end_idx
        return self


class StrFinder(AbstractStrFinder):
    """
    字符串查找器

    Attributes
    ----------
    str_to_find : str
        要查找的字符串
    case_insensitive : bool
        是否忽略大小写

    Methods
    -------
    set_case_insensitive(self, case_insensitive: bool)
        设置是否忽略大小写
    set_str_to_find(self, str_to_find: str)
        设置要查找的字符串
    start(self, from_idx: int)
        开始查找, 如果查找到, 则返回开始位置索引, 否则返回-1
    end(self, start_idx: int)
        根据给定的查找结果起始索引，返回结束位置索引
    reset(self)
        重置各个参数和标志位
    """

    def __init__(self, text: str, str_to_find: str) -> None:
        self.str_to_find = str_to_find
        self.case_insensitive = False
        super().__init__(text)

    def set_case_insensitive(self, case_insensitive: bool) -> Self:
        """
        设置是否忽略大小写

        Parameters
        ----------
        case_insensitive : bool
            是否忽略大小写

        Returns
        -------
        Self
            Finder对象本身, 方便链式调用
        """
        self.case_insensitive = case_insensitive
        return self

    def set_str_to_find(self, str_to_find: str) -> Self:
        """
        设置要查找的字符串

        Parameters
        ----------
        str_to_find : str
            给定的要查找的字符串

        Returns
        -------
        Self
            Finder对象本身, 方便链式调用
        """
        self.str_to_find = str_to_find
        return self

    def start(self, from_idx: int) -> int:
        """
        开始查找起始字段索引

        Parameters
        ----------
        from_idx : int
            查找开始位置索引

        Returns
        -------
        int
            如果没有找到返回-1,否则返回开始位置索引
        """
        if from_idx < 0:
            from_idx = 0

        text_length = StringUtil.get_length(self.text)
        str_to_find_length = StringUtil.get_length(self.str_to_find)

        if text_length < str_to_find_length or from_idx + str_to_find_length > text_length:
            return AbstractStrFinder.INDEX_NOT_FOUND

        if self.reverse:
            start_idx = StringUtil.last_index_of(
                self.text,
                from_idx,
                self.str_to_find,
                self.case_insensitive,
            )
        else:
            start_idx = StringUtil.first_index_of(
                self.text,
                from_idx,
                self.str_to_find,
                self.case_insensitive,
            )

        if start_idx != StrFinder.INDEX_NOT_FOUND:
            self.success = True

        return start_idx if self.success else StrFinder.INDEX_NOT_FOUND

    def end(self, start_idx: int) -> int:
        """
        根据给定的查找结果起始索引，返回结束位置索引

        Parameters
        ----------
        start_idx : int
            给定的查找结果索引, start 方法的返回值

        Returns
        -------
        int
            如果没有找到返回-1,否则返回结束位置索引
        """
        if start_idx == StrFinder.INDEX_NOT_FOUND:
            return StrFinder.INDEX_NOT_FOUND
        else:
            return start_idx + StringUtil.get_length(self.str_to_find) - 1

    def reset(self) -> None:
        """
        重置各个参数和标志位
        1. success: 是否找到
        2. end_idx: 结束位置索引
        3. text: 待查找的文本, Finder的核心是复用查找信息, 也就是说目标字符串是不变的, 变化的只有被查找文本。
        """
        self.success = False
        self.set_end_idx(StrFinder.INDEX_NOT_FOUND)
        self.text = ""


class PatternFinder(AbstractStrFinder):
    def __init__(
        self,
        text: str,
        regex: str | re.Pattern,
        case_insensitive: bool = False,
    ) -> None:
        self.pattern: re.Pattern = None  # type: ignore
        self.case_insensitive = case_insensitive
        self.matches: list[str] = []
        super().__init__(text)
        self._initialize_pattern(regex)

    def _initialize_pattern(
        self,
        regex: str | re.Pattern,
    ) -> None:
        if isinstance(regex, str):
            self.pattern = re.compile(regex, re.IGNORECASE if self.case_insensitive else 0)
        else:
            self.pattern = re.compile(regex.pattern, regex.flags)

    def set_pattern(
        self,
        regex: str | re.Pattern,
    ) -> Self:
        """
        设置使用的正则表达式模板

        Parameters
        ----------
        regex : str | re.Pattern
            新的正则表达式

        Returns
        -------
        Self
            Finder 对象本身, 方便链式调用
        """
        self._initialize_pattern(regex)
        return self

    def set_case_insensitive(self, case_insensitive: bool) -> Self:
        """
        设置是否忽略大小写

        Parameters
        ----------
        case_insensitive : bool
            是否忽略大小写

        Returns
        -------
        Self
            Finder对象本身, 方便链式调用
        """
        self.case_insensitive = case_insensitive
        self._initialize_pattern(self.pattern)
        return self

    def set_reverse(self, reverse: bool) -> Self:
        """
        设置是否反向查找

        Parameters
        ----------
        reverse : bool
            是否反向查找

        Returns
        -------
        Self
            Finder对象本身, 方便链式调用

        Raises
        ------
        UnsupportedOperationError
            调用该方法时抛出异常
        """
        raise UnsupportedOperationError("Reverse is invalid for Pattern")

    def start(self, from_idx: int) -> int:
        """
        开始查找起始字段索引

        Parameters
        ----------
        from_idx : int
            查找开始位置索引

        Returns
        -------
        int
            如果没有找到返回-1,否则返回开始位置索引
        """
        matches = ReUtil.find_all(self.pattern, self.text, from_idx)
        if not matches:
            return PatternFinder.INDEX_NOT_FOUND
        else:
            self.matches = matches
            return StringUtil.first_index_of(self.text, from_idx, matches[0])

    def end(self, start_idx: int) -> int:
        """
        根据给定的查找结果起始索引，返回结束位置索引

        Parameters
        ----------
        start_idx : int
            给定的查找结果索引, start 方法的返回值

        Returns
        -------
        int
            如果没有找到返回-1,否则返回结束位置索引
        """
        first_item = self.matches[0]
        return start_idx + StringUtil.get_length(first_item) - 1

    def reset(self) -> None:
        """
        重置各个参数和标志位
        1. success: 是否找到
        2. end_idx: 结束位置索引
        3. text: 待查找的文本, Finder的核心是复用查找信息, 也就是说目标字符串是不变的, 变化的只有被查找文本。
        4. matches: 匹配结果列表
        """
        self.success = False
        self.set_end_idx(PatternFinder.INDEX_NOT_FOUND)
        self.text = ""
        self.matches = []
