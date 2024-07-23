#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   color_constant.py
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

# 颜色常量


class Color:
    RGB_COLOR_BOUND = 256

    def __init__(self, red: int, green: int, blue: int, *, alpha: float = 1.0) -> None:
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha

    @staticmethod
    def is_rgb_value(val) -> bool:
        return 0 <= val <= Color.RGB_COLOR_BOUND

    @property
    def red(self) -> int:
        return self._red

    @red.setter
    def red(self, value: int) -> None:
        if not Color.is_rgb_value(value):
            raise ValueError(f"Invalid red value: {value}")
        self._red = value

    @property
    def green(self) -> int:
        return self._green

    @green.setter
    def green(self, value: int) -> None:
        if not Color.is_rgb_value(value):
            raise ValueError(f"Invalid green value: {value}")
        self._green = value

    @property
    def blue(self) -> int:
        return self._blue

    @blue.setter
    def blue(self, value: int) -> None:
        if not Color.is_rgb_value(value):
            raise ValueError(f"Invalid blue value: {value}")
        self._blue = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Color):
            return False
        return (
            self._red == other._red
            and self._green == other._green
            and self._blue == other._blue
        )

    def __repr__(self) -> str:
        return f"Color({self._red}, {self._green}, {self._blue})"
