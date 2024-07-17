#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     convertor
   Description :
   date：          2024/7/17
-------------------------------------------------
   Change Activity:
                   2024/7/17:
-------------------------------------------------
"""
import typing
from typing import Any


class BasicConvertor:

    @classmethod
    def to_complex(cls, value: Any, default_val: int = 0, *, strict_mode: bool = False) -> complex:
        """

        :param value: 待转换参数
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式，严格模式的情况下，转换失败就会直接报错，否则转换失败的情况返回默认值
        :return: 如果入参是None，则返回None，否则返回转换后的 Complex 值
        """
        return complex(value, value)

    @classmethod
    def to_int(cls, value: Any, default_val: int = 0, *, strict_mode: bool = False) \
            -> typing.Optional[int]:
        """
        转换为int
        :param value: 待转换参数
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式，严格模式的情况下，转换失败就会直接报错，否则转换失败的情况返回默认值
        :return: 如果入参是None，则返回None，否则返回转换后的INT值
        """
        if value is None:
            return None
        return int(cls.to_float(value))

    @classmethod
    def to_float(cls, value: Any, default_val: str = "", *, strict_mode: bool = False) -> float:
        """
        转换为Float
        :param value: 待转换的值
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式，严格模式的情况下，转换失败就会直接报错，否则转换失败的情况返回默认值
        :return: 如果入参是None，则返回None，否则返回转换后的浮点数
        """
        return float(value)

    @classmethod
    def to_bool(cls, value: Any, default_val: bool = False, *, strict_mode: bool = False) -> bool:
        """
        转换为布尔值
        :param value: 待转换的值
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式，严格模式的情况下，转换失败就会直接报错，否则转换失败的情况返回默认值
        :return: 如果入参是None，则返回None，否则返回转换后的布尔值
        """
        return bool(value)

    @classmethod
    def to_str(cls, value: Any, default_val: str = "", *, strict_mode: bool = False) -> str:
        """
        转换为字符串值
        :param value: 待转换的值
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式，严格模式的情况下，转换失败就会直接报错，否则转换失败的情况返回默认值
        :return: 如果入参是None，则返回None，否则返回转换后的字符串
        """
        return f"{value}"
