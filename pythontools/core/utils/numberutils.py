#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   numberutils.py
@Date       :   2024/08/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from decimal import Decimal


class NumberUtil:
    @classmethod
    def is_number(cls, s):
        pass

    @classmethod
    def add(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确加法

        Returns
        -------
        Decimal
            加法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result += Decimal(arg)
        return result

    @classmethod
    def sub(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确减法

        Returns
        -------
        Decimal
            减法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result -= Decimal(arg)
        return result

    @classmethod
    def mul(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确乘法

        Returns
        -------
        Decimal
            乘法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result *= Decimal(arg)
        return result

    @classmethod
    def div(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确除法

        Returns
        -------
        Decimal
            除法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result /= Decimal(arg)
        return result
