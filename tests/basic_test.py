#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_basic.py
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
import os


class TestBasic:
    def hex_dump(self, b):
        # hex
        h = [f"{x:02x}" for x in b]
        h = [h[i : i + 16] for i in range(0, len(h), 16)]
        h = [" ".join(x) for x in h]
        # ascii
        a = "".join(chr(x) if x in range(32, 127) else "." for x in b)
        a = [a[i : i + 16] for i in range(0, len(a), 16)]
        # dump
        d = ["  ".join([x, y]) for x, y in zip(h, a)]
        d = os.linesep.join(d)
        return d

    def test_format_formula(self):
        print(self.hex_dump(os.urandom(64)))
