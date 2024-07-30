#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   basic_utils.py
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

import calendar
import itertools as it
import random
import string
import time
import typing
from datetime import date, datetime, timedelta, timezone, tzinfo
from typing import Any

import pytz

from .constants.time_constant import Quarter, TimeUnit
from .convertor import BasicConvertor


class RandomUtil:
    @classmethod
    def get_random_val_from_range(
        cls, start: int, end: int, *, both_include: bool = False
    ) -> int:
        """
        从给定范围返回随机值

        Parameters
        ----------
        start : int
            范围起始点
        end : int
            范围结束点
        both_include : bool, optional
            是否包含尾边界, by default False

        Returns
        -------
        int
            随机值

        Raises
        ------
        ValueError
            如果start > end, 则抛出异常
        """
        if start > end:
            raise ValueError(f"{start=} must be less than {end=}")

        return (
            random.randrange(start, end)
            if not both_include
            else random.randint(start, end)
        )

    @classmethod
    def get_random_item_from_sequence(
        cls, seq: typing.Sequence[Any]
    ) -> typing.Optional[Any]:
        """
        随机从序列中抽取元素
        :param seq: 待抽取序列
        :return: 序列元素
        """
        if SequenceUtil.is_empty(seq):
            return None
        return random.choice(seq)

    @classmethod
    def get_random_items_from_sequence(
        cls, seq: typing.Sequence[Any], k: int
    ) -> typing.List[Any]:
        """
        从给定的序列中随机选择 k 个元素。
        :param seq: 输入的序列, 可以是任何类型的序列（如列表、元组等）。
        :param k: 要从序列中随机选择的元素数量。
        :return: 包含从输入序列中随机选择的 k 个元素的列表。
        """

        if SequenceUtil.is_empty(seq):
            return list()

        if k < 0:
            raise ValueError(f"{k=} must be greater than or equal to 0")

        if k >= len(seq):
            return [i for i in seq]
        return random.sample(seq, k)

    @classmethod
    def get_random_distinct_items_from_sequence(
        cls, seq: typing.Sequence[Any], k: int
    ) -> typing.Set[Any]:
        """
        随机获得列表中的一定量的不重复元素, 返回Set

        Parameters
        ----------
        seq : typing.Sequence[Any]
            待获取序列
        k : int
            获取数量

        Returns
        -------
        typing.Set[Any]
            不重复元素的集合

        Raises
        ------
        ValueError
            如果k > len(seq), 则抛出异常
        ValueError
            如果无法获取足够的元素, 则抛出异常
        """
        if k > len(seq):
            raise ValueError(f"{k=} must be less than or equal to the length of {seq=}")

        res: typing.Set[Any] = set()
        cnt = 0

        while len(res) < k:
            random_val = cls.get_random_item_from_sequence(seq)
            res.add(random_val)
            cnt += 1
            if cnt > 2 * k:
                raise ValueError(f"Cannot get {k=} distinct items from {seq=}")
        return res

    @classmethod
    def get_random_booleans(cls, length: int) -> typing.Generator[bool, None, None]:
        """
        获取指定数量的布尔值

        Parameters
        ----------
        length : int
            序列长度

        Returns
        -------
        typing.Generator[bool, None, None]
            布尔值生成器

        Yields
        ------
        Iterator[typing.Generator[bool, None, None]]
            生成布尔类型的生成器
        """
        for _ in range(length):
            yield cls.get_random_boolean()

    @classmethod
    def get_random_boolean(cls) -> bool:
        """
        返回随机布尔值

        Returns
        -------
        bool
            随机布尔值
        """
        val = cls.get_random_val_from_range(0, 2)
        return val == 1

    @classmethod
    def get_random_chineses(cls, length: int = 10) -> typing.Generator[str, None, None]:
        """
        获取指定长度的随机中文字符

        Parameters
        ----------
        length : int, optional
            字符序列长度, by default 10

        Returns
        -------
        typing.Generator[str, None, None]
            随机中文字符生成器

        Yields
        ------
        Iterator[typing.Generator[str, None, None]]
            随机中文字符生成器
        """
        for _ in range(length):
            yield cls.get_random_chinese()

    @classmethod
    def get_random_chinese(cls) -> str:
        """
        获取随机中文字符

        Examples
        --------
        >>> RandomUtil.get_random_chinese() # 输出: '龥'
        >>> RandomUtil.get_random_chinese() # 输出: '可'

        Returns
        -------
        str
            随机中文字符

        Notes
        --------
        1. 该方法依赖于`StringUtil.get_random_chinese()`
        """
        return StringUtil.get_random_chinese()

    @classmethod
    def get_random_float(cls) -> float:
        """
        获取随机浮点数

        Returns
        -------
        float
            随机浮点数, [0, 1)之间
        """
        return cls.get_random_float_with_range_and_precision(0.0, 1.0)

    @classmethod
    def get_random_floats_with_range_and_precision(
        cls, start: float, end: float, *, precision: int = 3, length: int = 10
    ) -> typing.Generator[float, None, None]:
        """
        返回指定长度的随机浮点数

        Parameters
        ----------
        start : float
            生成范围下限
        end : float
            生成范围上限
        precision : int, optional
            浮点数精度, by default 3
        length : int, optional
            序列长度, by default 10

        Returns
        -------
        typing.Generator[float, None, None]
            随机浮点数生成器
        """
        for _ in range(length):
            yield cls.get_random_float_with_range_and_precision(
                start, end, precision=precision
            )

    @classmethod
    def get_random_float_with_range_and_precision(
        cls, start: float, end: float, *, precision: int = 3
    ) -> float:
        """
        返回随机浮点数

        Parameters
        ----------
        start : float
            生成范围下限
        end : float
            生成范围上限
        precision : int, optional
            浮点数精度, by default 3

        Returns
        -------
        float
            随机浮点数
        """
        if start >= end:
            raise ValueError(f"{start=} must be less than {end=}")
        random_float = round(random.uniform(start, end), precision)
        return random_float

    @classmethod
    def get_random_complex(cls) -> complex:
        """
        获取随机复数

        Returns
        -------
        complex
            随机复数
        """
        real_part = cls.get_random_float()
        imag_part = cls.get_random_float()
        return complex(real_part, imag_part)

    @classmethod
    def get_random_complexes_with_range_and_precision(
        cls,
        real_range: typing.Tuple[float, float],
        imag_range: typing.Tuple[float, float],
        *,
        precision: int = 3,
        length: int = 10,
    ) -> typing.Generator[complex, None, None]:
        """
        返回指定长度的随机复数

        Parameters
        ----------
        real_range : typing.Tuple[float, float]
            实部生成范围
        imag_range : typing.Tuple[float, float]
            虚部生成范围
        precision : int, optional
            浮点数精度, by default 3
        length : int, optional
            序列长度, by default 10

        Returns
        -------
        typing.Generator[complex, None, None]
            随机复数生成器
        """
        for _ in range(length):
            yield cls.get_random_complex_with_range_and_precision(
                real_range, imag_range, precision=precision
            )

    @classmethod
    def get_random_complex_with_range_and_precision(
        cls,
        real_range: typing.Tuple[float, float],
        imag_range: typing.Tuple[float, float],
        *,
        precision: int = 3,
    ) -> complex:
        """
        获取随机复数

        Parameters
        ----------
        real_range : typing.Tuple[float, float]
            实部生成范围
        imag_range : typing.Tuple[float, float]
            虚部生成范围
        precision : int, optional
            浮点数精度, by default 3

        Returns
        -------
        complex
            随机复数
        """
        real_part = cls.get_random_float_with_range_and_precision(
            *real_range, precision=precision
        )
        imag_part = cls.get_random_float_with_range_and_precision(
            *imag_range, precision=precision
        )

        return complex(real_part, imag_part)

    @classmethod
    def get_random_bytes(cls, length: int) -> bytes:
        # todo
        raise NotImplementedError()

    @classmethod
    def get_random_date(cls) -> date:
        """
        获取随机日期对象

        Returns
        -------
        date
            随机日期对象

        Notes
        -------
        1. 该方法依赖于`DatetimeUtil.get_random_date()`
        """
        return DatetimeUtil.get_random_date()

    @classmethod
    def get_random_datetime(cls) -> datetime:
        """
        获取随机日期+时间

        Returns
        -------
        datetime
            随机日期+时间, datetime对象

        Notes
        -------
        1. 该方法依赖于`DatetimeUtil.get_random_datetime()`
        """
        return DatetimeUtil.get_random_datetime()

    @classmethod
    def get_random_str_upper(cls, k: int) -> str:
        """
        获取指定长度的随机大写字母字符串

        Parameters
        ----------
        k : int
            字符串长度

        Returns
        -------
        str
            随机大写字母字符串

        Notes
        -------
        1. 该方法依赖于`StringUtil.get_random_strs()`
        """
        basic_str = StringUtil.get_random_strs(k)
        return basic_str.upper()

    @classmethod
    def get_random_str_lower(cls, k: int) -> str:
        """
        获取指定长度的随机小写字母字符串

        Parameters
        ----------
        k : int
            字符串长度

        Returns
        -------
        str
            随机小写字母字符串

        Notes
        -------
        1. 该方法依赖于`StringUtil.get_random_strs()`
        """
        basic_str = StringUtil.get_random_strs(k)
        return basic_str.lower()

    @classmethod
    def get_random_str_capitalized(cls, k: int) -> str:
        """
        获取指定长度的随机首字母大写字母字符串

        Parameters
        ----------
        k : int
            字符串长度

        Returns
        -------
        str
            随机首字母大写字母字符串

        Notes
        -------
        1. 该方法依赖于`StringUtil.get_random_strs()`
        """
        basic_str = StringUtil.get_random_strs(k)
        return basic_str.capitalize()


