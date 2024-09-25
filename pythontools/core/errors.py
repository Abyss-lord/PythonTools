#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   errors.py
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

from collections.abc import Callable
from typing import Any


class BaseToolException(Exception):
    def __init__(self, msg: str) -> None:
        self._msg = f"Tool module Exception: {msg}"

    def __str__(self) -> str:
        return repr(self._msg)


class RegexValidationError(BaseToolException):
    def __init__(self, pattern, s, msg: str = "") -> None:
        super().__init__(msg)
        self.pattern = pattern
        self.s = s


class DecoratorException(BaseToolException):
    def __init__(
        self,
        decorator: Callable[[Callable[[Any], Any]], Any],
        msg: str,
    ) -> None:
        self._msg = f"Decorator {decorator.__name__} Exception: {msg}"


class LoggerException(BaseToolException):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Logger Exception Error: {msg}")


class ConversionError(Exception):
    def __init__(self, value: Any, type_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.type_name = type_name

    def __str__(self) -> str:
        return f"ConversionError: {self.value}, type:{type(self.value)} cannot be converted to {self.type_name}"


class UnsupportedOperationError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class DatetimeParseError(ValueError):
    pass


class CalendarError(Exception):
    """
    Base Calendar Error
    """


class UnsupportedDateType(CalendarError):
    """
    Raised when trying to use an unsupported date/datetime type.
    """
