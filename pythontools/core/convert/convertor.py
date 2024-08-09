#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   convertor.py
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

from typing import Any

from .convert_factory import ConvertFactory


class BasicConvertor:
    FACTORY = ConvertFactory()

    @classmethod
    def to_complex(cls, value: Any, default_val: int = 0, *, strict_mode: bool = False) -> complex:
        """

        :param value: 待转换参数
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式, 严格模式的情况下, 转换失败就会直接报错, 否则转换失败的情况返回默认值
        :return: 如果入参是None, 则返回None, 否则返回转换后的 Complex 值
        """
        return complex(value, value)

    @classmethod
    def to_int(cls, value: Any, default_val: int = 0, *, strict_mode: bool = False) -> int | None:
        """
        转换为int
        :param value: 待转换参数
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式, 严格模式的情况下, 转换失败就会直接报错, 否则转换失败的情况返回默认值
        :return: 如果入参是None, 则返回None, 否则返回转换后的INT值
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
        :param strict_mode: 是否启用严格模式, 严格模式的情况下, 转换失败就会直接报错, 否则转换失败的情况返回默认值
        :return: 如果入参是None, 则返回None, 否则返回转换后的浮点数
        """
        return float(value)

    @classmethod
    def to_number(cls, value: Any, default_val: int = 0, *, strict_mode: bool = False) -> int | float:
        # TODO 实现转换数字逻辑
        return 1

    @classmethod
    def to_bool(cls, value: Any, default_val: bool = False, *, strict_mode: bool = False) -> bool:
        """
        转换为布尔值
        :param value: 待转换的值
        :param default_val: 转换失败的默认值
        :param strict_mode: 是否启用严格模式, 严格模式的情况下, 转换失败就会直接报错, 否则转换失败的情况返回默认值
        :return: 如果入参是None, 则返回None, 否则返回转换后的布尔值
        """
        return bool(value)

    @classmethod
    def to_str(cls, value: Any, default_val: str = "", *, raise_exception: bool = False) -> str:
        if not raise_exception:
            return cls.convert_quietly(str, value, default_val)
        else:
            return cls.convert(str, value, default_val)

    @classmethod
    def convert_quietly(cls, t: type, value: Any, default_val: Any = None) -> Any:
        return cls.FACTORY.convert(t, value, default_val, raise_exception=False)

    @classmethod
    def convert(cls, t: type, value: Any, default_val: Any = None) -> Any:
        return cls.FACTORY.convert(t, value, default_val, raise_exception=False)
