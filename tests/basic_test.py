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


class TestBasic:
    def test_format_formula(self):
        for i in range(0, 7):
            for j in range(0, 7):
                print(f"{i=}, {j=}, {(7 - (i - j)) % 7}")

            print()
