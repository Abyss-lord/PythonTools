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
from typing import Any

from ..decorator import Singleton
from ..errors import ConversionError

PRIMITIVE_TYPE = (int, float, str, bool)
CONTAINER_TYPE = (list, tuple, set, dict, frozenset)


class Converter(ABC):
    @abstractmethod
    def convert(self, value: Any, default_value: Any, *, raise_exception: bool = False) -> Any: ...

    @abstractmethod
    def get_descreption(self) -> str: ...


@Singleton
class StringConverter(Converter):
    def convert(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        if isinstance(value, PRIMITIVE_TYPE):
            return self.convert_primitive_value(value, default_value, raise_exception=raise_exception)
        elif isinstance(value, CONTAINER_TYPE):
            return self.convert_container_value(value, default_value, raise_exception=raise_exception)
        else:
            if raise_exception:
                raise TypeError(f"Unsupported type: {type(value)}")
            return default_value

    def convert_primitive_value(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        try:
            str_value = str(value)
            return str_value
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, "String") from err
        return default_value

    def convert_container_value(self, value: Any, default_value: str, *, raise_exception: bool = False) -> str:
        try:
            if isinstance(value, (list | tuple | set | frozenset)):
                return "".join([str(i) for i in value])
            elif isinstance(value, dict):
                return "".join([str(i) for i in value.keys()])
        except Exception as err:
            if raise_exception:
                raise ConversionError(value, "String") from err

        return default_value

    def get_descreption(self) -> str:
        return "Convert any value to string"
