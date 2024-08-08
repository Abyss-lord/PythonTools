#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_decorator.py
@Date       :   2024/08/08
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/08
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import time

from .context import Singleton, StringUtil, TraceUsedTime, UnCkeckFucntion


@Singleton
class SingletonCls:
    def __init__(self, name) -> None:
        self.name = name


class TestDecorator:
    @classmethod
    @TraceUsedTime("enter msg", "exit msg")
    def test_trace_used_time(cls) -> None:
        time.sleep(1)

    @classmethod
    @UnCkeckFucntion(True)
    def test_unckeck_function(cls) -> None:
        print("test_unckeck_function")

    @classmethod
    def test_singleton(cls) -> None:
        s1 = SingletonCls("s1")
        s2 = SingletonCls("s2")
        assert StringUtil.equals(s1.name, s2.name)
        assert s1 is s2
