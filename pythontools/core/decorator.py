#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   decorator.py
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

import functools
import threading
import time
import typing


# 单例模式装饰器
class Singleton(object):
    """
    单例模式装饰器

    *Example::*

    >>> @Singleton
    ... class A(object):
    ...     pass
    """

    def __init__(self, cls):
        self.__instance = None
        self.__cls = cls
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        self._lock.acquire()
        print(f"call {self.__cls=}, {self.__instance=}")
        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._lock.release()
        return self.__instance


class TraceUsedTime(object):
    """
    Trace used time inside a function.

    Will print to LOGFILE if you initialized logging with cup.log.init_comlog.

    example::

        import time

        from cup import decorators

        @decorators.TraceUsedTime(True)
        def test():
            print('test')
            time.sleep(4)


        # trace something with context. E.g. event_id
        def _test_trace_time_map(sleep_time):
            print('ready to work')
            time.sleep(sleep_time)


        traced_test_trace_time_map = decorators.TraceUsedTime(
            b_print_stdout=False,
            enter_msg='event_id: 0x12345',
            leave_msg='event_id: 0x12345'
        )(_test_trace_time_map)
        traced_test_trace_time_map(sleep_time=5)

    """

    def __init__(self, b_print_stdout=False, enter_msg="", leave_msg=""):
        """
        :param b_print_stdout:
            When b_print_stdout is True, CUP will print to both LOGFILE
            that passed to cup.log.init_comlog and stdout

        :param enter_msg:
            entrance msg before invoking the function

        :param leave_msg:
            exist msg after leaving the function

        If you never use cup.log.init_comlog, make sure b_print_stdout == True
        """
        self._b_print_stdout = b_print_stdout
        self._enter_msg = enter_msg
        self._leave_msg = leave_msg

    def __call__(self, function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = function(*args, **kwargs)
            end_time = time.time()
            print(f"func use time {end_time - start_time}")
            return res

        return wrapper