class CharsetUtil(object):
    ISO_8859_1: typing.Final[str] = "ISO-8859-1"
    UTF_8: typing.Final[str] = "UTF-8"
    GBK: typing.Final[str] = "GBK"


class BooleanUtil(object):
    TRUE_SET: typing.FrozenSet[str] = frozenset([
        "true",
        "yes",
        "y",
        "t",
        "ok",
        "1",
        "on",
        "是",
        "对",
        "真",
        "對",
        "√",
    ])
    FALSE_SET: typing.FrozenSet[str] = frozenset([
        "false",
        "no",
        "n",
        "f",
        "0",
        "off",
        "否",
        "错",
        "假",
        "錯",
        "×",
    ])
    DEFAULT_TRUE_STRING: typing.Final[str] = "TRUE"
    DEFAULT_FALSE_STRING: typing.Final[str] = "FALSE"

    @classmethod
    def value_of(cls, val: Any) -> bool:
        """
        包装方法, 用于将值转换成布尔类型
        NOTE 底层依赖于 BasicConvertor.to_bool
        :param val: 待转换的值
        :return: 转换后的布尔值
        """
        return BasicConvertor.to_bool(val)

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
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
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
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
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
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
        :return: 'true', 'false'
        """
        return cls.to_string(
            value,
            cls.DEFAULT_TRUE_STRING,
            cls.DEFAULT_FALSE_STRING,
            strict_mode=strict_mode,
        )

    @classmethod
    def to_str_on_and_off(cls, value: bool, *, strict_mode: bool = True) -> str:
        """
        将boolean转换为字符串 'on' 或者 'off'.
        :param value: Boolean值
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
        :return: 'on', 'off'
        """
        return cls.to_string(value, "YES", "NO", strict_mode=strict_mode)

    @classmethod
    def to_str_yes_no(cls, value: bool, *, strict_mode: bool = True) -> str:
        """
        将boolean转换为字符串 'yes' 或者 'no'.
        :param value: Boolean值
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
        :return: 'yes', 'no'
        """
        return cls.to_string(value, "YES", "NO", strict_mode=strict_mode)

    @classmethod
    def to_string(
        cls, value: bool, true_str: str, false_str: str, *, strict_mode: bool = False
    ) -> str:
        """
        将boolean转换为字符串
        :param value: Boolean值
        :param true_str:
        :param false_str:
        :param strict_mode: 是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算, 否则会进行布尔运算
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
        对Boolean数组取与

        Parameters
        ----------
        values : typing.List[bool]
            待检测Boolean数组
        strict_mode : bool, optional
            是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算,否则会进行布尔运算, by default True

        Returns
        -------
        bool
            _description_

        Raises
        ------
        ValueError
            如果数组为空则抛出异常
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
        """
        对Boolean数组取或

        Example:
        ----------
        >>> BooleanUtil.or_all([True, False]) # True
        >>> BooleanUtil.or_all([True, True]) # True
        >>> BooleanUtil.or_all([True, False, True]) # True
        >>> BooleanUtil.or_all([False, False, False]) # False

        Parameters
        ----------
        values : typing.List[bool]
            待检测Boolean数组
        strict_mode : bool, optional
            是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算,否则会进行布尔运算, by default True

        Returns
        -------
        bool
            取值为真返回

        Raises
        ------
        ValueError
            如果数组为空则抛出异常
        """
        if SequenceUtil.is_empty(values):
            raise ValueError("Empty sequence")

        for flg in values:
            flg = cls._check_boolean_value(flg, strict_mode=strict_mode)
            if flg:
                return True

        return False

    @classmethod
    def xor(cls, *values, strict: bool = True) -> bool:
        """
        对Boolean数组取异或

        Example:
        ----------
        >>> BooleanUtil.xor(True, False) # True
        >>> BooleanUtil.xor(True, True) # False
        >>> BooleanUtil.xor(True, False, True) # False

        Parameters
        ----------
        values : typing.List[bool]
            待检测Boolean数组
        strict : bool, optional
            是否启动严格模式, 如果开启严格模式, 则不会使用BOOL进行布尔运算,否则会进行布尔运算, by default True

        Returns
        -------
        bool
            如果数组检测结果为真则返回

        Raises
        ------
            ValueError: 如果数组为空则抛出异常
        """
        if SequenceUtil.is_empty(values):
            raise ValueError("Empty sequence")
        result = False
        for flg in values:
            flg = cls._check_boolean_value(flg, strict_mode=strict)
            result = result ^ flg
        return result

    @classmethod
    def _check_boolean_value(cls, value: bool, *, strict_mode: bool = False) -> bool:
        if not isinstance(value, bool) and strict_mode:
            raise ValueError(f"{value} is not a boolean value")

        return bool(value)


