#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   typehint.py
@Date       :   2024/08/05
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/05
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

from os import PathLike
from typing import TypeAlias, TypeVar

# here put the import lib
StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]
FileDescriptorOrPath: TypeAlias = int | StrOrBytesPath
PrimitiveType: TypeAlias = int | float | str | bool | bytes | bytearray | memoryview
ContainerType: TypeAlias = list | tuple | set | frozenset | dict
T = TypeVar("T")
