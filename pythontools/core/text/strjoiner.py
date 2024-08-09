#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   strjoiner.py
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
from enum import IntEnum, auto
from typing import Any, Self

from ..basicutils import StringUtil
from ..constants.string_constant import CharPool
from ..convert.convertor import BasicConvertor


class NullMode(IntEnum):
    """
    空值处理模式
    """

    IGNORE = auto()  # 忽略空值
    EMPTY = auto()  # 空值用空字符串代替
    NULL_STRING = auto()  # 空值用字符串"null"代替


class StrJoiner:
    def __init__(self, delimiter: str | None = None, prefix: str | None = None, suffix: str | None = None):
        self.delimiter = delimiter if delimiter is not None else CharPool.SPACE
        self.prefix = prefix if prefix is not None else StringUtil.EMPTY
        self.suffix = suffix if suffix is not None else StringUtil.EMPTY

        self.empty_result = StringUtil.EMPTY
        self.null_mdoe = NullMode.NULL_STRING

        self.__data: list[str] = None  # type: ignore
        self.__initialized = False

    @staticmethod
    def get_instance_from_joiner(other_joiner: "StrJoiner") -> "StrJoiner":
        return StrJoiner(other_joiner.delimiter, other_joiner.prefix, other_joiner.suffix)

    @staticmethod
    def get_instance(delimiter: str | None = None, prefix: str | None = None, suffix: str | None = None) -> "StrJoiner":
        return StrJoiner(delimiter, prefix, suffix)

    def set_delimiter(self, delimiter: str) -> Self:
        self.delimiter = delimiter
        return self

    def set_prefix(self, prefix: str) -> Self:
        self.prefix = prefix
        return self

    def set_suffix(self, suffix: str) -> Self:
        self.suffix = suffix
        return self

    def set_empty_result(self, empty_result: str) -> Self:
        self.empty_result = empty_result
        return self

    def set_null_mode(self, null_mode: NullMode) -> Self:
        self.null_mdoe = null_mode
        return self

    def append(self, *values: Any) -> Self:
        """
        添加一个要合并的字符串或对象

        Parameters
        ----------
        values : Any
            要合并的字符串或对象

        Returns
        -------
        Self
            StrJoiner对象, 用于链式调用

        Raises
        ------
        ValueError
            如果空值处理模式不合法, 则抛出该异常
        """
        if not self.__initialized:
            self._initialize()

        for value in values:
            if value is None:
                if self.null_mdoe == NullMode.IGNORE:
                    continue
                elif self.null_mdoe == NullMode.EMPTY:
                    self.__data.append(StringUtil.EMPTY)
                    continue
                elif self.null_mdoe == NullMode.NULL_STRING:
                    self.__data.append("NONE")
                    continue
                else:
                    raise ValueError("Invalid null mode")
            self.__data.append(BasicConvertor.to_str(value))
        return self

    def get_merged_string(self) -> str:
        if not self.__initialized:
            return self.empty_result

        content_part = self.delimiter.join(self.__data)
        merged_str = self.prefix + content_part + self.suffix
        self.reset()

        return merged_str

    def reset(self) -> Self:
        self.__data = None  # type: ignore
        self.__initialized = False
        return self

    def _initialize(self):
        self.__data = []
        self.__initialized = True
