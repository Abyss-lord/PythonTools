#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   basicvalidator.py
@Date       :   2024/07/24
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/24
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import typing


class BasicValidator(object):
    @classmethod
    def is_number(cls, value: typing.Any) -> bool:
        pass

    @classmethod
    def is_between(
        cls, val, min_val, max_val, *, raise_exception: bool = False
    ) -> bool:
        pass
