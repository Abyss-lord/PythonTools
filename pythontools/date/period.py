#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   period.py
@Date       :   2024/09/04
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/04
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from dataclasses import dataclass

from pythontools.core.constants.datetime_constant import DayType, EndDateType, _DayTyp


# TODO 实现类逻辑
@dataclass
class Period:
    number_of_days: int
    day_type: DayType

    def __init__(
        self,
        number_of_days: int,
        day_type: _DayTyp,
        end_date_type: EndDateType = EndDateType.EXCLUSIVE,
    ):
        self.number_of_days = number_of_days
        if end_date_type == EndDateType.INCLUSIVE:
            if self.number_of_days > 0:
                self.number_of_days -= 1
            elif self.number_of_days < 0:
                self.number_of_days += 1
        if isinstance(day_type, DayType):
            pass
        elif isinstance(day_type, str):
            day_type = DayType(day_type)
        else:
            raise ValueError(f"'{day_type}' is not an allowed value; Check the typing")
        self.day_type: DayType = day_type
