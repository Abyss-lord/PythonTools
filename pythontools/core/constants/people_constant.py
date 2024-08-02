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
import typing
from collections import namedtuple
from enum import Enum

Person = namedtuple("Person", ["sex", "sex_code"])


MALE_SET: typing.FrozenSet[str] = frozenset(["MALE", "male", "男性", "男", "男的"])
FEMALE_SET: typing.FrozenSet[str] = frozenset([
    "FEMALE",
    "female",
    "女性",
    "女",
    "女的",
])


class Gender(Enum):
    MALE = Person(sex="男性", sex_code=1)
    FEMALE = Person(sex="女性", sex_code=2)

    @classmethod
    def get_gender_by_code(cls, code: int) -> "Gender":
        if code % 2 == 1:
            return cls.MALE
        else:
            return cls.FEMALE

    @classmethod
    def get_gender_by_name(cls, name: str) -> "Gender":
        if name in MALE_SET:
            return cls.MALE
        elif name in FEMALE_SET:
            return cls.FEMALE
        else:
            raise ValueError(f"Invalid name: {name}")
