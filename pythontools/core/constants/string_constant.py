#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   string_constant.py
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


class CharPool:
    SPACE: typing.Final[str] = " "
    TAB: typing.Final[str] = "	"
    DOT: typing.Final[str] = "."
    SLASH: typing.Final[str] = "/"
    BACKSLASH: typing.Final[str] = "\\"
    CR: typing.Final[str] = "\r"
    LF: typing.Final[str] = "\n"
    DASHED: typing.Final[str] = "-"
    UNDERLINE: typing.Final[str] = "_"
    COMMA: typing.Final[str] = ","
    DELIM_START: typing.Final[str] = "{"
    DELIM_END: typing.Final[str] = "}"
    BRACKET_START: typing.Final[str] = "["
    BRACKET_END: typing.Final[str] = "]"
    DOUBLE_QUOTES: typing.Final[str] = '"'
    SINGLE_QUOTE: typing.Final[str] = "'"
    AMP: typing.Final[str] = "&"
    COLON: typing.Final[str] = ":"
    AT: typing.Final[str] = "@"