class SequenceUtil(object):
    EMPTY: typing.Final[str] = ""
    SPACE: typing.Final[str] = " "

    @classmethod
    def is_empty(cls, sequence: typing.Sequence[Any]) -> bool:
        """
        返回序列是否为空。

        Example:
        >>> SequenceUtil.is_empty(None) # True
        >>> SequenceUtil.is_empty([]) # True
        >>> SequenceUtil.is_empty([1, 2, 3]) # False

        Parameters
        ----------
        sequence : typing.Sequence[Any]
            待检测序列

        Returns
        -------
        bool
            如果序列为空返回True, 否则返回False
        """
        return sequence is None or len(sequence) == 0

    @classmethod
    def is_not_empty(cls, sequence: typing.Sequence[Any]) -> bool:
        """
        返回序列是否为非空。\n
        NOTE 依赖于 is_empty 实现。

        :param sequence:
        :return:
        """
        return not cls.is_empty(sequence)

    @classmethod
    def reverse_sequence(cls, sequence: typing.Sequence[Any]) -> typing.Sequence:
        """
        翻转序列
        :param sequence: 待翻转序列
        :return: 翻转后的序列
        """
        return sequence[::-1]

    @classmethod
    def has_none(cls, sequence: typing.Sequence[Any]) -> bool:
        """
        返回序列是否含有None元素
        :param sequence: 待检测序列
        :return: 如果包含None则返回True, 否则返回False
        """
        for item in sequence:
            if item is None:
                return True
        return False

    @classmethod
    def get_length(cls, sequence: typing.Sequence[Any]) -> int:
        """
        返回序列长度

        Examples:
        ----------
        >>> SequenceUtil.get_length(None)
        ValueError: Invalid sequence
        >>> SequenceUtil.get_length([])
        0
        >>> SequenceUtil.get_length([1, 2, 3])
        3

        Parameters
        ----------
        sequence : typing.Sequence[Any]
            待检测序列

        Returns
        -------
        int
            序列长度

        Raises
        ------
        ValueError
            如果序列为None则抛出异常
        """
        if sequence is None or not isinstance(sequence, typing.Sequence):
            raise ValueError("Invalid sequence")
        return len(sequence)

    @classmethod
    def first_idx_of_none(cls, sequence: typing.Sequence[Any]) -> int:
        """
        返回第一个None元素的索引
        :param sequence: 待检测序列
        :return: 返回None的索引, 如果不存在返回-1
        """
        for i, item in enumerate(sequence):
            if item is None:
                return i

        return -1

    @classmethod
    def contains_any(cls, sequence: typing.Sequence[Any], *args) -> bool:
        """
        检查序列是否包含任意给定元素

        Example:
        ----------
        >>> SequenceUtil.contains_any([1, 2, 3], 2, 4) # True
        >>> SequenceUtil.contains_any([1, 2, 3], 4, 5) # False

        Parameters
        ----------
        sequence : typing.Sequence[Any]
            待检测序列
        args : Any
            任意数量的元素, 用于检测是否包含其中之一

        Returns
        -------
        bool
            如果包含args中的任意元素返回True, 否则返回False
        """
        # PERF 可能有更好的方案
        for i in args:
            if i in sequence:
                return True
        return False

    @classmethod
    def new_list(cls, capacity: int, fill_val: Any = None) -> typing.List[Any]:
        """
        根据给定容量创建列表

        Example:
        ----------
        >>> SequenceUtil.new_list(5, 0) # [0, 0, 0, 0, 0]
        >>> SequenceUtil.new_list(3) # [None, None, None]

        Parameters
        ----------
        capacity : int
            给定容量
        fill_val : Any, optional
            填充项的默认值, by default None

        Returns
        -------
        typing.List[Any]
            创建的列表
        """
        return [fill_val for _ in range(capacity)]

    @classmethod
    def set_or_append(cls, lst: typing.Sequence[Any], idx: int, value: Any) -> int:
        """
        插入或者尾部追加元素

        Example:
        ----------
        >>> lst = [1, 2, 3]
        ... SequenceUtil.set_or_append(lst, 4, 4) # 1
        ... lst # [1, 2, 3, 4]
        >>> lst = [1, 2, 3]
        ... SequenceUtil.set_or_append(lst, 1, 5) # 0
        ... lst # [1, 5, 3]

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待添加元素的序列
        idx : int
            添加元素的位置
        value : Any
            待添加的值

        Returns
        -------
        int
            返回序列操作前后的长度差
        """
        old_length = len(lst)
        if 0 <= idx < old_length:
            lst[idx] = value
        else:
            lst.append(value)

        return len(lst) - old_length

    @classmethod
    def resize(
        cls, lst: typing.Sequence[Any], new_length: int, *, fill_val: Any = None
    ) -> typing.Sequence[Any]:
        """
        调整序列的长度, 如果新长度小于原长度, 则截断, 如果新长度大于原长度, 则填充默认值。

        Example:
        ----------
        >>> lst = [1, 2, 3]
        ... SequenceUtil.resize(lst, 5, fill_val=0) # [1, 2, 3, 0, 0]
        >>> lst = [1, 2, 3]
        ... SequenceUtil.resize(lst, 2) # [1, 2]

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待调整的序列
        new_length : int
            新的长度
        fill_val : Any, optional
            填充项的默认值, by default None

        Returns
        -------
        typing.Sequence[Any]
            调整后新生成的序列, 长度为new_length,
        """

        if 0 > new_length:
            return [i for i in lst]

        if new_length <= len(lst):
            return [lst[i] for i in range(new_length)]

        diff_length = new_length - len(lst)
        return [i for i in lst] + cls.new_list(diff_length, fill_val)

    @classmethod
    def remove_none_item(cls, lst: typing.Sequence[Any]) -> typing.Sequence[Any]:
        """
        移除序列中所有的None元素

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待处理序列

        Returns
        -------
        typing.Sequence[Any]
            处理完成后新产生的序列
        """
        return [i for i in lst if i is not None]

    @classmethod
    def remove_false_item(cls, lst: typing.Sequence[Any]) -> typing.Sequence[Any]:
        """
        移除序列中所有的False元素

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待处理序列

        Returns
        -------
        typing.Sequence[Any]
            处理完成后新产生的序列

        Notes
        -------
        Extended summary follows.

        依赖于 `BooleanUtil#value_of()` 方法。
        """
        return [i for i in lst if BooleanUtil.value_of(i)]

    @classmethod
    def sub_lst(
        cls,
        lst: typing.Sequence[Any],
        start: int,
        end: int,
        *,
        include_last: bool = False,
    ) -> typing.Sequence[Any]:
        """
        从序列中获取子序列

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待切分序列
        start : int
            开始切分位置
        end : int
            结束切分位置
        include_last : bool, optional
            是否包含结束位置的元素, by default False

        Returns
        -------
        typing.Sequence[Any]
            切分后的子序列

        Raises
        ------
        ValueError
            如果开始位置大于结束位置、开始位置大于等于序列长度、开始位置小于0则抛出异常
        """
        if start < 0 or start > end or start >= len(lst):
            raise ValueError(f"Start index {start} is out of range")

        return lst[start : end + 1] if include_last else lst[start:end]

    @classmethod
    def get_item_by_idx(
        cls,
        lst: typing.Sequence[Any],
        idx: int,
        default: Any = None,
        *,
        raise_exception: bool = False,
    ) -> Any:
        """
        根据给定的索引返回元素

        Example:
        ----------
        >>> lst = [1, 2, 3]
        ... SequenceUtil.get_item_by_idx(lst, 1) # 2
        ... SequenceUtil.get_item_by_idx(lst, 4) # None
        ... SequenceUtil.get_item_by_idx(lst, 4, default=0) # 0

        Parameters
        ----------
        lst : typing.Sequence[Any]
            待提取序列
        idx : int
            给定的索引位置
        default : Any, optional
            提取默认值, by default None
        raise_exception : bool, optional
            当给定索引大于等于序列长度时是否抛出异常, by default False

        Returns
        -------
        Any
            提取的值

        Raises
        ------
        ValueError
            当索引小于0时抛出异常
        IndexError
            当给定索引大于等于序列长度时, 并且 raise_exception 为 True, 则抛出异常
        """
        seq_length = len(lst)
        if idx < 0:
            raise ValueError(f"Index {idx} is out of range")
        if idx >= seq_length:
            if raise_exception:
                raise IndexError(f"Index {idx} is out of range")
            else:
                return default
        return lst[idx]

    @classmethod
    def get_first_n_item_from_iter(
        cls, iterable: typing.Iterable[Any], n: int
    ) -> typing.Iterable[Any]:
        """
        从序列中获取前n个元素

        Example:
        ----------
        >>> lst = [1, 2, 3, 4, 5]
        ... SequenceUtil.get_first_n_item_from_iter(lst, 3) # [1, 2, 3]
        >>> d = {3: 4, 6: 2, 0: 9, 9: 0, 1: 4}
        ... SequenceUtil.get_first_n_item_from_iter(d.keys(), 3) # [(3, 4), (6, 2), (0, 9)]
        ... SequenceUtil.get_first_n_item_from_iter(d, 10) # [3, 6, 0, 9, 1]

        Parameters
        ----------
        iterable : typing.Sequence[Any]
            待提取序列
        n : int
            前n个元素

        Returns
        -------
        typing.Iterable[Any]
            前n个元素组成的序列

        Raises
        ------
        ValueError
            如果n小于0则抛出异常
        """
        if n < 0:
            raise ValueError(f"n should be greater than 0, but got {n}")

        return list(it.islice(iterable, n))

    @classmethod
    def get_first_match_item(
        iterable: typing.Iterable[Any],
        func: typing.Callable[[Any], bool],
        default_val: Any = None,
    ) -> Any:
        """
        从可迭代对象中返回第一个符合条件的元素

        Parameters
        ----------
        iterable : typing.Iterable[Any]
            待提取可迭代对象
        func : typing.Callable[[Any], bool]
            检测函数
        default_val : Any, optional
            返回默认值, by default None

        Returns
        -------
        Any
            第一个符合条件的对象
        """
        return next((i for i in iterable if func(i)), default_val)

    @classmethod
    def is_all_ele_equal(cls, iterable: typing.Iterable[Any]) -> bool:
        """
        判断序列中是否所有元素相等

        Example:
        ----------
        >>> SequenceUtil.is_all_ele_equal([1, 1, 1, 1]) # True
        >>> SequenceUtil.is_all_ele_equal([1, 2, 1, 1]) # False

        Parameters
        ----------
        iterable : typing.Iterable[Any]
            待检测序列

        Returns
        -------
        bool
            如果所有元素相等返回True, 否则返回False
        """
        g = it.groupby(iterable)
        return next(g, True) and not next(g, False)


