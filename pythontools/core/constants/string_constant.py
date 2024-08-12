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
from collections import namedtuple
from enum import Enum

DesensitizedTypeTuple = namedtuple("DesensitizedTypeTuple", ["description"])
PasswdStrengthTuple = namedtuple("PasswdStrengthTuple", ["name", "description", "strength"])


class CharPool:
    EMPTY: typing.Final[str] = ""
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
    ASTERISK: typing.Final[str] = "*"


class DesensitizedType(Enum):
    #  用户id
    USER_ID = DesensitizedTypeTuple("用户id")
    #  中文名
    CHINESE_NAME = DesensitizedTypeTuple("中文名")
    #  身份证号
    ID_CARD = DesensitizedTypeTuple("身份证号")
    #  座机号
    FIXED_PHONE = DesensitizedTypeTuple("座机号")
    #  手机号
    MOBILE_PHONE = DesensitizedTypeTuple("手机号")
    # 地址
    ADDRESS = DesensitizedTypeTuple("地址")
    # 电子邮件
    EMAIL = DesensitizedTypeTuple("电子邮件")
    #  密码
    PASSWORD = DesensitizedTypeTuple("密码")
    # 中国大陆车牌，包含普通车辆、新能源车辆
    CAR_LICENSE = DesensitizedTypeTuple("车牌号")
    # 银行卡
    BANK_CARD = DesensitizedTypeTuple("银行卡")
    # IPv4地址
    IPV4 = DesensitizedTypeTuple("IPv4地址")
    #  IPv6地址
    IPV6 = DesensitizedTypeTuple("IPv6地址")
    # 定义了一个first_mask的规则，只显示第一个字符。
    FIRST_MASK = DesensitizedTypeTuple("只显示第一个字符")
    # 定义了一个last_mask的规则，只显示最后一个字符。
    LAST_MASK = DesensitizedTypeTuple("只显示最后一个字符")
    # 全部不显示
    ALL_MASK = DesensitizedTypeTuple("全部不显示")

    def get_description(self) -> str:
        """
        显示枚举值描述信息

        Returns
        -------
        str
            枚举值描述信息
        """
        return self.value.description


class PasswdStrength(Enum):
    EASY = PasswdStrengthTuple("EASY", "简单", 0)
    MIDIUM = PasswdStrengthTuple("MIDIUM", "中等", 4)
    STRONG = PasswdStrengthTuple("STRONG", "强", 7)
    VERY_STRONG = PasswdStrengthTuple("VERY_STRONG", "非常强", 10)
    EXTREMELY_STRONG = PasswdStrengthTuple("EXTREMELY_STRONG", "超强", 13)


class CommonExpression:
    INDEX_NOT_FOUND = -1


class CharsetUtil:
    ISO_8859_1: typing.Final[str] = "ISO-8859-1"
    UTF_8: typing.Final[str] = "UTF-8"
    GBK: typing.Final[str] = "GBK"
