#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   imgutils.py
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

from .basicutils import RandomUtil
from .constants.color_constant import Color


class ColorUtil:
    RGB_COLOR_BOUND = 256

    @classmethod
    def get_random_color(
        cls,
    ) -> str:
        red = RandomUtil.get_random_val_from_range(0, cls.RGB_COLOR_BOUND)
        green = RandomUtil.get_random_val_from_range(0, cls.RGB_COLOR_BOUND)
        blue = RandomUtil.get_random_val_from_range(0, cls.RGB_COLOR_BOUND)

        return Color(red, green, blue)