class StringUtil(SequenceUtil):
    @classmethod
    def is_string(cls, obj: typing.Any, *, raise_type_exception: bool = False) -> bool:
        """
        检查对象是否是字符串

        *Example:*

        >>> assert is_string('foo') # returns true
        >>> assert not is_string(b'foo') # returns false

        :param obj: 待检测对象
        :param raise_type_exception: 类型错误的时候是否引发异常
        :return: 如果是字符串返回True, 否则返回False
        """
        if isinstance(obj, str):
            return True
        if raise_type_exception:
            raise TypeError(f"{obj} is not a string")
        return False

    @classmethod
    def is_blank(
        cls, s: typing.Optional[str], *, raise_type_exception: bool = False
    ) -> bool:
        """
        判断给定的字符串是否为空, 空字符串包括null、空字符串: ""、空格、全角空格、制表符、换行符, 等不可见字符, \\n

        Parameters
        ----------
        s : typing.Optional[str]
            待检测的字符串
        raise_type_exception : bool, optional
            如果类型错误, 是否要抛出异常, by default False

        Returns
        -------
        bool
            如果字符串为空返回True, 否则返回False

        Raises
        ------
        TypeError
            如果类型错误, 并且 raise_type_exception 为 True, 则抛出异常
        """
        if s is None:
            return True
        if not cls.is_string(s, raise_type_exception=raise_type_exception):
            return False

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
        :param raise_type_exception: 如果类型错误, 是否要抛出异常
        :return: 如果字符串为非空返回True, 否则返回False
        """
        return not cls.is_blank(s, raise_type_exception=raise_type_exception)

    @classmethod
    def has_blank(cls, *args) -> bool:
        """
        判断多个字符串中是否有空白字符串
        :param args: 待判断字符串
        :return: 如果有空白字符串返回True, 否则返回False
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
        :return: 如果都为空则返回True, 否则返回False
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
        当给定字符串为null时, 转换为Empty
        :param s: 待检测字符串
        :return: 转换后的字符串
        """
        return cls.none_to_default(s, cls.EMPTY)

    @classmethod
    def none_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是 null, 则返回指定默认字符串, 否则返回字符串本身。
        :param s: 要转换的字符串
        :param default_str: 默认字符串
        :return: 如果字符串是 null, 则返回指定默认字符串, 否则返回字符串本身。
        """
        return default_str if s is None else s

    @classmethod
    def empty_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是null或者"", 则返回指定默认字符串, 否则返回字符串本身。
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
        当给定字符串为空字符串时, 转换为null
        :param s: 被转换的字符串
        :return: 转换后的字符串
        """
        return None if cls.is_empty(s) else s

    @classmethod
    def blank_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是null或者""或者空白, 则返回指定默认字符串, 否则返回字符串本身。
        :param s: 要转换的字符串
        :param default_str: 默认字符串
        :return: 转换后的字符串
        """
        if cls.is_blank(s):
            return default_str
        else:
            return s

    @classmethod
    def to_bytes(
        cls, byte_or_str: typing.Union[bytes, str], encoding=CharsetUtil.UTF_8
    ) -> bytes:
        """
        将字节序列或者字符串转换成字节序列
        :param byte_or_str: 待转换对象
        :param encoding: 编码方式
        :return: 如果是bytes序列则返回自身, 否则编码后返回
        """
        assert isinstance(byte_or_str, bytes) or isinstance(byte_or_str, str)
        if isinstance(byte_or_str, bytes):
            return byte_or_str
        else:
            return byte_or_str.encode(encoding)

    @classmethod
    def to_str(
        cls, byte_or_str: typing.Union[bytes, str], encoding=CharsetUtil.UTF_8
    ) -> str:
        """
        将字节序列或者字符串转换成字符串
        :param byte_or_str: 待转换对象
        :param encoding: 解码方式
        :return: 如果是字符串则返回自身, 否则解码后返回
        """
        assert isinstance(byte_or_str, bytes) or isinstance(byte_or_str, str)
        if isinstance(byte_or_str, str):
            return byte_or_str
        else:
            return byte_or_str.decode(encoding)

    @classmethod
    def fill_before(cls, s: str, fill_char: str, length: int) -> str:
        """
        将已有字符串填充为规定长度, 如果已有字符串超过这个长度则返回这个字符串。

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
        获取打印信息, 信息左右两侧由指定字符填充

        *Example:*

        >>> StringUtil.get_center_msg("hello world", "=", 40) # ==== hello world ====
        >>> StringUtil.get_center_msg("hello world", "=", 1) # hello world

        :param s: 被填充的字符串
        :param fill_char: 填充的字符
        :param length:
        :return: 填充后的字符串
        """
        single_side_width = length // 2
        return f" {s} ".center(single_side_width, fill_char)

    @classmethod
    def equals(
        cls,
        s1: str,
        s2: str,
        *,
        case_insensitive: bool = True,
        strict_mode: bool = False,
    ) -> bool:
        """

        :param s1:
        :param s2:
        :param case_insensitive:
        :param strict_mode:
        :return:
        """
        if strict_mode:
            return s1 == s2
        if case_insensitive:
            return s1.strip().lower() == s2.strip().lower()
        else:
            return s1.strip() == s2.strip()

    @classmethod
    def hide(cls, s: str, start: int, end: int, replace_char: str = "*") -> str:
        """
         隐藏字符串 s 中从 start 到 end 位置的字符, 用指定的替换字符 replace_char 替换。

        *Example*

        >>> StringUtil.hide("1234567890", 3, 6) # '123***7890'
        >>> StringUtil.hide("1234567890", 0, 4, "#") # '####567890'

        :param s: 输入的字符串。
        :param start: 开始替换的位置（包含）。
        :param end: 结束替换的位置（不包含）。
        :param replace_char: 用于替换的字符, 默认为 '*'。
        :return: 替换后的字符串, 其中从 start 到 end 的字符被替换为 replace_char。
        """
        if cls.is_blank(s):
            return s

        if start > len(s):
            return s

        if end >= len(s):
            end = len(s)

        new_str_lst = []
        for i, v in enumerate(s):
            if start <= i < end:
                new_str_lst.append(replace_char)
            else:
                new_str_lst.append(v)

        return "".join(new_str_lst)

    @classmethod
    def is_startswith(
        cls,
        s: str,
        prefix: str,
        *,
        case_insensitive: bool = True,
        strict_mode: bool = False,
    ) -> bool:
        """
        检查字符串 s 是否以指定的前缀 prefix 开头。

        :param s: 输入的字符串。
        :param prefix: 要检查的前缀。
        :param case_insensitive: 是否忽略大小写进行检查, 默认为 True。
        :param strict_mode: 严格模式下, 不会对待测试字符串和前缀进行任何处理, 默认False
        :return: 如果 s 以 prefix 开头, 则返回 True；否则返回 False。
        """

        if strict_mode:
            return s.startswith(prefix)

        if case_insensitive:
            return s.lower().strip().startswith(prefix.lower().strip())

        return s.strip().startswith(prefix.strip())

    @classmethod
    def get_random_strs(cls, n, *, chars: typing.Optional[str] = None) -> str:
        """
        返回给定个数的随机字符串
        :param n: 字符数量
        :param chars: 源字符串
        :return: 随机字符串
        """
        if chars is None:
            chars = string.ascii_letters + string.digits

        return "".join(RandomUtil.get_random_items_from_sequence(chars, n))

    @classmethod
    def get_random_chinese(cls) -> str:
        """
        获取随机中文字符串

        Returns
        -------
        str
            随机中文字符串
        """
        random_val = RandomUtil.get_random_val_from_range(0x4E00, 0x9FA5)
        return chr(random_val)


