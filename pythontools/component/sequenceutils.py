#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     Utils
   Description :
   date：          2024/7/16
-------------------------------------------------
   Change Activity:
                   2024/7/16:
-------------------------------------------------
"""

import typing
import string
from loguru import logger


class CharsetUtil(object):
    ISO_8859_1: typing.Final[str] = "ISO-8859-1"
    UTF_8: typing.Final[str] = "UTF-8"
    GBK: typing.Final[str] = "GBK"


class BooleanUtil(object):
    TRUE_SET: typing.FrozenSet[str] = frozenset(
        ["true", "yes", "y", "t", "ok", "1", "on", "是", "对", "真", "對", "√"])
    FALSE_SET: typing.FrozenSet[str] = frozenset(
        ["false", "no", "n", "f", "0", "off", "否", "错", "假", "錯", "×"])
    DEFAULT_TRUE_STRING: typing.Final[str] = "TRUE"
    DEFAULT_FALSE_STRING: typing.Final[str] = "FALSE"

    @classmethod
    def negate(cls, state: bool, *, raise_exception: bool = False) -> bool:
        """
        安全取相反值
        :param state: Boolean值
        :param raise_exception: 相反的Boolean值
        :return:
        """
        if not isinstance(state, bool):
            if raise_exception:
                raise TypeError(f"{state} is not a boolean type")
            state = bool(state)
        return not state

    @classmethod
    def str_to_boolean(cls, value_str: str, *, strict_mode: bool = False) -> bool:
        """
        转换字符串为boolean值
        :param value_str: 待转换字符串
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: boolean值
        """
        if StringUtil.is_blank(value_str):
            return False

        value_str = value_str.strip().lower()
        true_flg = value_str in cls.TRUE_SET
        false_flg = value_str in cls.FALSE_SET

        if not true_flg and not false_flg:
            if strict_mode:
                raise ValueError(f"{value_str} is not a boolean value")
            return bool(value_str)

        return False if false_flg else True

    @classmethod
    def boolean_to_int(cls, value: bool, *, strict_mode: bool = False) -> int:
        """
        boolean值转为int
        :param value: 待测试的值
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: int 值
        """
        if not isinstance(value, bool):
            if strict_mode:
                raise ValueError(f"{value} is not a boolean value")
            return 1 if bool(value) else 0

        return 1 if value else 0

    @classmethod
    def to_str_true_and_false(cls, value: bool, *, strict_mode: bool = True) -> str:
        """
        将boolean转换为字符串 'true' 或者 'false'.
        :param value: Boolean值
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: 'true', 'false'
        """
        return cls.to_string(value, cls.DEFAULT_TRUE_STRING, cls.DEFAULT_FALSE_STRING,
                             strict_mode=strict_mode)

    @classmethod
    def to_str_on_and_off(cls, value: bool, *, strict_mode: bool = True) -> str:
        """
        将boolean转换为字符串 'on' 或者 'off'.
        :param value: Boolean值
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: 'on', 'off'
        """
        return cls.to_string(value, "YES", "NO", strict_mode=strict_mode)

    @classmethod
    def to_str_yes_no(cls, value: bool, *, strict_mode: bool = True) -> str:
        """
        将boolean转换为字符串 'yes' 或者 'no'.
        :param value: Boolean值
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: 'yes', 'no'
        """
        return cls.to_string(value, "YES", "NO", strict_mode=strict_mode)

    @classmethod
    def to_string(cls, value: bool, true_str: str, false_str: str, *,
                  strict_mode: bool = False) -> str:
        """
        将boolean转换为字符串
        :param value: Boolean值
        :param true_str:
        :param false_str:
        :param strict_mode: 是否启动严格模式，如果开启严格模式，则不会使用BOOL进行布尔运算，否则会进行布尔运算
        :return: 转换后的字符串
        """
        value = cls._check_boolean_value(value, strict_mode=strict_mode)

        if StringUtil.is_blank(true_str):
            true_str = cls.DEFAULT_TRUE_STRING
        if StringUtil.is_blank(false_str):
            false_str = cls.DEFAULT_FALSE_STRING

        return true_str if value else false_str

    @classmethod
    def and_all(cls, *values, strict_mode: bool = True) -> bool:
        """

        :param values:
        :param strict_mode:
        :return:
        """
        if SequenceUtil.is_empty(values):
            raise ValueError("Empty sequence")

        for flg in values:
            flg = cls._check_boolean_value(flg, strict_mode=strict_mode)
            if not flg:
                return False

        return True

    @classmethod
    def or_all(cls, *values, strict_mode: bool = True) -> bool:
        if SequenceUtil.is_empty(values):
            raise ValueError("Empty sequence")

        for flg in values:
            flg = cls._check_boolean_value(flg, strict_mode=strict_mode)
            if flg:
                return True

        return False

    @classmethod
    def xor(cls, *values: typing.List[bool], strict: bool = True) -> bool:
        pass

    @classmethod
    def _check_boolean_value(cls, value: bool, *, strict_mode: bool = False) -> bool:
        if not isinstance(value, bool) and strict_mode:
            raise ValueError(f"{value} is not a boolean value")

        return bool(value)


class SequenceUtil(object):
    EMPTY: typing.Final[str] = ""
    SPACE: typing.Final[str] = " "

    @classmethod
    def is_empty(cls, sequence: typing.Sequence) -> bool:
        """
        返回序列是否为空
        :param sequence: 待检测序列
        :return: 如果检测序列为空返回True，否则返回False
        """
        return sequence is None or len(sequence) == 0

    @classmethod
    def is_not_empty(cls, sequence: typing.Sequence) -> bool:
        """
        返回序列是否为非空。\n
        NOTE 依赖于 is_empty 实现。

        :param sequence:
        :return:
        """
        return not cls.is_empty(sequence)

    @classmethod
    def reverse_sequence(cls, sequence: typing.Sequence) -> typing.Sequence:
        """
        翻转序列
        :param sequence: 待翻转序列
        :return: 翻转后的序列
        """
        return sequence[::-1]


class StringUtil(SequenceUtil):

    @classmethod
    def is_blank(cls, s: typing.Optional[str], *, raise_type_exception: bool = False) -> bool:
        """
        判断给定的字符串是否为空，空字符串包括null、空字符串：""、空格、全角空格、制表符、换行符，等不可见字符.\n

        :param s: 被检测的字符串
        :param raise_type_exception: 如果类型错误，是否要抛出异常
        :return: 如果字符串为空返回True，否则返回False
        :raises: TypeError

        Example：
            >>> StringUtil.is_blank(None) # True
            >>> StringUtil.is_blank("") # True
            >>> StringUtil.is_blank("abc") # False
        """
        if not isinstance(s, str) and raise_type_exception:
            raise TypeError(f"{s} is not a string")

        if cls.is_empty(s):
            return True

        val = str(s)
        for c in val:
            if c in (string.ascii_letters + string.digits + string.punctuation):
                return False

        return True

    @classmethod
    def is_not_blank(cls, s: str, *, raise_type_exception: bool = False) -> bool:
        """
        判断给定的字符串是否为非空。\n
        NOTE 依赖于is_blank实现。

        :param s: 被检测的字符串
        :param raise_type_exception: 如果类型错误，是否要抛出异常
        :return: 如果字符串为非空返回True，否则返回False
        """
        return not cls.is_blank(s, raise_type_exception=raise_type_exception)

    @classmethod
    def has_blank(cls, *args) -> bool:
        """
        判断多个字符串中是否有空白字符串
        :param args: 待判断字符串
        :return: 如果有空白字符串返回True，否则返回False
        """
        if cls.is_empty(args):
            return True
        for arg in args:
            if cls.is_blank(arg):
                return True

        return False

    @classmethod
    def is_all_blank(cls, *args) -> bool:
        """
        给定的多个字符串是否全为空
        :param args: 待检测的多个字符串
        :return: 如果都为空则返回True，否则返回False
        """
        if cls.is_empty(args):
            return True

        for arg in args:
            if cls.is_not_blank(arg):
                return False

        return True

    @classmethod
    def none_to_empty(cls, s: str) -> str:
        """
        当给定字符串为null时，转换为Empty
        :param s: 待检测字符串
        :return: 转换后的字符串
        """
        return cls.none_to_default(s, cls.EMPTY)

    @classmethod
    def none_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是 null，则返回指定默认字符串，否则返回字符串本身。
        :param s: 要转换的字符串
        :param default_str: 默认字符串
        :return: 如果字符串是 null，则返回指定默认字符串，否则返回字符串本身。
        """
        return default_str if s is None else s

    @classmethod
    def empty_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是null或者""，则返回指定默认字符串，否则返回字符串本身。
        :param s: 要转换的字符串
        :param default_str: 默认字符串
        :return: 转换后的字符串
        """
        if s is None or cls.EMPTY == s:
            return default_str
        else:
            return s

    @classmethod
    def empty_to_none(cls, s: str) -> typing.Optional[str]:
        """
        当给定字符串为空字符串时，转换为null
        :param s: 被转换的字符串
        :return: 转换后的字符串
        """
        return None if cls.is_empty(s) else s

    @classmethod
    def blank_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是null或者""或者空白，则返回指定默认字符串，否则返回字符串本身。
        :param s: 要转换的字符串
        :param default_str: 默认字符串
        :return: 转换后的字符串
        """
        if cls.is_blank(s):
            return default_str
        else:
            return s

    @classmethod
    def to_bytes(cls, byte_or_str: typing.Union[bytes, str], encoding=CharsetUtil.UTF_8) -> bytes:
        """
        将字节序列或者字符串转换成字节序列
        :param byte_or_str: 待转换对象
        :param encoding: 编码方式
        :return: 如果是bytes序列则返回自身，否则编码后返回
        """
        assert isinstance(byte_or_str, bytes) or isinstance(byte_or_str, str)
        if isinstance(byte_or_str, bytes):
            return byte_or_str
        else:
            return byte_or_str.encode(encoding)

    @classmethod
    def to_str(cls, byte_or_str: typing.Union[bytes, str], encoding=CharsetUtil.UTF_8) -> str:
        """
        将字节序列或者字符串转换成字符串
        :param byte_or_str: 待转换对象
        :param encoding: 解码方式
        :return: 如果是字符串则返回自身，否则解码后返回
        """
        assert isinstance(byte_or_str, bytes) or isinstance(byte_or_str, str)
        if isinstance(byte_or_str, str):
            return byte_or_str
        else:
            return byte_or_str.decode(encoding)

    @classmethod
    def fill_before(cls, s: str, fill_char: str, length: int) -> str:
        """
        将已有字符串填充为规定长度，如果已有字符串超过这个长度则返回这个字符串。

        :param s: 被填充的字符串
        :param fill_char: 填充的字符
        :param length: 填充长度
        :return: 填充后的字符串
        """
        return s.rjust(length, fill_char)

    @classmethod
    def fill_after(cls, s: str, fill_char: str, length: int) -> str:
        """

        :param s: 被填充的字符串
        :param fill_char: 填充的字符
        :param length:
        :return: 填充后的字符串
        """
        return s.ljust(length, fill_char)

    @classmethod
    def get_center_msg(cls, s: str, fill_char: str, length: int) -> str:
        """
        获取打印信息，信息左右两侧由指定字符填充
        :param s: 被填充的字符串
        :param fill_char: 填充的字符
        :param length:
        :return: 填充后的字符串

        Example：
            >>> StringUtil.get_center_msg("hello world", "=", 40) # ==== hello world ====
            >>> StringUtil.get_center_msg("hello world", "=", 1) # hello world
        """
        single_side_width = length // 2
        return f" {s} ".center(single_side_width, fill_char)
