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

import allure

from .context_test import Singleton, StringUtil, TraceUsedTime, UnCheckFunction


@Singleton
class SingletonCls:
    def __init__(self, name) -> None:
        self.name = name


@allure.feature("自定义装饰器")
@allure.description("自定义装饰器,可以计算运算时间, 单例模式等功能")
@allure.tag("装饰器")
class TestDecorator:
    @allure.story("测试TraceUsedTime装饰器")
    @allure.description("测试TraceUsedTime装饰器,可以计算函数执行时间")
    class TestUseTime:
        @allure.title("测试TraceUsedTime装饰器")
        @TraceUsedTime("enter msg", "exit msg")
        def test_trace_used_time(self) -> None:
            time.sleep(1)

    @allure.story("测试 UnCheckFunction 装饰器")
    @allure.description("测试 UnCheckFunction 装饰器, 可以提示调用者函数是否会对参数进行检测")
    class TestUnCheckedFunction:
        @allure.title("测试 UnCheckFunction 装饰器")
        @UnCheckFunction(True)
        def test_uncheck_function(self) -> None:
            print("test_uncheck_function")

    @allure.story("测试单例模式")
    @allure.description("测试单例模式, 可以保证一个类只有一个实例")
    class TestSingleton:
        @allure.title("测试单例模式")
        def test_singleton(self) -> None:
            s1 = SingletonCls("s1")
            s2 = SingletonCls("s2")
            assert StringUtil.equals(s1.name, s2.name)
            assert s1 is s2
