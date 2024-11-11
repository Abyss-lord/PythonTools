#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   datepattern.py
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
from enum import Enum, unique


@unique
class DatePattern(Enum):
    NORM_YEAR_PATTERN = "YYYY"
    NORM_MONTH_PATTERN = "YYYY-MM"
    ISO8601_PATTERN = "%Y-%m-%dT%H:%M:%S.%f%z"
    RFC822_PATTERN = "%a, %d %b %Y %H:%M:%S %z"

    def get_value(self):
        return self.value
