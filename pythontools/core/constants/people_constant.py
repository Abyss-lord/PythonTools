#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   people_constant.py
@Date       :   2024/07/26
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/26
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from collections import namedtuple
from enum import Enum

Person = namedtuple("Person", ["sex", "sex_code"])


class Gender(Enum):
    MALE = Person(sex="男性", sex_code=1)
    FEMALE = Person(sex="女性", sex_code=2)

    @classmethod
    def get_sex(cls, code: int) -> "Gender":
        if code % 2 == 1:
            return cls.MALE
        else:
            return cls.FEMALE
