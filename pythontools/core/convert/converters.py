#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   converters.py
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
from abc import ABC, abstractmethod
from numbers import Complex, Number
from typing import Any

from pythontools.core.constants.pattern_pool import PatternPool
from pythontools.core.decorator import Singleton
from pythontools.core.errors import ConversionError
from pythontools.core.utils.basic_utils import ReUtil

PRIMITIVE_TYPE = (int, float, str, bool)
NUMERIC_TYPE = Number
CONTAINER_TYPE = (list, tuple, set, dict, frozenset)


class Converter(ABC):
    @abstractmethod
    def convert(self, value: Any, default_value: Any, *, raise_exception: bool = False) -> Any: ...

    @abstractmethod
    def _convert(self, value: Any, default_value: Any, *, raise_exception: bool = False) -> Any: ...

    @abstractmethod
    def is_converted_type(self, value: Any) -> bool: ...

    @abstractmethod
    def get_descreption(self) -> str: ...


class AbstractConverter(Converter):
    def __init__(self, type_name: str) -> None:
        self.type_name = type_name

    def convert(self, value: Any, default_value: Any, *, raise_exception: bool = False) -> Any:
        if self.is_converted_type(value):
            return self._convert(value, default_value, raise_exception=raise_exception)
        if raise_exception:
            raise TypeError(f"Unsupported type: {type(value)}")
        return default_value

    def get_descreption(self) -> str:
        return f"Convert any value to {self.type_name}"


@Singleton
class StringConverter(AbstractConverter):
    def __init__(self) -> None:
        super().__init__("string")

    def _convert(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        if isinstance(value, PRIMITIVE_TYPE):
            return self.convert_primitive_value(value, default_value, raise_exception=raise_exception)
        else:
            return self.convert_container_value(value, default_value, raise_exception=raise_exception)

    def is_converted_type(self, value: Any) -> bool:
        return isinstance(value, (PRIMITIVE_TYPE, CONTAINER_TYPE))  # type: ignore  # noqa: UP038

    def convert_primitive_value(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        try:
            return str(value)
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, self.type_name) from err
        return default_value

    def convert_container_value(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        try:
            if isinstance(value, (list | tuple | set | frozenset)):
                return "".join([str(i) for i in value])
            elif isinstance(value, dict):
                return "".join([str(i) for i in value.keys()])
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, self.type_name) from err

        return default_value

    def get_descreption(self) -> str:
        return "Convert any value to string"


class IntegerConverter(AbstractConverter):
    def __init__(self) -> None:
        super().__init__("Integer")

    def _convert(self, value: Any, default_value: Any, *, raise_exception: bool = False) -> int:
        # 1. bool 类型
        # 2. int 类型
        # 3. float 类型
        # 4. 复数类型
        # 5. 字符串类型，包含整数和浮点数
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return int(value)
        elif isinstance(value, Complex):
            # NOTE 复数转整数，取的是模
            return abs(value.real)  # type: ignore
        elif isinstance(value, str):
            if ReUtil.is_match(PatternPool.FLOAT_NUM, value):
                return int(float(value))
            elif ReUtil.is_match(PatternPool.INTEGER, value):
                return int(value)

        try:
            return int(value)
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, self.type_name) from err

        return default_value

    def is_converted_type(self, value: Any) -> bool:
        return isinstance(value, (NUMERIC_TYPE | str))


class FloatConverter(AbstractConverter):
    def __init__(self) -> None:
        super().__init__("Float")

    def _convert(self, value: Any, default_value: float, *, raise_exception: bool = False) -> float:
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, int):
            return float(value)
        elif isinstance(value, float):
            return value
        elif isinstance(value, Complex):
            return abs(value)  # type: ignore
        elif isinstance(value, str):
            if ReUtil.is_match(PatternPool.FLOAT_NUM, value) or ReUtil.is_match(PatternPool.INTEGER, value):
                return float(value)

        try:
            return float(value)
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, self.type_name) from err

        return default_value

    def is_converted_type(self, value: Any) -> bool:
        return isinstance(value, (NUMERIC_TYPE | str))


class BooleanConverter(AbstractConverter):
    TRUE_SET: frozenset[str] = frozenset(
        [
            "true",
            "yes",
            "y",
            "t",
            "ok",
            "1",
            "on",
            "是",
            "对",
            "真",
            "對",
            "√",
        ]
    )
    FALSE_SET: frozenset[str] = frozenset(
        [
            "false",
            "no",
            "n",
            "f",
            "0",
            "off",
            "否",
            "错",
            "假",
            "錯",
            "×",
        ]
    )

    def __init__(self) -> None:
        super().__init__("Boolean")

    def _convert(self, value: Any, default_value: bool, *, raise_exception: bool = False) -> bool:
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return self.str_to_boolean(value, strict_mode=True)
        else:
            try:
                return bool(value)
            except Exception as err:
                if raise_exception:
                    raise ConversionError(value, self.type_name) from err

            return default_value

    def is_converted_type(self, value: Any) -> bool:
        return True

    def str_to_boolean(self, value_str: str, *, strict_mode: bool = False) -> bool:
        """
        转换字符串为boolean值
        :param value_str: 待转换字符串
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
        :return: boolean值
        """
        if not value_str.strip():
            return False

        value_str = value_str.strip().lower()
        true_flg = value_str in BooleanConverter.TRUE_SET
        false_flg = value_str in BooleanConverter.FALSE_SET

        return bool(value_str) if not true_flg and not false_flg else not false_flg
