# Copyright 2024 The pythontools Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
-------------------------------------------------
@File       :   numberutils.py
@Date       :   2024/11/13
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/11/13
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from decimal import Decimal


class NumberUtil:
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
