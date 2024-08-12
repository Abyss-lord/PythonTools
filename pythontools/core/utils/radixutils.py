#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   radixutils.py
@Date       :   2024/08/11
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/11
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from ..constants.string_constant import CommonExpression


class RadixUtil:
    ZERO = "0"
    INDEX_NOT_FOUND = CommonExpression.INDEX_NOT_FOUND

    @classmethod
    def convert_base(cls, num: int | str, from_base: int, to_base: int) -> str:
        """
        进制转换

        Parameters
        ----------
        num : typing.Union[int, str]
            要转换的数据
        from_base : int
            初始进制
        to_base : int
            目标进制

        Returns
        -------
        str
            转换后的字符串
        """

        def to_decimal(num: int | str, from_base: int) -> int:
            if isinstance(num, int):
                return num
            return int(num, base=from_base)

        def from_decimal(num: int, base: int) -> str:
            if num == 0:
                return cls.ZERO
            digits = []
            while num:
                digits.append(str(num % base))
                num //= base
            # PERF 倒转字符串效率低, 应该优化
            digits.reverse()
            return "".join(map(lambda x: str(x) if int(x) < 10 else chr(int(x) + 55), digits))

        decimal_val = to_decimal(num, from_base)
        return from_decimal(decimal_val, to_base)

    @classmethod
    def get_lst_one_idx(cls, i: int) -> int:
        """
        返回十进制数i的二进制表示中最后一个1相对于末尾的位置

        Parameters
        ----------
        i : int
            待求的十进制数

        Returns
        -------
        int
            如果给定的十进制数小于0返回-1, 否则返回二进制表示中最后一个1相对于末尾的位置
        """
        if i <= 0:
            return -1

        base_to_expression = cls.convert_base(i, 10, 2)
        length = len(base_to_expression)

        for i, v in enumerate(base_to_expression):
            if v == "1":
                return length - i - 1

        return cls.INDEX_NOT_FOUND
