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
from abc import ABC, abstractmethod
from typing import Self


class Finder(ABC):
    INDEX_NOT_FOUND = -1

    # 返回开始位置索引
    @abstractmethod
    def start_idx(self, from_idx: int) -> int: ...

    # 返回结束字符索引
    @abstractmethod
    def end_idx(self, from_idx: int) -> int: ...

    # 重置查找器
    @abstractmethod
    def reset(self) -> None: ...


class AbstractFinder(Finder):
    def __init__(self, text: str) -> None:
        self.text = text
        self.reverse = False
        super().__init__()

    def set_text(self, text: str) -> Self:
        self.text = text
        return self

    def set_reverse(self, reverse: bool) -> Self:
        self.reverse = reverse
        return self

    def start_idx(self, from_idx: int) -> int:
        raise NotImplementedError

    def end_idx(self, from_idx: int) -> int:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError


class StrFinder:
    def __init__(self, str_to_find: str) -> None:
        self.str_to_find = str_to_find
        self.case_insensitive = False

    def set_case_insensitive(self, case_insensitive: bool) -> Self:
        self.case_insensitive = case_insensitive
        return self
