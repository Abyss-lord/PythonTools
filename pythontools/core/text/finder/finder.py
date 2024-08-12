#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   finder.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from abc import ABC, abstractmethod

from pythontools.core.constants.string_constant import CommonExpression


class Finder(ABC):
    INDEX_NOT_FOUND = CommonExpression.INDEX_NOT_FOUND

    # 返回开始位置索引
    @abstractmethod
    def start(self, from_idx: int) -> int: ...

    # 返回结束字符索引
    @abstractmethod
    def end(self, start_idx: int) -> int: ...

    # 重置查找器
    @abstractmethod
    def reset(self) -> None: ...
