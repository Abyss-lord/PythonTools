#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   type_constant.py
@Date       :   2024/08/06
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/06
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from collections import namedtuple
from enum import Enum, unique

FunctionTypeTuple = namedtuple("FunctionTypeTuple", ["name", "description"])


@unique
class FunctionType(Enum):
    NORMAL_FUNCTION = FunctionTypeTuple("normal_function", "普通函数")
    UNBIND_METHOD = FunctionTypeTuple("unbind_method", "未绑定的方法")
    BUILT_IN_METHOD = FunctionTypeTuple("built_in_method", "内置方法")
    GENERATOR_METHOD = FunctionTypeTuple("generator_method", "生成器方法")
    COROUTINE_METHOD = FunctionTypeTuple("coroutine_method", "协程方法")
    UNKNOWN_METHOD = FunctionTypeTuple("unknown_method", "未知方法")