class DatetimeUtil(object):
    wtb = [
        "sun",
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "gmt",
        "ut",
        "utc",
        "est",
        "edt",
        "cst",
        "cdt",
        "mst",
        "mdt",
        "pst",
        "pdt",
    ]

    @classmethod
    def this_year(cls) -> int:
        """
        返回当前年份
        :return: 当前年份
        """
        return datetime.now().year

    @classmethod
    def this_quarter(cls) -> int:
        """

        :return:
        """
        dt = datetime.now()
        quarter = Quarter.get_quarter(dt)
        return quarter.value.val

    @classmethod
    def this_month(cls) -> int:
        """
        返回当前月份
        :return: 当前月份
        """
        return datetime.now().month

    @classmethod
    def this_day(cls) -> int:
        """
        返回当前天
        :return: 当前天
        """
        return datetime.now().day

    @classmethod
    def this_hour(cls) -> int:
        """
        返回当前小时
        :return: 当前小时
        """
        return datetime.now().hour

    @classmethod
    def this_minute(cls) -> int:
        """
        返回当前分钟数
        :return: 当前分钟
        """
        return datetime.now().minute

    @classmethod
    def this_second(cls) -> int:
        """
        返回当前分钟数
        :return: 当前分钟
        """
        return datetime.now().second

    @classmethod
    def this_millisecond(cls) -> int:
        """

        :return:
        """
        datetime.now

        raise NotImplementedError()

    @classmethod
    def this_ts(cls) -> float:
        """

        :return:
        """
        return datetime.now().timestamp()

    @classmethod
    def is_leap_year(cls, year: int) -> bool:
        """
        判断给定年份是否是闰年, 闰年是指年份不能被4整除或者 \n
        年份能被100整除但不能被400整除
        :param year: 待检测年份
        :return: 是否是闰年
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @classmethod
    def is_same_year(cls, date1: date, date2: date) -> bool:
        """
        检查给定的两个对象是否是同一年
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一年
        """
        if date1 is None or date2 is None:
            return False
        return date1.year == date2.year

    @classmethod
    def is_same_quarter(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一个季度
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否在同一个季度
        """
        q1 = Quarter.get_quarter(date1)
        q2 = Quarter.get_quarter(date2)

        return date1.year == date2.year and q1 == q2

    @classmethod
    def is_same_month(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一个月
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一个月
        """
        if date1 is None or date2 is None:
            return False
        return cls.is_same_year(date1, date2) and date1.month == date2.month

    @classmethod
    def is_same_week(cls, date1: datetime, date2: datetime) -> bool:
        """
        检查给定的两个日期是否是同一周
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return:是否在同一周
        """
        _, week_num1, _ = date1.isocalendar()
        _, week_num2, _ = date2.isocalendar()
        return cls.is_same_year(date1, date2) and week_num1 == week_num2

    @classmethod
    def is_same_day(cls, date1, date2) -> bool:
        """
        检查给定的两个日期是否是同一个天
        :param date1: 待检测日期1
        :param date2: 待检测日期2
        :return: 是否是同一天
        """
        if date1 is None or date2 is None:
            return False

        return cls.is_same_month(date1, date2) and date1.day == date2.day

    @classmethod
    def get_random_tz(cls) -> tzinfo:
        """
        获取随机时区
        :return: 随机时区
        """
        timezones = pytz.all_timezones

        random_tz = RandomUtil.get_random_item_from_sequence(timezones)
        return pytz.timezone(random_tz)

    @classmethod
    def get_local_tz(cls) -> timezone:
        """
        获取默认时区
        :return: timezone实例
        """
        if time.daylight != 0:
            offset_seconds = time.altzone
        else:
            offset_seconds = time.timezone

        tz = timezone(timedelta(seconds=offset_seconds))
        return tz

    @classmethod
    def get_random_date(
        cls, start: typing.Optional[date] = None, end: typing.Optional[date] = None
    ) -> date:
        """
        返回随机日期

        *Example*

        >>> cls.get_random_date(date(1998, 4, 24)) # 2014-12-05
        >>> cls.get_random_date(date(1998, 4, 24)) # 2012-05-24
        >>> cls.get_random_date(date(1998, 4, 24)) # 1998-08-25

        :param start: 开始日期
        :param end: 结束日期
        :return: 随机日期
        """
        if start is not None and end is not None and end <= start:
            raise ValueError(f"{start} must be less than {end}")
        if start is None:
            start = date(1900, 1, 1)
        if end is None:
            end = date.today()

        days_between = (end - start).days
        random_num_of_days = RandomUtil.get_random_val_from_range(0, days_between)
        random_date = start + timedelta(days=random_num_of_days)
        return random_date

    @classmethod
    def get_random_datetime(
        cls,
        start: typing.Optional[datetime] = None,
        end: typing.Optional[datetime] = None,
        *,
        random_tz: bool = False,
    ) -> datetime:
        """
        生成一个随机的 datetime 对象, 支持指定时间范围和随机时区。

        *Example*

        >>> cls.get_random_datetime(random_tz=True) # datetime.datetime(1947, 12, 21, 9, 9, 39, tzinfo=<DstTzInfo 'Kwajalein' LMT+11:09:00 STD>)
        >>> cls.get_random_datetime() # datetime.datetime(1981, 7, 28, 13, 14, 35)
        >>> cls.get_random_datetime(random_tz=False) # datetime.datetime(1947, 12, 21, 9, 9, 39)

        :param start: 随机日期时间的开始范围
        :param end: 随机日期时间的结束范围。
        :param random_tz: 是否生成带有随机时区信息的 datetime 对象。如果为 True, 则生成带有随机时区的 datetime 对象。
        :return: 随机 datetime 对象
        """

        # NOTE 获取随机Date对象, 依赖于 get_random_date 方法
        start_date = start.date() if start is not None else start
        end_date = end.date() if end is not None else end
        random_date = cls.get_random_date(start_date, end_date)
        random_datetime = datetime.combine(random_date, datetime.min.time())

        # 获取时间部分随机值
        random_hour = RandomUtil.get_random_val_from_range(0, 24)
        random_minute = RandomUtil.get_random_val_from_range(0, 60)
        random_second = RandomUtil.get_random_val_from_range(0, 60)

        # 拼接 datetime 对象
        random_datetime = random_datetime.replace(
            hour=random_hour, minute=random_minute, second=random_second
        )
        if random_tz:
            tz_info = cls.get_random_tz()
            random_datetime = random_datetime.replace(tzinfo=tz_info)

        return random_datetime

    @classmethod
    def sleep(cls, seconds: float) -> None:
        """
        更加精确的Sleep方法
        :param seconds: 要睡眠的时间, 单位秒
        :return: None
        """
        start = time.time()
        seconds = seconds * (datetime.resolution * 1e6).seconds
        left = seconds
        while True:
            time.sleep(left)
            left = seconds - (time.time() - start)
            if left <= 0:
                break

    @classmethod
    def utc_now(cls) -> datetime:
        """
        获取当前 UTC 时间
        :return: 表示当前 UTC 时间的 datetime 对象
        """
        return datetime.now(pytz.UTC)

    @classmethod
    def local_to_utc(cls, date_obj: datetime) -> datetime:
        """
        当前时间转UTC时间
        :param date_obj: 待转换的 Datetime 对象
        :return: 表示UTC时间的 Datetime 对象
        """
        if not isinstance(date_obj, datetime):
            raise TypeError(f"date_obj must be datetime.datetime, not {type(date_obj)}")
        return date_obj.astimezone(pytz.timezone("UTC"))

    @classmethod
    def utc_to_local(cls, date_obj: datetime, tz: str) -> datetime:
        """
        UTC 时间转指定时区时间
        :param date_obj: 待转换的 Datetime 对象, 表示一个 UTC 时间
        :param tz: 指定的时区
        :return: 转换后的 Datetime 对象
        """
        if not isinstance(date_obj, datetime):
            raise TypeError(f"date_obj must be datetime.datetime, not {type(date_obj)}")

        return date_obj.astimezone(pytz.timezone(tz))

    @classmethod
    def days_in_month(cls, year: int, month: int) -> int:
        """
        获取指定年份指定月多少天
        :param year: 指定年份
        :param month: 指定月
        :return: 该月一共多少天
        """
        assert 1 <= month <= 12, month
        _, days_in_month = calendar.monthrange(year, month)
        return days_in_month

    @classmethod
    def get_age(
        cls, birthday: datetime, *, use_float_format: bool = False
    ) -> typing.Union[int, float]:
        """
        根据给定生日返回年龄
        :param birthday: 给定生日
        :param use_float_format: 是否采用浮点数显示
        :return: 年龄
        """
        if birthday is None:
            raise ValueError("birthday cannot be None")

        now = datetime.now() + timedelta(days=1)
        if use_float_format:
            sub_days = (now - birthday).days
            age = round(sub_days / 365, 1)
            return age

        age = now.year - birthday.year

        # NOTE 根据月、日判断是否对年龄 -1
        # ISSUE-1, 如果生日是闰年2-29, 则构建datetime对象时报错。
        # 这里的问题是如果是闰年，会出现2月29日，那么使用 9999-02-29 构建 datetime 对象会报错
        # 改为单独对月和日进行判断，不再构建datetime对象
        # birth_dt_with_fix_year = datetime(9999, birthday.month, birthday.day)
        # now_dt_with_fix_year = datetime(9999, now.month, now.day)

        if birthday.month > now.month or (
            birthday.month == now.month and birthday.day > now.day
        ):
            age -= 1

        return age

    @classmethod
    def nanos_to_seconds(cls, duration: int) -> float:
        """
        纳秒转秒
        :param duration: 时长
        :return: 秒
        """
        return TimeUnit.convert(duration, TimeUnit.NANOSECONDS, TimeUnit.SECONDS)

    @classmethod
    def nanos_to_millis(cls, duration: int) -> float:
        """
        纳秒转毫秒
        :param duration: 时长
        :return: 毫秒
        """
        return TimeUnit.convert(duration, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS)

    @classmethod
    def second_to_time(cls, seconds: int) -> str:
        """
        秒数转为时间格式(HH:mm:ss)
        :param seconds: 需要转换的秒数
        :return: 转换后的字符串
        """
        # PERF 取余符号效率低, 应该优化
        # PERF 1 使用整除代替除法
        hour = seconds // 3600
        other = seconds % 3600
        minute = other / 60
        seconds = other % 60

        res_dt = datetime.now() + timedelta(hours=hour, minutes=minute, seconds=seconds)
        return res_dt.strftime("%H:%M:%S")


class RadixUtil(object):
    ZERO = "0"

    @classmethod
    def convert_base(
        cls, num: typing.Union[int, str], from_base: int, to_base: int
    ) -> str:
        """
        进制转换

        Parameters
        ----------
        num : typing.Union[int, str]
            要转换的数据
        from_base : int
            初始进制
        to_base : int
            目标进制

        Returns
        -------
        str
            转换后的字符串
        """

        def to_decimal(num: typing.Union[int, str], from_base: int) -> int:
            if isinstance(num, int):
                return num
            return int(num, base=from_base)

        def from_decimal(num: int, base: int) -> str:
            if num == 0:
                return cls.ZERO
            digits = []
            while num:
                digits.append(str(num % base))
                num //= base
            # PERF 倒转字符串效率低, 应该优化
            digits.reverse()
            return "".join(
                map(lambda x: str(x) if int(x) < 10 else chr(int(x) + 55), digits)
            )

        decimal_val = to_decimal(num, from_base)
        return from_decimal(decimal_val, to_base)
