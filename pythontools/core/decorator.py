#!/usr/bin/env python
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
import os
import platform
import threading
import time
import typing
import warnings
from typing import Any

from pythontools.core.errors import DecoratorException


# 单例模式装饰器
class Singleton:
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

        if self.__instance is None:
            self.__instance = self.__cls(*args, **kwargs)
        self._lock.release()
        return self.__instance


class TraceUsedTime:
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


class UnCheckFunction:
    WARNING_MESSAGE = "The function {} does not validate its arguments,\
    which requires the caller to guarantee that the arguments is valid"

    def __init__(self, warning_enabled: bool = True) -> None:
        self.warning_enabled = warning_enabled

    def __call__(self, func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.warning_enabled:
                warnings.warn(self.WARNING_MESSAGE.format(func.__name__))
            return func(*args, **kwargs)

        return wrapper


def need_linux(func: typing.Callable[[Any], Any]) -> typing.Callable[[Any], Any]:
    """
    确保在linux系统下运行, 否则抛出异常

    Examples
    --------
    >>> from pythontools.core.decorator import need_linux
    >>> @need_linux
    ... def you_func():
    ...     print("test")


    Parameters
    ----------
    func : typing.Callable[[Any], Any]
        待装饰函数

    Returns
    -------
    typing.Callable[[Any], Any]
        装饰函数

    Raises
    ------
    DecoratorException
        如果运行的系统不是linux，则抛出异常
    """
    if platform.system() != "Linux":
        raise DecoratorException(
            need_linux,
            "The system is not linux." + "This functionality only supported in linux",
        )
    return func


def need_posix(func: typing.Callable[[Any], Any]) -> typing.Callable[[Any], Any]:
    """
    确保在posix系统下运行, 否则抛出异常

    Examples
    --------
    >>> from pythontools.core.decorator import need_posix
    >>> @need_posix
    ... def you_func():
    ...     print("test")



    Parameters
    ----------
    func : typing.Callable[[Any], Any]
        待装饰函数

    Returns
    -------
    typing.Callable[[Any], Any]
        待装饰函数

    Raises
    ------
    DecoratorException
        如果运行的系统不是posix, 则抛出异常
    """
    if os.name != "posix":
        raise DecoratorException(
            need_posix,
            "The system is not posix." + "This functionality only supported in posix",
        )
    return func


def need_mac(func: typing.Callable[[Any], Any]) -> typing.Callable[[Any], Any]:
    """
        确保在mac系统下运行, 否则抛出异常

        Examples
        --------
        >>> from pythontools.core.decorator import need_mac
        >>> @need_mac
        ... def you_func():
        ...     print("test")

    Parameters
        ----------
        func : typing.Callable[[Any], Any]
            待装饰函数

        Returns
        -------
        typing.Callable[[Any], Any]
            待装饰函数

        Raises
        ------
        DecoratorException
            如果运行的系统不是mac, 则抛出异常
    """
    if platform.system() != "Darwin":
        raise DecoratorException(
            need_mac,
            "The system is not mac." + "This functionality only supported in mac",
        )
    return func
