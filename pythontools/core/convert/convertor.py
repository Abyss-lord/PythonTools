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
    FACTORY: ConvertFactory = ConvertFactory()

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
    def to_int(cls, value: Any, default_val: int = 0, *, raise_exception: bool = False) -> int:
        if not raise_exception:
            return cls.convert_quietly(int, value, default_val)
        else:
            return cls.convert(int, value, default_val)

    @classmethod
    def to_float(cls, value: Any, default_val: float = 0.0, *, raise_exception: bool = False) -> float:
        if not raise_exception:
            return cls.convert_quietly(float, value, default_val)
        else:
            return cls.convert(float, value, default_val)

    @classmethod
    def to_number(cls, value: Any, default_val: int | float, *, raise_exception: bool = False) -> int | float:
        int_convert_result = cls.to_int(value, -1, raise_exception=raise_exception)
        float_convert_result = cls.to_float(value, float("inf"), raise_exception=raise_exception)
        if float_convert_result == float("inf") and int_convert_result == -1:
            return default_val
        elif float_convert_result == float("inf"):
            return int_convert_result
        else:
            return float_convert_result

    @classmethod
    def to_bool(cls, value: Any, default_val: bool = False, *, raise_exception: bool = False) -> bool:
        if not raise_exception:
            return cls.convert_quietly(bool, value, default_val)
        else:
            return cls.convert(bool, value, default_val)

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
        return cls.FACTORY.convert(t, value, default_val, raise_exception=True)
