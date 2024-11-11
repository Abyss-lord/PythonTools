#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   convert_factory.py
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

from collections.abc import Mapping
from typing import Any

from pythontools.core.decorator import Singleton

from .converters import BooleanConverter, Converter, FloatConverter, IntegerConverter, StringConverter


@Singleton
class ConvertFactory:
    def __init__(self):
        self.converter_dict: Mapping[type, Converter] = {}  # type: ignore

        self.__initialize()

    def __initialize(self):
        self.converter_dict[str] = StringConverter()
        self.converter_dict[int] = IntegerConverter()
        self.converter_dict[float] = FloatConverter()
        self.converter_dict[bool] = BooleanConverter()

    def convert(
        self, target_type: type, value: Any, default_value: Any, raise_exception: bool
    ) -> Any:  # -> Any | None:
        converter = self.converter_dict.get(target_type)
        if converter is not None:
            return converter.convert(value, default_value, raise_exception=raise_exception)
        else:
            raise TypeError(f"Unsupported target type: {target_type}")
