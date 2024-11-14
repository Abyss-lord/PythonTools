#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   graycode.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import typing

from ..radix_utils import RadixUtil


class GrayCode:
    """
    格雷码（循环二进制单位距离码）是任意两个相邻数的代码只有一位二进制数不同的编码，它与奇偶校验码同属可靠性编码。

    """

    @classmethod
    def gray_code_generator(cls, n: int) -> typing.Generator[str, None, None]:
        if n < 0:
            raise ValueError("n must be non-negative")

        code = [0 for _ in range(n)]

        i = 0
        while True:
            # PERF 可能会有性能问题
            if not code:
                yield "0"
            else:
                yield "".join([f"{i}" for i in code])

            i += 1
            p = RadixUtil.get_lst_one_idx(i)
            if p == n:
                break

            code[p] ^= 1  # 取反等价于异或上1
