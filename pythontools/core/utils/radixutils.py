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


class RadixUtil:
    ZERO = "0"

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
