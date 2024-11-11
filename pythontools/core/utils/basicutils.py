#!/usr/bin/env python
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

import binascii
import calendar
import datetime as dt_lib
import itertools as it
import os
import random
import re
import string
import sys
import time
import typing as t
import unicodedata
from collections.abc import Generator, Mapping, Sequence, Set
from datetime import date, datetime, timedelta, tzinfo
from decimal import Decimal

import pytz
from loguru import logger

from pythontools.core.__typing import K, T
from pythontools.core.constants.datetime_constant import Month, Quarter, TimeUnit, Week
from pythontools.core.constants.pattern_pool import PatternPool, RegexPool
from pythontools.core.constants.string_constant import CharPool, CharsetUtil
from pythontools.core.decorator import UnCheckFunction
from pythontools.core.errors import RegexValidationError, UnsupportedDateType
from pythontools.date.relativedelta import relativedelta


class BooleanUtil:
    TRUE_SET: frozenset[str] = frozenset(
        [
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
        ]
    )
    FALSE_SET: frozenset[str] = frozenset(
        [
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
        ]
    )
    DEFAULT_EN_TRUE_STR: t.Final[str] = "TRUE"
    DEFAULT_EN_FALSE_STR: t.Final[str] = "FALSE"
    DEFAULT_CN_TRUE_STR: t.Final[str] = "是"
    DEFAULT_CN_FALSE_STR: t.Final[str] = "否"

    @classmethod
    def to_bool_default_if_none(
        cls,
        val: bool | None,
        default: bool = False,
    ) -> bool:
        """
        给定一个值, 如果值是None, 则返回默认值, 否则返回布尔值

        Example:
        ----------
        >>> BooleanUtil.to_bool_default_if_none(None, False)
        False
        >>> BooleanUtil.to_bool_default_if_none(True)
        True
        >>> BooleanUtil.to_bool_default_if_none(False)
        False

        Parameters
        ----------
        value : bool | None
            待检测值
        default_val : bool, optional
            默认布尔值, by default False

        Returns
        -------
        bool
            如果值是None, 则返回默认值, 否则返回布尔值
        """
        return val if val is not None else default

    @classmethod
    def value_of(cls, val: T) -> bool:
        """
        将给定值转换成布尔值

        Parameters
        ----------
        val : Any
            待转换值

        Returns
        -------
        bool
            转换后的布尔值
        """
        return cls._get_bool_from_val(val)

    @classmethod
    def is_true(cls, val: T) -> bool:
        """
        判断给定的值是否为真

        Parameters
        ----------
        val : Any
            待检测值

        Returns
        -------
        bool
            如果值是真, 则返回True, 否则返回False
        """
        return cls._get_bool_from_val(val)

    @classmethod
    def is_false(cls, val: T) -> bool:
        """
        判断给定的值布尔计算是否为假

        Parameters
        ----------
        val : Any
            待判断的值

        Returns
        -------
        bool
            计算结果
        """
        return not cls._get_bool_from_val(val)

    @classmethod
    def negate(
        cls,
        state: T,
    ) -> bool:
        """
        对值取反

        Parameters
        ----------
        state : Any
            待取反值，不一定是布尔类型，函数内部会做布尔计算的

        Returns
        -------
        bool
            取反结果
        """
        if not isinstance(state, bool):
            state = cls.value_of(state)
        return not state

    @classmethod
    def str_to_boolean(cls, expr: str) -> bool:
        """
        将字符串转换为布尔值

        Parameters
        ----------
        expr : str
            待转换字符串

        Returns
        -------
        bool
            转换后的布尔值

        Raises
        ------
        ValueError
            如果字符串无法转换成布尔值则抛出异常
        """
        if StringUtil.is_blank(expr):
            return False

        expr = expr.strip().lower()
        true_flg = expr in cls.TRUE_SET
        false_flg = expr in cls.FALSE_SET

        if true_flg or false_flg:
            return not false_flg
        else:
            raise ValueError(f"{expr} is not a boolean value")

    @classmethod
    def boolean_to_str(cls, state: bool) -> str:
        """
        将布尔值转换为字符串

        Parameters
        ----------
        state : bool
            待转换布尔值

        Returns
        -------
        str
            转换后的字符串
        """
        return cls.to_string(state, cls.DEFAULT_EN_TRUE_STR, cls.DEFAULT_EN_FALSE_STR)

    @classmethod
    def number_to_boolean(cls, val: int) -> bool:
        """
        将整数值转换成布尔值

        Parameters
        ----------
        val : int
            待转换整数值

        Returns
        -------
        bool
            转换后的布尔值
        """
        if not isinstance(val, int | float):
            raise ValueError(f"{val} is not a integer value")
        return val != 0

    @classmethod
    def boolean_to_number(cls, state: bool) -> int:
        """
        将布尔值转换成整数

        Parameters
        ----------
        value : bool
            待转换布尔值

        Returns
        -------
        int
            转换后的整数值

        Raises
        ------
        ValueError
            如果布尔值无法转换成整数则抛出异常
        """
        if not isinstance(state, bool):
            raise ValueError(f"{state} is not a boolean value")

        return 1 if state else 0

    @classmethod
    def to_str_on_and_off(
        cls,
        state: bool,
    ) -> str:
        """
        将boolean转换为字符串 'on' 或者 'off'.

        Parameters
        ----------
        value : bool
            待转换布尔值

        Returns
        -------
        str
            如果布尔值为True, 则返回 'ON', 否则返回 'OFF'
        """
        return cls.to_string(
            state,
            "ON",
            "OFF",
        )

    @classmethod
    def to_str_yes_and_no(
        cls,
        state: bool,
    ) -> str:
        """
        将boolean转换为字符串 'yes' 或者 'no'.

        Parameters
        ----------
        value : bool
            待转换布尔值

        Returns
        -------
        str
            如果布尔值为True, 则返回 'YES', 否则返回 'NO'
        """
        return cls.to_string(
            state,
            "YES",
            "NO",
        )

    @classmethod
    def to_chinese_str(
        cls,
        state: bool,
    ) -> str:
        """
        将给定布尔值转换为“是”或者“否”

        Parameters
        ----------
        value : bool
            待转换布尔值

        Returns
        -------
        str
            如果布尔值为True, 则返回 '是', 否则返回 '否'
        """
        return cls.to_string(
            state,
            cls.DEFAULT_CN_TRUE_STR,
            cls.DEFAULT_CN_FALSE_STR,
        )

    @classmethod
    def to_string(
        cls,
        value: bool,
        true_expr: str,
        false_expr: str,
    ) -> str:
        """
        将布尔值转换成给定的字符串

        Parameters
        ----------
        value : bool
            待转换布尔值
        true_str : str
            如果布尔值为True, 返回的字符串
        false_str : str
            如果布尔值为False, 返回的字符串

        Returns
        -------
        str
            如果布尔值为True, 则返回true_str, 否则返回false_str
        """
        value = cls._get_bool_from_val(value)

        if StringUtil.is_blank(true_expr):
            true_expr = cls.DEFAULT_EN_TRUE_STR
        if StringUtil.is_blank(false_expr):
            false_expr = cls.DEFAULT_EN_FALSE_STR

        return true_expr if value else false_expr

    @classmethod
    def and_all(cls, *values) -> bool:
        """
        对Boolean数组取与

        Parameters
        ----------
        values : t.List[bool]
            待检测Boolean数组


        Returns
        -------
        bool


        Raises
        ------
        ValueError
            _description_
        """
        if SequenceUtil.is_empty(values):
            raise ValueError("Empty sequence")

        return all(values)

    @classmethod
    def or_all(cls, *values) -> bool:
        """
        对Boolean数组取或

        Example:
        ----------
        >>> BooleanUtil.or_all([True, False])
        True
        >>> BooleanUtil.or_all([True, True])
        True
        >>> BooleanUtil.or_all([True, False, True])
        True
        >>> BooleanUtil.or_all([False, False, False])
        False

        Parameters
        ----------
        values : t.List[bool]
            待检测Boolean数组

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

        return any(values)

    @classmethod
    def xor_all(cls, *values) -> bool:
        """
        对Boolean数组取异或

        Example:
        ----------
        >>> BooleanUtil.xor(True, False) # True
        >>> BooleanUtil.xor(True, True) # False
        >>> BooleanUtil.xor(True, False, True) # False

        Parameters
        ----------
        values : t.List[bool]
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
        result = SequenceUtil.get_element(values, 0)
        for state in values[1:]:
            state = cls._get_bool_from_val(state)
            result = result ^ state
        return result

    @classmethod
    def _get_bool_from_val(cls, value: T) -> bool:
        return bool(value)


class SequenceUtil:
    EMPTY: t.Final[str] = CharPool.EMPTY
    SPACE: t.Final[str] = CharPool.SPACE
    INDEX_NOT_FOUND: t.Final[int] = -1

    @classmethod
    def is_empty(cls, sequence: t.Sequence[T]) -> bool:
        """
        返回序列是否为空。

        Example:
        >>> SequenceUtil.is_empty(None) # True
        >>> SequenceUtil.is_empty([]) # True
        >>> SequenceUtil.is_empty([1, 2, 3]) # False

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列

        Returns
        -------
        bool
            如果序列为空返回True, 否则返回False
        """
        return sequence is None or len(sequence) == 0

    @classmethod
    def is_not_empty(cls, sequence: t.Sequence[T]) -> bool:
        """
        返回序列是否为非空

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列

        Returns
        -------
        bool
            如果序列为非空返回True, 否则返回False
        """
        return not cls.is_empty(sequence)

    @classmethod
    def is_sub_equal(
        cls,
        main_seq: Sequence[T],
        start_idx: int,
        sub_seq: Sequence[T],
        sub_start_idx: int,
        split_length: int,
    ) -> bool:
        """
        截取两个字符串的不同部分（长度一致），判断截取的子串是否相同 任意一个字符串为null返回false

        Parameters
        ----------
        main_seq : Sequence[Any]
            主要序列
        start_idx : int
            主要序列的起始位置
        sub_seq : Sequence[Any]
            次要序列
        sub_start_idx : int
            次要序列的起始位置
        split_length : int
            截取长度

        Returns
        -------
        bool
            子序列是否相同
        """
        if cls.is_empty(main_seq) or cls.is_empty(sub_seq):
            return False

        main_seq_len = len(main_seq)
        sub_seq_len = len(sub_seq)
        if start_idx < 0 or sub_start_idx < 0:
            return False

        if main_seq_len < start_idx + split_length or sub_seq_len < sub_start_idx + split_length:
            return False

        main_split_seq = main_seq[start_idx : start_idx + split_length]
        sub_split_seq = sub_seq[sub_start_idx : sub_start_idx + split_length]

        return all(i == j for i, j in zip(main_split_seq, sub_split_seq))

    @classmethod
    def is_sorted(
        cls,
        sequence: t.Sequence[T],
        key_selector: t.Callable[
            [T],
            K,
        ] = None,
    ) -> bool:
        """
        判断序列是否有序

        Parameters
        ----------
        sequence : t.Sequence[T]
            待检测序列
        key_selector : t.Callable[[T], K], optional
            排序的key, by default None

        Returns
        -------
        bool
            如果序列有序返回True, 否则返回False
        """
        if key_selector is None:
            key_selector = lambda x: x

        return all(key_selector(sequence[i]) <= key_selector(sequence[i + 1]) for i in range(len(sequence) - 1))

    @classmethod
    def reverse_sequence(cls, sequence: t.Sequence[T]) -> t.Sequence:
        """
        翻转序列
        :param sequence: 待翻转序列
        :return: 翻转后的序列
        """
        return sequence[::-1]

    @classmethod
    def has_none(cls, sequence: t.Sequence[T]) -> bool:
        """
        返回序列是否含有None元素
        :param sequence: 待检测序列
        :return: 如果包含None则返回True, 否则返回False
        """
        return any(item is None for item in sequence)

    @classmethod
    def get_element(cls, seq: t.Sequence[T], idx: int) -> T:
        return seq[idx] if idx < len(seq) else None

    @classmethod
    def get_length(cls, sequence: t.Sequence[T]) -> int:
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
        sequence : t.Sequence[Any]
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
        if sequence is None or not isinstance(sequence, t.Sequence):
            raise ValueError(f"Invalid sequence, {sequence}")
        return len(sequence)

    @classmethod
    def first_idx_of_none(cls, sequence: t.Sequence[T]) -> int:
        """
        返回序列中第一个None元素的索引

        Parameters
        ----------
        sequence : t.Sequence[T]
            待检测序列

        Returns
        -------
        int
            如果序列中不存在None元素, 则返回-1，否则返回第一个None元素的索引
        """

        return cls.first_index_of(sequence, 0, None)

    @classmethod
    def last_idx_of_none(cls, sequence: t.Sequence[T]) -> int:
        """
        返回序列中最后一个None元素的索引

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列

        Returns
        -------
        int
            最后一个None元素的索引位置
        """
        return cls.last_index_of(sequence, -1, None)

    @classmethod
    def first_index_of(
        cls,
        sequence: t.Sequence[T],
        from_idx: int,
        value: T,
    ) -> int:
        """
        寻找序列中第一个指定元素的索引

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列
        value : Any
            待查找元素
        from_idx : int
            查找起始索引

        Returns
        -------
        int
            如果
        """
        if cls.is_empty(sequence):
            return cls.INDEX_NOT_FOUND
        try:
            idx = sequence.index(value, from_idx)
        except ValueError:
            return cls.INDEX_NOT_FOUND
        return idx

    @classmethod
    def last_index_of(
        cls,
        sequence: Sequence[T],
        from_idx: int,
        value: T,
    ) -> int:
        """
        寻找序列中最后一个指定元素的索引

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列
        value : Any
            待查找元素

        Returns
        -------
        int
            如果存在则返回索引, 否则返回-1
        """
        if cls.is_empty(sequence):
            return cls.INDEX_NOT_FOUND

        length = len(sequence)
        # 计算倒序后的起始索引
        if from_idx == 0:
            from_idx = length - 1
        else:
            from_idx = length - abs(from_idx) if from_idx < 0 else from_idx

        return next(
            (i for i in range(from_idx, -1, -1) if sequence[i] == value),
            cls.INDEX_NOT_FOUND,
        )

    @classmethod
    def contains_any(
        cls,
        sequence: t.Sequence[T],
        *args,
    ) -> bool:
        """
        检查序列是否包含任意给定元素

        Example:
        ----------
        >>> SequenceUtil.contains_any([1, 2, 3], 2, 4) # True
        >>> SequenceUtil.contains_any([1, 2, 3], 4, 5) # False

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列
        args : Any
            任意数量的元素, 用于检测是否包含其中之一

        Returns
        -------
        bool
            如果包含args中的任意元素返回True, 否则返回False
        """
        return any(i in sequence for i in args)

    @classmethod
    def new_list(
        cls,
        capacity: int,
        fill_val: T = None,
    ) -> list[T]:
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
        t.List[Any]
            创建的列表
        """
        return [fill_val for _ in range(capacity)]

    @classmethod
    def set_or_append(
        cls,
        lst: t.Sequence[T],
        idx: int,
        value: T,
    ) -> Sequence[T]:
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
        lst : t.Sequence[Any]
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
        tmp = list(lst)
        if 0 <= idx < len(lst):
            tmp[idx] = value
            return tmp

        if idx < 0:
            tmp = [value] + tmp
        else:
            tmp.append(value)

        return tmp

    @classmethod
    def resize(
        cls,
        seq: t.Sequence[T],
        new_length: int,
        *,
        fill_val: T = None,
    ) -> t.Sequence[T]:
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
        lst : t.Sequence[Any]
            待调整的序列
        new_length : int
            新的长度
        fill_val : Any, optional
            填充项的默认值, by default None

        Returns
        -------
        t.Sequence[Any]
            调整后新生成的序列, 长度为new_length,
        """

        if new_length < 0:
            return list(seq)

        if new_length <= len(seq):
            return [seq[i] for i in range(new_length)]

        diff_length = new_length - len(seq)
        return list(seq) + cls.new_list(diff_length, fill_val)

    @classmethod
    def remove_none_item(
        cls,
        seq: t.Sequence[T],
    ) -> t.Sequence[T]:
        """
        移除序列中所有的None元素

        Parameters
        ----------
        seq : t.Sequence[Any]
            待处理序列

        Returns
        -------
        t.Sequence[Any]
            处理完成后新产生的序列
        """
        return [i for i in seq if i is not None]

    @classmethod
    def remove_false_item(cls, lst: t.Sequence[T]) -> t.Sequence[T]:
        """
        移除序列中所有的False元素

        Parameters
        ----------
        lst : t.Sequence[Any]
            待处理序列

        Returns
        -------
        t.Sequence[Any]
            处理完成后新产生的序列

        Notes
        -------
        Extended summary follows.

        依赖于 `BooleanUtil#value_of()` 方法。
        """
        return [i for i in lst if BooleanUtil.value_of(i)]

    @classmethod
    def sub_sequence(
        cls,
        lst: t.Sequence[T],
        start: int,
        end: int | None = None,
        *,
        include_last: bool = False,
    ) -> t.Sequence[T]:
        """
        从序列中获取子序列

        Parameters
        ----------
        lst : t.Sequence[Any]
            待切分序列
        start : int
            开始切分位置
        end : int
            结束切分位置
        include_last : bool, optional
            是否包含结束位置的元素, by default False

        Returns
        --------
        t.Sequence[Any]
            切分后的子序列

        Raises
        ------
        ValueError
            如果开始位置大于结束位置、开始位置大于等于序列长度、开始位置小于0则抛出异常
        """
        if end is None:
            end = cls.get_length(lst)
        if start < 0 or start > end or start >= len(lst):
            raise ValueError(f"Start index {start} is out of range")

        if start == end:
            return [lst[start]] if include_last else []

        return lst[start : end + 1] if include_last else lst[start:end]

    @classmethod
    def get_first_items(
        cls,
        iterable: t.Iterable[T],
        n: int,
    ) -> t.Iterable[T]:
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
        iterable : t.Sequence[Any]
            待提取序列
        n : int
            前n个元素

        Returns
        -------
        t.Iterable[Any]
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
    def get_first_match(
        cls,
        iterable: t.Iterable[T],
        func: t.Callable[[T], bool],
        default_val: T = None,
    ) -> T:
        """
        从可迭代对象中返回第一个符合条件的元素

        Parameters
        ----------
        iterable : t.Iterable[Any]
            待提取可迭代对象
        func : t.Callable[[Any], bool]
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
    def is_all_element_equal(cls, iterable: t.Iterable[T]) -> bool:
        """
        判断序列中是否所有元素相等

        Example:
        ----------
        >>> SequenceUtil.is_all_ele_equal([1, 1, 1, 1]) # True
        >>> SequenceUtil.is_all_ele_equal([1, 2, 1, 1]) # False

        Parameters
        ----------
        iterable : t.Iterable[Any]
            待检测序列

        Returns
        -------
        bool
            如果所有元素相等返回True, 否则返回False
        """
        g = it.groupby(iterable)
        return next(g, True) and not next(g, False)  # type: ignore

    @classmethod
    def cycle_shift(
        cls,
        seq: t.Sequence[T],
        move_length: int,
    ) -> t.Sequence[T]:
        """
        将列表滚动移动 n 位

        Parameters
        ----------
        seq : t.Sequence[Any]
            待滚动序列
        move_length : int
            滚动位数, 正数向后移动, 负数向前移动

        Returns
        -------
        t.Sequence[Any]
            滚动后的新列表
        """
        if cls.is_empty(seq):
            return cls.EMPTY
        seq_length = len(seq)

        if abs(move_length) > seq_length:
            move_length %= seq_length

        res = list(seq[-move_length:])
        res.extend(iter(seq[:-move_length]))
        return res

    @classmethod
    def get_chunks(
        cls,
        seq: t.Sequence[T],
        chunk_size: int,
    ) -> t.Generator[t.Sequence[T], None, None]:
        """
        根据给定的大小, 将序列切分为多个块

        Parameters
        ----------
        seq : t.Sequence[Any]
            待切分序列
        chunk_size : int
            给定的块大小

        Returns
        -------
        t.Generator[t.Sequence[Any], None, None]
            块序列的生成器

        Yields
        ------
        Iterator[t.Generator[t.Sequence[Any], None, None]]
            块序列的生成器

        NOTES:
        ------
        参考:https://stackoverflow.com/a/312464
        """
        seq_length = cls.get_length(seq)
        for i in range(0, seq_length, chunk_size):
            yield seq[i : i + chunk_size]

    @classmethod
    def flatten_sequence(
        cls,
        seq: t.Sequence[T],
    ) -> t.Generator[T, None, None]:
        """
        将嵌套序列展开

        Example:
        ----------
        >>> lst = [1, [2, 3], 4, [5, [6, 7]]]
        ... list(SequenceUtil.flatten_sequence(lst))
        [1, 2, 3, 4, 5, 6, 7]

        Parameters
        ----------
        seq : t.Sequence[Any]
            待展开序列

        Returns
        -------
        None
            展开后的序列

        NOTES:
        ------
        refer: https://stackoverflow.com/a/2158532
        """
        for i in seq:
            if isinstance(i, Sequence):
                yield from cls.flatten_sequence(i)
            else:
                yield i

    @classmethod
    def split_sequence(
        cls,
        seq: t.Sequence[T],
        num_of_group: int,
    ) -> Sequence[Sequence[T]]:
        """
        将序列切分成指定数量的组

        Parameters
        ----------
        seq : t.Sequence[Any]
            待切分序列
        num_of_group : int
            给定的组数量

        Returns
        -------
        Sequence[Sequence[Any]]
            切分后的多个序列组成的列表

        Raises
        ------
        ValueError
            如果num_of_group小于等于0则抛出异常
        """
        if num_of_group <= 0:
            raise ValueError("num_of_group should be greater than 0")

        length = cls.get_length(seq)
        if num_of_group == 1:
            return [seq]

        if length <= num_of_group:
            return [[i] for i in seq]

        cnt_of_group = int(length / num_of_group)
        out = []
        split_cnt_lst = []
        tmp = 0
        while tmp + cnt_of_group <= length:
            split_cnt_lst.append(cnt_of_group)
            tmp += cnt_of_group

        split_cnt_lst[-1] += length - tmp
        logger.debug(f"split_cnt_lst: {split_cnt_lst}")

        last = 0
        for i in split_cnt_lst:
            out.append(seq[last : last + i])
            last += i

        return out

    @classmethod
    def split_half(cls, seq: t.Sequence[T]) -> Sequence[Sequence[T]]:
        """
        将序列切分成前后两半

        Parameters
        ----------
        seq : t.Sequence[Any]
            待切分序列

        Returns
        -------
        t.Tuple[t.Sequence[Any], t.Sequence[Any]]
            切分后的前后两半序列
        """
        return cls.split_sequence(seq, 2)

    @classmethod
    def merge_ranges(cls, *ranges) -> list:
        """
        合并多个范围, 并返回合并后的范围列表

        Example:
        ----------
        >>> merge_ranges([(1, 3), (2, 4), (5, 6)])
        [(1, 4), (5, 6)]

        Parameters
        ----------
        ranges : t.Tuple[t.Tuple[int, int], ...]
            待合并的范围列表

        Returns
        -------
        t.List[t.Tuple[int, int]]
            合并后的范围列表
        """

        def has_intersection(r1, r2, key_func=lambda x: x):
            c, d = key_func(r2)
            a, b = key_func(r1)
            return b >= c and d >= a

        if not ranges:
            return []
        # (1, 3), (2, 4), (7, 8)]
        ranges = sorted(ranges, key=lambda s: s[0])
        logger.warning(f"ranges: {ranges}")
        merged = [ranges[0]]
        for r in ranges[1:]:
            if has_intersection(merged[-1], r):
                merged[-1] = (min(merged[-1][0], r[0]), max(merged[-1][1], r[1]))
            else:
                merged.append(r)

        return merged


class StringUtil(SequenceUtil):
    # UNICODE 字符宽度
    WIDTHS = [
        (126, 1),
        (159, 0),
        (687, 1),
        (710, 0),
        (711, 1),
        (727, 0),
        (733, 1),
        (879, 0),
        (1154, 1),
        (1161, 0),
        (4347, 1),
        (4447, 2),
        (7467, 1),
        (7521, 0),
        (8369, 1),
        (8426, 0),
        (9000, 1),
        (9002, 2),
        (11021, 1),
        (12350, 2),
        (12351, 1),
        (12438, 2),
        (12442, 0),
        (19893, 2),
        (19967, 1),
        (55203, 2),
        (63743, 1),
        (64106, 2),
        (65039, 1),
        (65059, 0),
        (65131, 2),
        (65279, 1),
        (65376, 2),
        (65500, 1),
        (65510, 2),
        (120831, 1),
        (262141, 2),
        (1114109, 1),
    ]

    __VAL = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    __SYB = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

    @classmethod
    def is_string(cls, obj: T, *, raise_type_exception: bool = False) -> bool:
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
    def is_all_whitespace(cls, s: str) -> bool:
        """
        判断字符串是否全为空白字符

        Examples:
        -------

        >>> assert is_all_whitespace('   ') # returns true
        True
        >>> assert is_all_whitespace('foo') # returns false
        False

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            字符串是否全为空白字符
        """
        return all(c.isspace() for c in s) if s is not None else False

    @classmethod
    def is_ascii_control(cls, s: str) -> bool:
        """
        判断字符串是否全为ASCII控制字符

        Parameters
        ----------
        s : str
            待判断字符串

        Returns
        -------
        bool
            如果字符串中的每个字符都是ASCII控制字符, 则返回True, 否则返回False
        """
        return all((ord(c) < 32 or ord(c) == 127) for c in s)

    @classmethod
    def is_unicode_str(cls, s: str) -> bool:
        """
        判断字符串是否为unicode字符串

        Parameters
        ----------
        s : str
            待检测字符
        """
        code_point = ord(s)
        return 0 <= code_point <= 0x10FFFF

    @classmethod
    def is_file_separator(cls, s: str) -> bool:
        """
        判断给定字符是否是文件分隔符, 即 / 或 \

        Parameters
        ----------
        s : str
            待检测字符

        Returns
        -------
        bool
            如果是文件分隔符返回True, 否则返回False

        Raises
        ------
        ValueError
            如果字符串长度不为1则抛出异常
        """
        if (length := cls.get_length(s)) != 1:
            raise ValueError(f"expected a character, but string of length {length} found")

        return cls.equals_any(s, CharPool.SLASH, CharPool.BACKSLASH)

    @classmethod
    def is_blank(
        cls,
        s: str | None,
    ) -> bool:
        """
        判断给定的字符串是否为空, 空字符串包括null、空字符串: ""、空格、全角空格、制表符、换行符, 等不可见字符, \\n

        Parameters
        ----------
        s : t.Optional[str]
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

        if not isinstance(s, str):
            raise TypeError(f"{s} is not a string")

        if s is None:
            return True

        for c in s:
            if c in (string.ascii_letters + string.digits + string.punctuation):
                return False

        return len(s.strip()) == 0

    @classmethod
    def is_not_blank(cls, s: str) -> bool:
        """
        判断给定的字符串是否为非空。\n
        NOTE 依赖于is_blank实现。

        :param s: 被检测的字符串
        :param raise_type_exception: 如果类型错误, 是否要抛出异常
        :return: 如果字符串为非空返回True, 否则返回False
        """
        return not cls.is_blank(s)

    @classmethod
    def has_blank(cls, *args) -> bool:
        """
        判断多个字符串中是否有空白字符串
        :param args: 待判断字符串
        :return: 如果有空白字符串返回True, 否则返回False
        """
        return True if cls.is_empty(args) else any(cls.is_blank(arg) for arg in args)

    @classmethod
    def is_all_blank(cls, *args) -> bool:
        """
        给定的多个字符串是否全为空
        :param args: 待检测的多个字符串
        :return: 如果都为空则返回True, 否则返回False
        """
        if cls.is_empty(args):
            return True

        return not any(cls.is_not_blank(arg) for arg in args)

    @classmethod
    def starts_with(
        cls,
        s: str,
        prefix: str,
        *,
        case_insensitive: bool = True,
    ) -> bool:
        """
        检查字符串 s 是否以指定的前缀 prefix 开头。

        Parameters
        ----------
        s : str
            待检测字符串
        prefix : str
            前缀
        case_insensitive : bool, optional
            大小写是否敏感, by default True
        strict_mode : bool, optional
            是否采用严格模式, by default False

        Returns
        -------
        bool
            字符串 s 是否以指定的前缀 prefix 开头。
        """

        if case_insensitive:
            return s.lower().startswith(prefix.lower())

        return s.startswith(prefix)

    @classmethod
    def starts_with_any(cls, s: str, *prefixes: str, case_insensitive: bool = False) -> bool:
        """
        判断给定字符串是否以任何一个字符串开始.
        如果 prefixes 为空或者s为空, 则返回False.

        Parameters
        ----------
        s : str
            待检测字符串
        case_insensitive : bool, optional
            是否忽略大小写, by default False

        Returns
        -------
        bool
            如果字符串以任何一个字符串开始返回True, 否则返回False
        """
        return (
            False
            if cls.is_empty(prefixes) or cls.is_blank(s)
            else any(cls.starts_with(s, prefix, case_insensitive=case_insensitive) for prefix in prefixes)
        )

    @classmethod
    def ends_with(
        cls,
        s: str,
        suffix: str,
        *,
        case_insensitive: bool = True,
        strict_mode: bool = False,
    ) -> bool:
        """
        判断一个字符串 s 是否以指定的后缀 suffix 结尾

        Parameters
        ----------
        s : str
            待检测字符串
        suffix : str
            制定的后缀
        case_insensitive : bool, optional
            大小写是否敏感, by default True
        strict_mode : bool, optional
            是否采用严格模式, by default False

        Returns
        -------
        bool
            字符串 s 是否以指定的后缀 suffix 结尾
        """
        if strict_mode:
            return s.endswith(suffix)

        s = s.strip()
        suffix = suffix.strip()
        if case_insensitive:
            return s.lower().endswith(suffix.lower())

        return s.endswith(suffix)

    @classmethod
    def is_surround(cls, s: str, prefix: str, suffix: str, case_insensitive: bool = True) -> bool:
        """
        判断字符串是否由指定前后缀包围

        Parameters
        ----------
        s : str
            待检测字符串
        prefix : str
            指定前缀
        suffix : str
            指定后缀

        Returns
        -------
        bool
            是否由指定前后缀包围
        """
        if case_insensitive:
            s = s.lower()
            prefix = prefix.lower()
            suffix = suffix.lower()
        return s.startswith(prefix) and s.endswith(suffix)

    @classmethod
    def ends_with_any(cls, s: str, *suffixes: str, case_insensitive: bool = False) -> bool:
        """
        判断一个字符串 s 是否以任何一个给定字符串结尾
        如果 suffixes 为空或者s为空, 则返回False.

        Parameters
        ----------
        s : str
            待检测字符串
        case_insensitive : bool, optional
            是否忽略大小写, by default False

        Returns
        -------
        bool
            字符串 s 是否以任何一个给定字符串结尾
        """
        if cls.is_empty(suffixes) or cls.is_blank(s):
            return False
        return any(cls.ends_with(s, suffix, case_insensitive=case_insensitive) for suffix in suffixes)

    @classmethod
    def is_mixed_case(cls, s: str) -> bool:
        """
        判断给定的字符串是否包含大写字母和小写字母

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            如果字符串包含大写字母和小写字母则返回True, 否则返回False
        """
        if cls.is_empty(s) or cls.get_length(s) == 1:
            return False
        contain_lower_case = False
        contain_upper_case = False
        for c in s:
            if c.islower():
                contain_lower_case = True
            elif c.isupper():
                contain_upper_case = True

        return contain_lower_case and contain_upper_case

    @classmethod
    def is_half_of_alphabet(cls, text: str) -> bool:
        """
        判断给定的字符串是否都是字母表中前半部分的字母

        Parameters
        ----------
        text : str
            待检测字符串

        Returns
        -------
        bool
            如果字符串都是字母表中前半部分的字母则返回True, 否则返回False
        """
        return all(c.lower() <= "m" for c in text)

    @classmethod
    def is_last_half_of_alphabet(cls, text: str) -> bool:
        """
        判断给定的字符串中的字符是否都是字母表中最后半部分的字母

        Parameters
        ----------
        text : str
            待检测字符串

        Returns
        -------
        bool
            如果字符串中的字符都是字母表中最后半部分的字母则返回True, 否则返回False
        """
        return all(c.lower() >= "m" for c in text)

    @classmethod
    def contain_digit(cls, s: str) -> bool:
        """
        判断字符串是否包含数字

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            字符串是否包含数字
        """
        return any(char.isdigit() for char in s)

    @classmethod
    def has_lowercase(cls, s: str) -> bool:
        """
        判断字符串是否包含小写字母

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            字符串是否包含小写字母
        """
        return any(char.islower() for char in s)

    @classmethod
    def has_uppercase(cls, s: str) -> bool:
        """
        判断字符串是否包含大写字母

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            字符串是否包含大写字母
        """
        return any(char.isupper() for char in s)

    @classmethod
    def none_to_empty(cls, s: str) -> str:
        """
        当给定字符串为null时, 转换为Empty

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        str
            转换后的字符串
        """
        return cls.none_to_default(s, cls.EMPTY)

    @classmethod
    def none_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是 null, 则返回指定默认字符串, 否则返回字符串本身。

        Parameters
        ----------
        s : str
            待检测字符串
        default_str : str
            默认字符串

        Returns
        -------
        str
            如果字符串是 null, 则返回指定默认字符串, 否则返回字符串本身。
        """
        return default_str if s is None else s

    @classmethod
    def empty_to_default(cls, s: str, default_str: str) -> str:
        """
        如果字符串是null或者"", 则返回指定默认字符串, 否则返回字符串本身。

        Parameters
        ----------
        s : str
            待检测字符串
        default_str : str
            默认字符串

        Returns
        -------
        str
            转换后的字符串
        """
        return default_str if s is None or cls.EMPTY == s else s

    @classmethod
    def empty_to_none(cls, s: str) -> str | None:
        """
        当给定字符串为空字符串时, 转换为null

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        str | None
            转换后的值
        """
        return None if cls.is_empty(s) else s

    @classmethod
    def to_bytes(
        cls,
        byte_or_str: bytes | str,
        encoding: str = CharsetUtil.UTF_8,
    ) -> bytes:
        """
        将字节序列或者字符串转换成字节序列

        Parameters
        ----------
        byte_or_str : bytes | str
            待转换对象
        encoding : str, optional
            编码方式, by default CharsetUtil.UTF_8

        Returns
        -------
        bytes
            如果是bytes序列则返回自身, 否则编码后返回

        Raises
        ------
        TypeError
            如果 byte_or_str 不是 bytes 或 str 则抛出异常
        """
        if not isinstance(byte_or_str, (str | bytes)):
            raise TypeError(f"Expected bytes or str, but found {type(byte_or_str)}")

        return byte_or_str if isinstance(byte_or_str, bytes) else byte_or_str.encode(encoding)

    @classmethod
    def to_str(
        cls,
        byte_or_str: bytes | str,
        encoding: str = CharsetUtil.UTF_8,
    ) -> str:
        """
        将字节序列或者字符串转换成字符串

        Parameters
        ----------
        byte_or_str : bytes | str
            待转换对象
        encoding : str, optional
            解码方式, by default CharsetUtil.UTF_8

        Returns
        -------
        str
            如果是字符串则返回自身, 否则解码后返回

        Raises
        ------
        TypeError
            如果 byte_or_str 不是 bytes 或 str 则抛出异常
        """
        if not isinstance(byte_or_str, (str | bytes)):
            raise TypeError(f"Expected bytes or str, but found {type(byte_or_str)}")
        return byte_or_str if isinstance(byte_or_str, str) else byte_or_str.decode(encoding)

    @classmethod
    def as_set(cls, *args, froze: bool = False) -> Set[T]:
        """
        将多个字符串输入转换成集合

        Parameters
        ----------
        froze : bool, optional
            输出集合是否不可变, by default False

        Returns
        -------
        Set[Any]
            返回的集合
        """
        return frozenset(args) if froze else set(args)

    @classmethod
    def as_list(cls, *args) -> list[str]:
        """
        将多个字符串输入转换成列表

        Returns
        -------
        list[str]
            返回的列表
        """
        return list(args)

    @classmethod
    def show_unicode_info(cls, s: str) -> None:
        """
        显示字符串的unicode信息

        Parameters
        ----------
        s : str
            待显示的字符串
        """
        for code_point in s:
            print(f"U+{ord(code_point):04X}, code point: {code_point}, name: {unicodedata.name(code_point)}")

    @classmethod
    def convert_to_circled(cls, char: str) -> str:
        """
        将字母、数字转换为带圈的字符：

        Parameters
        ----------
        char : str
            待转换字符

        Returns
        -------
        str
            转换后的带圈字符

        Raises
        ------
        ValueError
            如果 char 不是单个字符则抛出异常
        """
        if (length := cls.get_length(char)) != 1:
            raise ValueError(f"expected a character, but string of length {length} found")
        if "0" <= char <= "9":
            # 带圈数字的 Unicode 编码从 ① (2460) 开始
            return chr(ord(char) + 0x245F)
        elif "A" <= char <= "Z":
            # 带圈大写字母的 Unicode 编码从 Ⓐ (24B6) 开始
            return chr(ord(char) + 0x24B6 - ord("A"))
        elif "a" <= char <= "z":
            # 带圈小写字母的 Unicode 编码从 ⓐ (24D0) 开始
            return chr(ord(char) + 0x24D0 - ord("a"))
        else:
            # 非数字或字母字符，返回原字符
            return char

    @classmethod
    def camel_case_to_snake(
        cls,
        input_string: str,
        separator="_",
    ) -> str:
        """
        camelCase 格式的字符串转为 snake_case 格式的字符串

        Parameters
        ----------
        input_string : str
            待转换字符串
        separator : str, optional
            分隔符, by default "_"

        Returns
        -------
        str
            转换后的字符串

        Raises
        ------
        TypeError
            如果 input_string 不是字符串则抛出异常
        """
        if not cls.is_string(input_string):
            raise TypeError("input_string must be a string")

        return PatternPool.CAMEL_CASE_REPLACE.sub(lambda m: m.group(1) + separator, input_string).lower()

    @classmethod
    def snake_case_to_camel(
        cls,
        input_string: str,
        upper_case_first: bool = False,
        separator: str = "_",
    ) -> str:
        """
        将 snake_case 格式的字符串转为 camelCase 格式的字符串

        Parameters
        ----------
        input_string : str
            待转换字符串
        upper_case_first : bool, optional
            是否首单词首字母大写, by default False
        separator : str, optional
            分隔符, by default "_"

        Returns
        -------
        str
            转换后的字符串

        Raises
        ------
        TypeError
            如果 input_string 不是字符串则抛出异常
        """
        if not cls.is_string(input_string):
            raise TypeError("input_string must be a string")

        tokens = [s.title() for s in input_string.split(separator)]

        if not upper_case_first:
            tokens[0] = tokens[0].lower()

        return "".join(tokens)

    @classmethod
    def get_circled_number(cls, number: int) -> str:
        """
        将[1-20]数字转换为带圈的字符：

        Parameters
        ----------
        number : int
            待转换数字

        Returns
        -------
        str
            转换后的带圈字符

        Raises
        ------
        ValueError
            如果 number 不是[1-20]范围的数字则抛出异常
        """
        if not (1 <= number <= 20):
            raise ValueError("number should be between 1 and 20")
        return chr(ord("①") + number - 1)

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
    def sub_before(cls, s: str, separator: str, use_last_separator: bool = False) -> str:
        """
        截取分隔字符串之前的字符串，不包括分隔字符串本身。

        Parameters
        ----------
        s : str
            被查找的字符串
        separator : str
            分隔字符串
        use_last_separator : bool, optional
            是否查找最后一个分隔字符串（多次出现分隔字符串时选取最后一个）, by default False

        Returns
        -------
        str
            切割后的字符串
        """
        if cls.is_blank(s):
            return cls.EMPTY

        if cls.is_blank(separator):
            return s

        try:
            separator_idx = s.rindex(separator) if use_last_separator else s.index(separator)
        except ValueError:
            return s
        else:
            return s[:separator_idx]

    @classmethod
    def sub_after(cls, s: str, separator: str, use_last_separator: bool = False) -> str:
        """
        截取分隔字符串之后的字符串，不包括分隔字符串本身。

        Parameters
        ----------
        s : str
            被查找的字符串
        separator : str
            分隔字符串
        use_last_separator : bool, optional
            是否查找最后一个分隔字符串（多次出现分隔字符串时选取最后一个）, by default False

        Returns
        -------
        str
            切割后的字符串
        """
        if cls.is_blank(s):
            return cls.EMPTY

        if cls.is_blank(separator):
            return s

        try:
            separator_idx = s.rindex(separator) if use_last_separator else s.index(separator)
        except ValueError:
            return s
        else:
            return s[separator_idx + 1 :]

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
    ) -> bool:
        """
        判断两个字符串是否相等

        Parameters
        ----------
        s1 : str
            待检测字符串 s1
        s2 : str
            待检测字符串 s2
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        bool
            返回两个字符串是否相等
        """
        if s1 is None or s2 is None:
            return False

        s1_length = cls.get_length(s1)
        s2_length = cls.get_length(s2)
        if s1_length != s2_length:
            return False

        for i, j in zip(s1, s2):
            if case_insensitive:
                if i.lower() != j.lower() and i.upper() != j.upper():
                    return False
            elif i != j:
                return False

        return True

    @classmethod
    def not_equals(
        cls,
        s1: str,
        s2: str,
        *,
        case_insensitive: bool = True,
    ) -> bool:
        """
        判断两个字符串是否不相等

        Parameters
        ----------
        s1 : str
            待检测字符串1
        s2 : str
            待检测字符串2
        case_insensitive : bool, optional
            是否忽略大小写, by default True


        Returns
        -------
        bool
            _description_
        """
        return not cls.equals(s1, s2, case_insensitive=case_insensitive)

    @classmethod
    def equals_any(cls, s: str, *args: str, case_insensitive: bool = True) -> bool:
        """
        判断字符串 s 等于任何一个给定的字符串 args 中的字符串, 则返回 True, 否则返回 False.

        Parameters
        ----------
        s : str
            待检测字符串 s
        args : str
            待比较的字符串列表
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        bool
            如果字符串 s 等于任何一个给定的字符串 args 中的字符串, 则返回 True, 否则返回 False.
        """
        if cls.is_empty(args):
            return False
        return any(cls.equals(s, arg, case_insensitive=case_insensitive) for arg in args)

    @classmethod
    def hide(cls, s: str, start: int, end: int, *, replace_char: str = "*") -> str:
        """
        隐藏字符串 s 中从 start 到 end 位置的字符, 用指定的替换字符 replace_char 替换。

        Parameters
        ----------
        s : str
            待替换字符串
        start : int
            开始替换的位置, 包含
        end : int
            替换结束的位置, 不包含
        replace_char : str, optional
            替换后的字符串, 其中从 start 到 end 的字符被替换为 replace_char, by default "*"

        Returns
        -------
        str
            替换后的字符串
        """
        if cls.is_blank(s):
            return s

        if start > len(s):
            return s

        end = min(end, len(s))
        new_str_lst = []
        for i, v in enumerate(s):
            if start <= i < end:
                new_str_lst.append(replace_char)
            else:
                new_str_lst.append(v)

        return "".join(new_str_lst)

    @classmethod
    def sub_sequence(
        cls,
        lst: Sequence[T],
        start: int,
        end: int | None = None,
        *,
        include_last: bool = False,
    ) -> str:
        """
        根据给定的字符串获取子字符串

        Parameters
        ----------
        lst : Sequence[Any]
            主字符串
        start : int
            子字符串起始索引
        end : int
            子字符串结束索引
        include_last : bool, optional
            是否包含end索引位置的元素, by default False

        Returns
        -------
        str
            子字符串
        """
        if end is None:
            end = cls.get_length(lst)
        sub_seq = super().sub_sequence(lst, start, end, include_last=include_last)
        return "".join(sub_seq)

    @classmethod
    def get_name_sequence(cls, prefix: str) -> Generator[str, T, None]:
        """
        返回一个名字序列生成器

        Parameters
        ----------
        prefix : str
            名字前缀

        Returns
        -------
        t.Callable[[], str]
            名字序列生成器
        """
        sequence = it.count()
        while True:
            yield f"{prefix}{next(sequence)}"

    @classmethod
    def get_new_name(
        cls,
        taken: t.Collection[str],
        base: str,
        transform: t.Callable[[str], str] = None,
    ) -> str:
        """
        获取一个新的名字, 保证名字不重复

        Parameters
        ----------
        taken : t.Collection[str]
            已有名字集合
        base : str
            基础名字
        transform : t.Callable[[str], str], optional
            名字转换函数, by default None

        Returns
        -------
        str
            一个重复的名字
        """
        if base is None:
            raise ValueError("base cannot be None")
        if base not in taken:
            return base

        if transform is None:
            i = 1
            new = f"{base}_{i}"
            while new in taken:
                i += 1
                new = f"{base}_{i}"
            return new
        else:
            new = base
            while new in taken:
                new = transform(new)
            return new

    @classmethod
    def get_random_strs(cls, n: int, *, chars: str | None = None) -> str:
        """
        返回给定数量的随机字符串

        Parameters
        ----------
        n : int
            字符数量
        chars : t.Optional[str], optional
            源字符串, 如果为None则使用默认的字符集, by default None

        Returns
        -------
        str
            随机字符串
        """
        if chars is None:
            chars = string.ascii_letters

        return "".join(RandomUtil.get_random_items_from_sequence(chars, n))

    @classmethod
    def get_random_secure_hex(cls, n: int) -> str:
        """
        获取随机的安全的十六进制字符串

        Parameters
        ----------
        n : int
            字符串数量

        Returns
        -------
        str
            随机的安全的十六进制字符串

        Raises
        ------
        ValueError
            如果 n 小于 1, 则抛出异常
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError("byte_count must be >= 1")

        random_bytes = os.urandom(n)
        hex_bytes = binascii.hexlify(random_bytes)
        return hex_bytes.decode()

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

    @classmethod
    def generate_box_string_from_dict(
        cls,
        data: t.Mapping[str, T],
        *,
        title: str = " RESULT ",
    ) -> str:
        """
        从字典数据生成箱体信息

        Parameters
        ----------
        data : t.Mapping[str, Any]
            待生成的数据
        title : str, optional
            标题, by default " RESULT "

        Returns
        -------
        str
            箱体信息
        """

        def get_center_title(title: str) -> str:
            if not title.startswith(" ") and not title.endswith(" "):
                return f" {title} "
            if not title.startswith(" "):
                return f" {title}"

            return title if title.endswith(" ") else f"{title} "

        def get_max_length_from_dict(data: t.Mapping[str, T], level: int = 0) -> tuple[int, int]:
            max_key_length = 0
            max_value_length = 0
            for key, value in data.items():
                if isinstance(value, dict):
                    sub_max_key_length, sub_max_value_length = get_max_length_from_dict(value, level + 1)
                    max_key_length = max(max_key_length, sub_max_key_length)
                    max_value_length = max(max_value_length, sub_max_value_length)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            sub_max_key_length, sub_max_value_length = get_max_length_from_dict(item, level + 1)
                            max_key_length = max(max_key_length, sub_max_key_length)
                            max_value_length = max(max_value_length, sub_max_value_length)
                        else:
                            raise TypeError(f"Unsupported type: {type(item)}")
                else:
                    max_key_length = max(max_key_length, get_length_with_level(str(key), level))
                    max_value_length = max(max_value_length, cls.get_width(str(value)))

            return max_key_length, max_value_length

        def get_length_with_level(key: str, level: int, step: int = 2) -> int:
            return cls.get_width(key) + len(get_left_padding_str(level))

        def get_left_padding_str(level: int, fill_str: str = " ", step: int = 2) -> str:
            return fill_str * level * step

        def append_content_lines(data, level) -> None:
            for k, v in data.items():
                if isinstance(v, dict):
                    _append_content_line(k, "", level)
                    append_content_lines(v, level + 1)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            append_content_lines(v, level + 1)
                        else:
                            raise TypeError(f"Unsupported type: {type(item)} in nested dict")
                else:
                    _append_content_line(f"{k}", f"{v}", level)

        def _append_content_line(key: str, value: str, level: int) -> None:
            prefix = "| "
            symbol = " : "
            suffix = " |"

            current_key_length = get_length_with_level(key, level)
            current_key_padding_length = max_key_length - current_key_length

            current_value_length = cls.get_width(value)
            current_value_padding_length = max_value_length - current_value_length

            level_padding = get_left_padding_str(level)

            key_padding = ""
            value_padding = ""

            if current_key_padding_length > 0:
                key_padding = " " * current_key_padding_length
            if current_value_padding_length > 0:
                value_padding = " " * current_value_padding_length

            content.append(f"{prefix}{level_padding}{key}{key_padding}{symbol}{value}{value_padding}{suffix}")

        max_key_length, max_value_length = get_max_length_from_dict(data)
        print(f"{max_key_length=}")
        require_symbol_length = 7

        # 边框长度，即 +-----+ 的总长度
        box_width = max_key_length + max_value_length + require_symbol_length

        title = get_center_title(title)
        padding_length = (box_width - cls.get_width(title) - 2) // 2

        # 预生成框的顶部边框
        top_border = "+" + "-" * padding_length + f"{title}" + "-" * padding_length + "+"

        # 生成框的内容
        content: list[str] = []

        # 包装，生成内容
        append_content_lines(data, 0)

        # 生成框的底部边框
        bottom_border = "+" + "-" * (box_width - 2) + "+"

        # 获取修正值
        border_modification_length = cls.get_width(bottom_border) - cls.get_width(top_border)
        if border_modification_length > 0:
            top_border = (
                "+" + "-" * border_modification_length + "-" * padding_length + f"{title}" + "-" * padding_length + "+"
            )

        # 合并所有部分
        box_string = "\n".join([top_border] + content + [bottom_border])
        return box_string

    @classmethod
    def get_annotation_str(cls, s: str, annotation_syntax: str = "--") -> str:
        """
        生成备注释信息

        Parameters
        ----------
        s : str
            待注释字符串
        annotation_syntax : str, optional
            注释语法, by default "--"

        Returns
        -------
        str
            被注释的语句
        """
        line_lst = []
        lines = s.splitlines()
        if not lines:
            return f"{annotation_syntax} {s}"
        for line in lines:
            if not line.startswith(annotation_syntax):
                line_lst.append(f"{annotation_syntax} {line}")
            else:
                line_lst.append(line)

        return "\n".join(line_lst)

    @classmethod
    def get_width(cls, s: str) -> int:
        """
        获取字符串显示宽度

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        int
            字符串长度
        """
        if s is None:
            return 0
        if cls.is_all_whitespace(s):
            return len(s)

        if cls.is_blank(s):
            return 0

        length = 0
        for c in s:
            if (o := ord(c)) == 0xE or o == 0xF:
                continue
            for num, wid in cls.WIDTHS:
                if o <= num:
                    length += wid
                    break

        return length

    @classmethod
    def align_text(cls, text: str, padding: str = " ", align: str = "left") -> str:
        """
        根据指定的方式对齐字符串

        Parameters
        ----------
        text : str
            待对齐文本
        padding : str, optional
            填充字符串, by default " "
        align : str, optional
            对齐方式, by default "left"

        Returns
        -------
        str
            对齐后的字符串

        Raises
        ------
        ValueError
            如果对齐方式不是 "left", "right" 或 "center", 则抛出异常
        """
        if align in {"left", "right", "center"}:
            return (
                cls._align_text(text, len(text) + 1, padding, align)
                if align in {"left", "right"}
                else cls._align_text(text, len(text) + 2, padding, align)
            )
        else:
            raise ValueError(f"align must be 'left', 'right' or 'center', but got {align}")

    @classmethod
    def get_common_suffix(cls, str1: str, str2: str) -> str:
        """
        返回两个字符串的公共后缀

        Parameters
        ----------
        str1 : str
            待检测字符串1
        str2 : str
            待检测字符串2

        Returns
        -------
        str
            公共后缀
        """
        rev_str1 = str1[::-1]
        rev_str2 = str2[::-1]
        return cls.get_common_prefix(rev_str1, rev_str2)[::-1]

    @classmethod
    def get_common_prefix(cls, str1: str, str2: str) -> str:
        """
        返回两个字符串的公共前缀

        Parameters
        ----------
        str1 : str
            待检测字符串1
        str2 : str
            待检测字符串2

        Returns
        -------
        str
            两个字符串的公共前缀
        """
        min_len = min(len(str1), len(str2))

        common_str_lst = []
        for i in range(min_len):
            if str1[i] != str2[i]:
                break
            else:
                common_str_lst.append(str1[i])

        return "".join(common_str_lst)

    @classmethod
    def get_most_common_letter(cls, text: str) -> str:
        """
        获取给定字符串中最多的字母

        Parameters
        ----------
        text : str
            待检测字符串

        Returns
        -------
        str
            字符串中最多的字母
        """
        if cls.is_blank(text):
            return cls.EMPTY
        text = text.lower()
        return max(string.ascii_lowercase, key=text.count)

    @classmethod
    def get_right(cls, s: str, len: int) -> str:
        """
        获取最右边的字符串

        Parameters
        ----------
        s : str
            待获取字符串
        len : int
            获取的长度

        Returns
        -------
        str
            获取后的字符串
        """
        if s is None or len < 0:
            return cls.EMPTY
        if len >= (s_len := cls.get_length(s)):
            return s

        return cls.sub_sequence(s, s_len - len)

    @classmethod
    def get_ascii_number_pairs(cls, text: str) -> list[tuple[str, int]]:
        """
        获取字符串-ASCII码对

        Parameters
        ----------
        text : str
            待获取字符串

        Returns
        -------
        list[tuple[str, int]]
            字符串-ASCII码对列表
        """
        return [(c, ord(c)) for c in text]

    @classmethod
    def group_by_length(cls, s: str, n: int) -> list[str]:
        """
        根据制定的长度分组字符串

        Parameters
        ----------
        s : str
            待分组字符串
        n : int
            每组字符串数量

        Returns
        -------
        t.List[str]
            分组后的字符串
        """
        if SequenceUtil.is_empty(s):
            return []
        return [s[i : i + n] for i in range(0, len(s), n)]

    @classmethod
    @UnCheckFunction()
    def format_in_currency(cls, s: str | float) -> str:
        """
        格式化字符串为货币格式

        Parameters
        ----------
        s : str
            待格式化字符串

        Returns
        -------
        str
            格式化后的字符串
        """
        # TODO 实现货币格式化, 目前只实现了逗号分隔符的格式化, 只能处理整数
        if isinstance(s, float):
            s = str(s)

        negative_flg = False
        if s.startswith("-"):
            negative_flg = True
            s = s[1:]

        if "." not in s:
            integer_part = s
            decimal_part = ""
        else:
            integer_part, decimal_part = s.split(".")

        rev_str = integer_part[::-1]
        str_lst = cls.group_by_length(rev_str, 3)
        res_lst = [i[::-1] for i in str_lst[::-1]]
        integer_str = ",".join(res_lst)
        decimal_str = f".{decimal_part}" if StringUtil.is_not_blank(decimal_part) else ""
        sign_str = "-" if negative_flg else ""

        return f"{sign_str}{integer_str}{decimal_str}"

    @classmethod
    def unwrap(cls, s: str, wrap_str: str) -> str:
        """
        折叠字符串中给定的字符

        Parameters
        ----------
        s : str
            待折叠字符串
        wrap_str : str
            给定的字符

        Returns
        -------
        str
            折叠后的字符串
        """
        if cls.is_empty(s) or cls.get_length(wrap_str) != 1 or wrap_str == CharPool.NUL or cls.get_length(s) < 2:
            return s

        res_lst = []

        for start_idx in range(len(s)):
            current_char = s[start_idx]
            if current_char != wrap_str:
                res_lst.append(current_char)
            elif SequenceUtil.is_empty(res_lst) or res_lst[-1] != wrap_str:
                res_lst.append(current_char)
        return "".join(res_lst)

    @classmethod
    def shuffle(cls, s: str) -> str:
        """
        打乱字符串并返回

        Parameters
        ----------
        s : str
            待打乱字符串

        Returns
        -------
        str
            打乱后的字符串
        """
        chars = list(s)
        random.shuffle(chars)
        return "".join(chars)

    @classmethod
    def append_if_missing(cls, s: str, suffix: str, case_insensitive: bool = True) -> str:
        """
        如果给定字符串不是以给定的字符串为结尾，则在尾部添加结尾字符串

        Parameters
        ----------
        s : str
            待检测字符串
        suffix : str
            指定后缀
        case_insensitive : bool, optional
            是否大小写敏感, by default True

        Returns
        -------
        str
            填充后的字符串
        """
        if cls.ends_with(s, suffix, case_insensitive=case_insensitive):
            return s
        else:
            return s + suffix

    @classmethod
    def repeat_by_length(cls, s: str, length: int) -> str:
        """
        重复字符串，直到长度达到指定长度


        Parameters
        ----------
        s : str
            待重复字符串
        length : int
            重复后字符串长度

        Returns
        -------
        str
            重复后的字符串
        """
        if cls.get_length(s) == 0:
            return cls.EMPTY
        str_length = len(s)
        if str_length >= length:
            return s[:length]
        else:
            return s + cls.repeat_by_length(s, length - str_length)

    @classmethod
    def repeat_by_count(cls, s: str, num: int) -> str:
        """
        重复字符串，直到数量达到指定数量

        Parameters
        ----------
        s : str
            待重复字符串
        num : int
            重复后字符串数量

        Returns
        -------
        str
            重复后的字符串
        """
        if num == 0:
            return cls.EMPTY
        return s if num == 1 else s + cls.repeat_by_count(s, num - 1)

    @classmethod
    @UnCheckFunction()
    def roman_encode(cls, num: int) -> str:
        """
        将阿拉伯数字转换成罗马数字

        Parameters
        ----------
        num : int
            待转换阿拉伯数字

        Returns
        -------
        str
            转换后的罗马数字
        """
        roman_num = ""
        i = 0
        while num > 0:
            for _ in range(num // cls.__VAL[i]):
                roman_num += cls.__SYB[i]
                num -= cls.__VAL[i]
            i += 1
        return roman_num

    @classmethod
    @UnCheckFunction()
    def roman_decode(cls, s: str) -> int:
        roman_int_mapping = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        int_value = 0
        prev_value = 0

        for char in reversed(s):
            current_value = roman_int_mapping[char]
            if current_value < prev_value:
                int_value -= current_value
            else:
                int_value += current_value
            prev_value = current_value

        return int_value

    @classmethod
    @UnCheckFunction()
    def get_roman_range(cls, start: int, end: int, step: int = 1) -> t.Generator[str, None, None]:
        """
        跟 range 函数一样生成罗马数字序列

        Parameters
        ----------
        start : int
            序列起点
        end : int
            序列终点
        step : int, optional
            序列步长, by default 1

        Returns
        -------
        t.Generator[str, None, None]
            罗马数字字符串生成器

        Yields
        ------
        Iterator[t.Generator[str, None, None]]
            罗马数字字符串迭代器

        Raises
        ------
        ValueError
            当 start 大于 end 时抛出异常
        """
        if start > end:
            raise ValueError(f"{start} must be less than {end}")

        for i in range(start, end):
            yield cls.roman_encode(i)

    @classmethod
    def remove_all(cls, s: str, *chars: str) -> str:
        """
        去除字符串中指定的多个字符，如有多个则全部去除

        Parameters
        ----------
        s : str
            待去除字符串
        chars : str
            字符列表

        Returns
        -------
        str
            如果字符串为 None 、为空或者 chars 参数为空, 则返回字符串本身。\n
            否则返回去除指定字符后的字符串
        """
        if s is None or SequenceUtil.is_empty(chars) or cls.is_blank(s):
            return s

        for char in chars:
            s = s.replace(char, "")

        return s

    @classmethod
    def remove_blank(cls, s: str) -> str:
        """
        移除字符串中的空白字符

        Parameters
        ----------
        s : str
            待移除字符串

        Returns
        -------
        str
            移除空白后的字符串
        """
        filter_result = it.filterfalse(lambda x: cls.is_blank(x), s)
        return "".join(filter_result)

    @classmethod
    def remove_suffix(cls, s: str, suffix: str, case_insensitive: bool = True) -> str:
        """
        移除字符串中的指定后缀

        Parameters
        ----------
        s : str
            待移除字符串
        suffix : str
            指定后缀
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        str
            移除后的字符串
        """
        # NOTE 兼容3.9之前的版本，3.9之后可以直接调用str.removesuffix()方法
        if cls.ends_with(s, suffix, case_insensitive=case_insensitive):
            return s[: -len(suffix)]
        else:
            return s

    @classmethod
    def remove_prefix(cls, s: str, prefix: str, case_insensitive: bool = True) -> str:
        """
        移除字符串中的指定前缀

        Parameters
        ----------
        s : str
            待移除字符串
        prefix : str
            指定的前缀
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        str
            移除后的字符串
        """
        # NOTE 兼容3.9之前的版本，3.9之后可以直接调用str.removesuffix()方法
        if cls.starts_with(s, prefix, case_insensitive=case_insensitive):
            return s[len(prefix) :]
        else:
            return s

    @classmethod
    def remove_char_at(cls, s: str, idx: int) -> str:
        """
        移除字符串中的指定位置的字符

        Parameters
        ----------
        s : str
            待移除字符串
        idx : int
            指定位置

        Returns
        -------
        str
            移除后的字符串
        """
        if idx < 0:
            raise ValueError(f"idx must be greater than or equal to 0, but got {idx}")

        length = cls.get_length(s)
        if cls.is_blank(s):
            return cls.EMPTY

        return s[:-1] if idx >= length or idx == length - 1 else s[:idx] + s[idx + 1 :]

    @classmethod
    def remove_range(cls, s: str, start: int, end: int) -> str:
        """
        移除字符串中的指定范围的字符

        Parameters
        ----------
        s : str
            待移除字符串
        start : int
            起始位置
        end : int
            结束位置

        Returns
        -------
        str
            移除后的字符串
        """
        if start < 0 or end < 0:
            raise ValueError(f"start and end must be greater than or equal to 0, but got {start} and {end}")

        if start >= end:
            raise ValueError(f"start must be less than end, but got {start} and {end}")

        if cls.is_blank(s):
            return cls.EMPTY

        return s[:start] if end >= cls.get_length(s) else s[:start] + s[end:]

    @classmethod
    def remove_non_ascii(cls, s: str) -> str:
        """
        移除字符串中的非ASCII字符

        Parameters
        ----------
        s : str
            待移除字符串

        Returns
        -------
        str
            移除非ASCII后的字符串
        """
        return "".join(filter(lambda x: ord(x) < 128, s))

    @classmethod
    def replace_char_at(cls, s: str, idx: int, char: str) -> str:
        """
        替换字符串中的指定位置的字符

        Parameters
        ----------
        s : str
            待替换字符串
        idx : int
            指定位置
        char : str
            待替换字符

        Returns
        -------
        str
            替换后的字符串
        """
        if idx < 0:
            raise ValueError(f"idx must be greater than or equal to 0, but got {idx}")

        if cls.is_blank(s):
            return cls.EMPTY

        length = cls.get_length(s)

        if idx >= length or idx == length - 1:
            return s[:-1] + char

        return s[:idx] + char + s[idx + 1 :]

    @classmethod
    def replace_range(cls, dest: str, source: str, start: int) -> str:
        """
        使用给定字符串替换指定位置的字符串

        Parameters
        ----------
        dest : str
            待替换字符串
        source : str
            替换字符串
        start : int
            替换起始位置

        Returns
        -------
        str
            替换后的字符串

        Raises
        ------
        ValueError
            如何 start 超出范围, 则抛出异常
        """
        if start < 0 or start > cls.get_length(dest):
            raise ValueError(
                f"start must be greater than or equal to 0 and less than {cls.get_length(dest)}, but got {start}"
            )
        if cls.is_blank(source) or cls.is_blank(dest):
            return dest
        source_len = cls.get_length(source)
        return dest[:start] + source + dest[start + source_len :]

    @classmethod
    def insert_str_at(cls, s: str, idx: int, sub_str: str) -> str:
        """
        在指定位置插入字符

        Parameters
        ----------
        s : str
            待插入字符串
        idx : int
            指定位置
        sub_str : str
            待插入字符

        Returns
        -------
        str
            插入后的字符串
        """
        if idx < 0:
            raise ValueError(f"idx must be greater than or equal to 0, but got {idx}")
        if cls.is_blank(s):
            return sub_str

        length = cls.get_length(s)
        return s + sub_str if idx >= length else s[:idx] + sub_str + s[idx:]

    @classmethod
    def abbreviate(cls, s: str, length: int, ellipsis: str = "...") -> str:
        """
        字符串缩略

        Parameters
        ----------
        s : str
            待缩略字符串
        length : int
            缩略后的最大长度, 小于4时抛出异常
        ellipsis : str, optional
            缩略后的省略号, by default "..."

        Returns
        -------
        str
            如果字符串是None或者为空, 则返回空字符串。\n
            如果字符串长度小于等于指定长度, 则返回原字符串, 否则返回缩略后的字符串

        Raises
        ------
        ValueError
            如果 length 小于4, 则抛出异常
        """
        if length < 4:
            raise ValueError(f"length must be greater than or equal to 4, but got {length}")
        if cls.is_blank(s):
            return cls.EMPTY
        if cls.get_length(s) <= length:
            return s
        else:
            return cls.sub_sequence(s, 0, length - cls.get_length(ellipsis)) + ellipsis  # type: ignore

    @classmethod
    def get_vowels_from_str(cls, s: str) -> str:
        """
        获取字符串中的元音字母

        Parameters
        ----------
        s : str
            待获取元音字母的字符串

        Returns
        -------
        str
            元音字母字符串
        """
        vowels = "aeiouAEIOU"
        return "".join(filter(lambda x: x in vowels, s))

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
        basic_str = cls.get_random_str_lower(k)
        return basic_str.capitalize()

    @classmethod
    def get_random_chinese_generator(cls, length: int = 10) -> t.Generator[str, None, None]:
        """
        获取指定长度的随机中文字符

        Parameters
        ----------
        length : int, optional
            字符序列长度, by default 10

        Returns
        -------
        t.Generator[str, None, None]
            随机中文字符生成器

        Yields
        ------
        Iterator[t.Generator[str, None, None]]
            随机中文字符生成器
        """
        for _ in range(length):
            yield cls.get_random_chinese()

    @classmethod
    def _align_text(cls, text: str, width: int, padding: str = " ", align: str = "left") -> str:
        if align == "left":
            return text.rjust(width, padding)
        elif align == "right":
            return text.ljust(width, padding)
        else:
            return text.center(width, padding)

    @classmethod
    def only_numerics(cls, s: str) -> str:
        """
        仅保留字符串中的数字

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留数字的字符串
        """
        return "".join(filter(str.isdigit, s))

    @classmethod
    def only_alphabetic(cls, s: str) -> str:
        """
        仅保留字符串中的字母

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留字母的字符串
        """
        return "".join(filter(str.isalpha, s))

    @classmethod
    def only_alphanumeric(cls, s: str) -> str:
        """
        仅保留字符串中的字母和数字

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留字母和数字的字符串
        """
        return "".join(filter(str.isalnum, s))

    @classmethod
    def only_uppercase(cls, s: str) -> str:
        """
        仅保留字符串中的大写字母

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留大写字母的字符串
        """
        return "".join(filter(str.isupper, s))

    @classmethod
    def only_lowercase(cls, s: str) -> str:
        """
        仅保留字符串中的小写字母

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留小写字母的字符串
        """
        return "".join(filter(str.islower, s))

    @classmethod
    def only_printable(cls, s: str) -> str:
        """
        仅保留字符串中的可打印字符

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留可打印字符的字符串
        """
        return "".join(filter(str.isprintable, s))

    @classmethod
    def only_ascii(cls, s: str) -> str:
        """
        仅保留字符串中的ASCII字符

        Parameters
        ----------
        s : str
            待处理字符串

        Returns
        -------
        str
            仅保留ASCII字符的字符串
        """
        # PERF 考虑版本兼容性问题
        if sys.version_info[1] >= 7:
            return "".join(filter(lambda x: x.isascii(), s))
        else:
            return "".join(filter(lambda x: ord(x) < 128, s))

    @classmethod
    def first_index_of(
        cls,
        sequence: Sequence[str],
        from_index: int,
        value: str,
        case_insensitive: bool = True,
    ) -> int:
        """
        在给定的字符串序列中查找指定字符串的第一个索引

        Parameters
        ----------
        sequence : Sequence[str]
            待查找的字符串序列
        value : str
            目标字符串
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        int
            如果找到目标字符串, 则返回其索引, 否则返回 -1
        """
        if cls.is_empty(sequence):
            return cls.INDEX_NOT_FOUND
        sub_seq_length = cls.get_length(value)
        split_main_seq = sequence[from_index:]

        return next(
            (
                i + from_index
                for i in range(len(split_main_seq))
                if cls.is_sub_equal(
                    split_main_seq,
                    i,
                    value,
                    0,
                    sub_seq_length,
                    case_insensitive=case_insensitive,
                )
            ),
            cls.INDEX_NOT_FOUND,
        )

    @classmethod
    def last_index_of(
        cls,
        sequence: Sequence[str],
        from_idx: int,
        value: str,
        case_insensitive: bool = True,
    ) -> int:
        """
        在给定的字符串序列中查找指定字符串的最后一个索引

        Parameters
        ----------
        sequence : Sequence[str]
            待查找的字符串序列
        value : str
            目标字符串
        case_insensitive : bool, optional
            是否忽略大小写, by default True

        Returns
        -------
        int
            如果找到目标字符串, 则返回其索引, 否则返回 -1
        """
        if cls.is_empty(sequence):
            return cls.INDEX_NOT_FOUND

        main_seq_length: int = cls.get_length(sequence)
        sub_seq_length = cls.get_length(value)
        if from_idx == 0:
            from_idx = main_seq_length - 1
        else:
            from_idx = main_seq_length - abs(from_idx) if from_idx < 0 else from_idx

        return next(
            (
                i
                for i in range(from_idx, -1, -1)
                if cls.is_sub_equal(
                    sequence,
                    i,
                    value,
                    0,
                    sub_seq_length,
                    case_insensitive=case_insensitive,
                )
            ),
            cls.INDEX_NOT_FOUND,
        )

    @classmethod
    def is_sub_equal(
        cls,
        main_seq: Sequence[str],
        start_idx: int,
        sub_seq: Sequence[str],
        sub_start_idx: int,
        split_length: int,
        case_insensitive: bool = True,
    ) -> bool:
        """
        截取两个字符串的不同部分（长度一致），判断截取的子串是否相同 任意一个字符串为null返回false

        Parameters
        ----------
        main_seq : Sequence[Any]
            主要字符串
        start_idx : int
            主要字符串的起始位置
        sub_seq : Sequence[Any]
            次要字符串
        sub_start_idx : int
            次要字符串的起始位置
        split_length : int
            截取长度

        Returns
        -------
        bool
            子字符串是否相同
        """
        if cls.is_empty(main_seq) or cls.is_empty(sub_seq):
            return False

        main_seq_len = len(main_seq)
        sub_seq_len = len(sub_seq)
        if start_idx < 0 or sub_start_idx < 0:
            return False

        if main_seq_len < start_idx + split_length or sub_seq_len < sub_start_idx + split_length:
            return False

        main_split_seq = main_seq[start_idx : start_idx + split_length]
        sub_split_seq = sub_seq[sub_start_idx : sub_start_idx + split_length]

        for i, j in zip(main_split_seq, sub_split_seq):
            tmp_i = i
            tmp_j = j
            if case_insensitive:
                tmp_i = tmp_i.lower()
                tmp_j = tmp_j.lower()

            if tmp_i != tmp_j:
                return False

        return True

    @classmethod
    def count_letter_by_type(cls, s: str) -> Mapping[str, int]:
        """
        统计字符串中各类字符的数量

        Parameters
        ----------
        s : str
            待统计字符串

        Returns
        -------
        Mapping[str, int]
            各类字符的数量
        """
        basic_dict = {
            "upper": 0,
            "lower": 0,
            "digit": 0,
            "other": 0,
            "whitespaces": 0,
        }

        for c in s:
            if c in string.ascii_lowercase:
                basic_dict["lower"] += 1
            elif c in string.ascii_uppercase:
                basic_dict["upper"] += 1
            elif c in string.digits:
                basic_dict["digit"] += 1
            elif c in string.whitespace:
                basic_dict["whitespaces"] += 1
            else:
                basic_dict["other"] += 1

        return basic_dict

    @classmethod
    def swap_case(cls, s: str) -> str:
        """
        交换字符串中的大小写

        Parameters
        ----------
        s : str
            待交换字符串

        Returns
        -------
        str
            交换后的字符串
        """
        return "".join(map(lambda x: x.swapcase(), s))


class RandomUtil:
    @classmethod
    def get_random_val_from_range(
        cls,
        start: int,
        end: int,
        *,
        both_include: bool = False,
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

        return random.randint(start, end) if both_include else random.randrange(start, end)

    @classmethod
    def get_random_item_from_sequence(cls, seq: t.Sequence[T]) -> T | None:
        """
        随机从序列中抽取元素
        :param seq: 待抽取序列
        :return: 序列元素
        """
        return None if seq is None or len(seq) == 0 else random.choice(seq)

    @classmethod
    def get_random_items_from_sequence(cls, seq: t.Sequence[T], k: int) -> list[T]:
        """
        从给定的序列中随机选择 k 个元素。
        :param seq: 输入的序列, 可以是任何类型的序列（如列表、元组等）。
        :param k: 要从序列中随机选择的元素数量。
        :return: 包含从输入序列中随机选择的 k 个元素的列表。
        """

        if seq is None or len(seq) == 0:
            return []

        if k < 0:
            raise ValueError(f"{k=} must be greater than or equal to 0")

        return list(seq) if k >= len(seq) else random.sample(seq, k)

    @classmethod
    def get_random_distinct_items_from_sequence(
        cls,
        seq: t.Sequence[T],
        k: int,
    ) -> set[T]:
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

        res: set[T] = set()
        cnt = 0

        while len(res) < k:
            random_val = cls.get_random_item_from_sequence(seq)
            res.add(random_val)
            cnt += 1
            if cnt > 2 * k:
                raise ValueError(f"Cannot get {k=} distinct items from {seq=}")
        return res

    @classmethod
    def get_random_booleans(cls, length: int) -> t.Generator[bool, None, None]:
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
    ) -> t.Generator[float, None, None]:
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
            yield cls.get_random_float_with_range_and_precision(start, end, precision=precision)

    @classmethod
    def get_random_float_with_range_and_precision(cls, start: float, end: float, *, precision: int = 3) -> float:
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
        return round(random.uniform(start, end), precision)

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
        real_range: tuple[float, float],
        imag_range: tuple[float, float],
        *,
        precision: int = 3,
        length: int = 10,
    ) -> t.Generator[complex, None, None]:
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
            yield cls.get_random_complex_with_range_and_precision(real_range, imag_range, precision=precision)

    @classmethod
    def get_random_complex_with_range_and_precision(
        cls,
        real_range: tuple[float, float],
        imag_range: tuple[float, float],
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
        real_part = cls.get_random_float_with_range_and_precision(*real_range, precision=precision)
        imag_part = cls.get_random_float_with_range_and_precision(*imag_range, precision=precision)

        return complex(real_part, imag_part)

    @classmethod
    def get_random_bytes(cls, length: int) -> bytes:
        # todo
        raise NotImplementedError()


class DatetimeUtil:
    UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}
    WTB = [
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
    def this_quarter(cls) -> Quarter | None:
        """

        :return:
        """
        dt = datetime.now()
        return Quarter.get_quarter(dt)

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
    def this_millisecond(cls) -> int | float:
        """
        返回当前毫秒数

        Returns
        -------
        int | float
            当前毫秒数
        """
        current_seconds = time.time()
        return cls.convert_time(current_seconds, TimeUnit.SECONDS, TimeUnit.MILLISECONDS)

    @classmethod
    def this_ts(cls) -> float:
        """

        :return:
        """
        return datetime.now().timestamp()

    @classmethod
    def tomorrow(cls) -> datetime:
        """
        返回明天的日期

        Returns
        -------
        date
            明天的日期
        """

        return cls.offset_day(cls.local_now(), 1)

    @classmethod
    def yesterday(cls) -> datetime:
        """
        返回表示昨天的日期对象

        Returns
        -------
        datetime
            表示昨天的日期对象
        """
        return cls.offset_day(cls.local_now(), -1)

    @classmethod
    def today_in_next_year(cls, dt: datetime | None) -> datetime:
        """
        获取下一年的日期

        Parameters
        ----------
        dt : datetime, optional
            待获取下一年的日期, 默认为当前日期, 类型为 datetime

        Returns
        -------
        datetime
            表示下一年同一天的 datetime 对象
        """
        if dt is None:
            dt = cls.local_now()

        if cls.is_leap_year(dt.year):
            return dt.replace(year=dt.year + 1, day=28)
        else:
            return dt.replace(year=dt.year + 1)

    @classmethod
    def today_in_last_year(cls, dt: datetime | None = None) -> datetime:
        """
        获取上一年的日期

        Parameters
        ----------
        dt : datetime | None, optional
            待获取上一年的日期, 默认为当前日期, by default None

        Returns
        -------
        datetime
            表示上一年同一天的 datetime 对象
        """
        if dt is None:
            dt = cls.local_now()

        return dt.replace(year=dt.year - 1)

    @classmethod
    def next_year(cls, dt: datetime | None = None) -> datetime:
        """
        返回下一年的年份

        Parameters
        ----------
        dt : datetime | None, optional
            待判断日期对象, 默认为当前日期

        Returns
        -------
        int
            下一年年份
        """
        if dt is None:
            dt = cls.local_now()
        return cls.offset_year(dt, 1)

    @classmethod
    def last_year(cls, dt: datetime | None = None) -> datetime:
        """
        返回上一年的年份

        Parameters
        ----------
        dt : datetime | None, optional
            待判断日期对象, 默认为当前日期

        Returns
        -------
        int
            上一年年份
        """
        if dt is None:
            dt = cls.local_now()
        return cls.offset_year(dt, -1)

    @classmethod
    def next_quarter(cls, dt: datetime | None = None) -> Quarter | None:
        """
        返回表示下一季度的枚举对象

        Parameters
        ----------
        dt : datetime | None, optional
            待判断日期对象, 默认为当前日期

        Returns
        -------
        Quarter
            _description_
        """
        if dt is None:
            dt = cls.local_now()

        return cls.offset_quarter(dt, 1)

    @classmethod
    def last_quarter(cls, dt: datetime | None = None) -> Quarter | None:
        if dt is None:
            dt = cls.local_now()
        return cls.offset_quarter(dt, -1)

    @classmethod
    def next_month(cls, dt: datetime | None = None) -> datetime:
        """
        返回表示下一个月的枚举对象

        Parameters
        ----------
        dt : datetime | None, optional
            待检测日期对象, by default None

        Returns
        -------
        Month
            表示下一个月的枚举对象
        """
        if dt is None:
            dt = cls.local_now()
        return cls.offset_month(dt, 1)

    @classmethod
    def last_month(cls, dt: datetime | None = None) -> datetime:
        """
        返回表示上一个月的枚举对象

        Parameters
        ----------
        dt : datetime | None, optional
            待检测的日期, 默认为当前日期, by default None

        Returns
        -------
        Month
            表示上一个月的枚举对象
        """
        if dt is None:
            dt = cls.local_now()

        return cls.offset_month(dt, -1)

    @classmethod
    def get_upcoming_day(cls, dt: datetime | date, weekday: Week) -> date:
        """
        获取指定日期的下一个指定星期的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期
        weekday : Week
            指定星期

        Returns
        -------
        date
            指定日期的下一个指定星期的日期
        """
        cnt_days_in_week = 7
        cleaned_dt = cls.get_cleaned_date(dt)
        current_weekday = dt.weekday()
        days_until_day = (
            cnt_days_in_week + weekday.get_value() - current_weekday
        ) % cnt_days_in_week or cnt_days_in_week

        return cleaned_dt + relativedelta(days=days_until_day)

    @classmethod
    def get_upcoming_monday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期一的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期一的日期
        """
        return cls.get_upcoming_day(dt, Week.MONDAY)

    @classmethod
    def get_upcoming_tuesday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期二的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期二的日期
        """
        return cls.get_upcoming_day(dt, Week.TUESDAY)

    @classmethod
    def get_upcoming_wednesday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期三的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期三的日期
        """
        return cls.get_upcoming_day(dt, Week.WEDNESDAY)

    @classmethod
    def get_upcoming_thursday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期四的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期四的日期
        """
        return cls.get_upcoming_day(dt, Week.THURSDAY)

    @classmethod
    def get_upcoming_friday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期五的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期五的日期
        """
        return cls.get_upcoming_day(dt, Week.FRIDAY)

    @classmethod
    def get_upcoming_saturday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期六的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期六的日期
        """
        return cls.get_upcoming_day(dt, Week.SATURDAY)

    @classmethod
    def get_upcoming_sunday(cls, dt: datetime | date) -> date:
        """
        获取指定日期的下一个星期日的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期

        Returns
        -------
        date
            指定日期的下一个星期日的日期
        """
        return cls.get_upcoming_day(dt, Week.SUNDAY)

    @classmethod
    def get_last_day(cls, dt: datetime | date, weekday: Week) -> date:
        """
        获取指定日期的上一个指定星期的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期
        weekday : Week
            指定星期

        Returns
        -------
        date
            指定日期的上一个指定星期的日期
        """
        cnt_days_in_week = 7
        cleaned_dt = cls.get_cleaned_date(dt)
        current_weekday = dt.weekday()

        days_until_day = (current_weekday - weekday.get_value()) % cnt_days_in_week

        return cleaned_dt - relativedelta(days=days_until_day)

    @classmethod
    def get_last_monday(cls, dt: datetime | date) -> date:
        """
        根据指定日期，获取上一个周一的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周一的日期
        """
        return cls.get_last_day(dt, Week.MONDAY)

    @classmethod
    def get_last_tuesday(cls, dt: datetime | date) -> date:
        """
        根据指定日期，获取上一个周二的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周二的日期
        """
        return cls.get_last_day(dt, Week.TUESDAY)

    @classmethod
    def get_last_wednesday(cls, dt: datetime | date) -> date:
        """
        根据指定的日期，获取上一个周三的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周三的日期
        """
        return cls.get_last_day(dt, Week.WEDNESDAY)

    @classmethod
    def get_last_thursday(cls, dt: datetime | date) -> date:
        """
        根据指定的日期，获取上一个周四的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周四的日期
        """
        return cls.get_last_day(dt, Week.THURSDAY)

    @classmethod
    def get_last_friday(cls, dt: datetime | date) -> date:
        """
        根据指定的日期，获取上一个周五的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周五的日期
        """
        return cls.get_last_day(dt, Week.FRIDAY)

    @classmethod
    def get_last_saturday(cls, dt: datetime | date) -> date:
        """
        根据指定的日期，获取上一个周六的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周六的日期
        """
        return cls.get_last_day(dt, Week.SATURDAY)

    @classmethod
    def get_last_sunday(cls, dt: datetime | date) -> date:
        """
        根据指定的日期，获取上一个周日的日期

        Parameters
        ----------
        dt : datetime | date
            指定的日期

        Returns
        -------
        date
            根据指定的日期，获取到的上一个周日的日期
        """
        return cls.get_last_day(dt, Week.SUNDAY)

    @classmethod
    def get_closest_weekday(cls, dt: datetime | date, weekday: Week) -> date:
        """
        获取指定日期的最近的指定星期的日期

        Parameters
        ----------
        dt : datetime | date
            指定日期
        weekday : Week
            指定星期

        Returns
        -------
        date
            指定日期的最近的指定星期的日期
        """
        dt = cls.get_cleaned_date(dt)
        last_weekday = cls.get_last_day(dt, weekday)
        upcoming_weekday = cls.get_upcoming_day(dt, weekday)

        if abs((dt - last_weekday).days) < abs((dt - upcoming_weekday).days):
            return last_weekday
        else:
            return upcoming_weekday

    @classmethod
    def get_closest_monday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期一的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期一的日期
        """
        return cls.get_closest_weekday(dt, Week.MONDAY)

    @classmethod
    def get_closest_tuesday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期二的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期二的日期
        """
        return cls.get_closest_weekday(dt, Week.TUESDAY)

    @classmethod
    def get_closest_wednesday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期三的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期三的日期
        """
        return cls.get_closest_weekday(dt, Week.WEDNESDAY)

    @classmethod
    def get_closest_thursday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期四的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期四的日期
        """
        return cls.get_closest_weekday(dt, Week.THURSDAY)

    @classmethod
    def get_closest_friday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期五的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期五的日期
        """
        return cls.get_closest_weekday(dt, Week.FRIDAY)

    @classmethod
    def get_closest_saturday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期六的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期六的日期
        """
        return cls.get_closest_weekday(dt, Week.SATURDAY)

    @classmethod
    def get_closest_sunday(cls, dt: datetime | date) -> date:
        """
        根据给定的日期，获取最近的星期日的日期

        Parameters
        ----------
        dt : datetime | date
            给定的日期

        Returns
        -------
        date
            根据给定的日期获取到的最近的星期日的日期
        """
        return cls.get_closest_weekday(dt, Week.SUNDAY)

    @classmethod
    def offset_year(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移年份

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        int
            偏移后的年份
        """
        return dt + relativedelta(years=offset)

    @classmethod
    def offset_quarter(cls, dt: datetime, offset: int) -> Quarter | None:
        """
        偏移季度

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        Quarter | None
            偏移后的季度枚举实例
        """
        new_dt = dt + relativedelta(months=3 * offset)
        return Quarter.get_quarter(new_dt)

    @classmethod
    def offset_month(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移月份

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        int
            偏移后的月份
        """
        return dt + relativedelta(months=offset)

    @classmethod
    def offset_week(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移周数

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(weeks=offset)

    @classmethod
    def offset_day(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移天数

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(days=offset)

    @classmethod
    def offset_hour(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移小时

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(hours=offset)

    @classmethod
    def offset_minute(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移分钟

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(minutes=offset)

    @classmethod
    def offset_second(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移秒数

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(seconds=offset)

    @classmethod
    def offset_millisecond(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移毫秒数

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(microseconds=offset * 1000)

    @classmethod
    def offset_microsecond(cls, dt: datetime, offset: int) -> datetime:
        """
        偏移微妙数

        Parameters
        ----------
        dt : datetime
            待偏移的日期
        offset : int
            偏移量

        Returns
        -------
        datetime
            偏移后的日期对象
        """
        return dt + relativedelta(microseconds=offset)

    @classmethod
    def between(cls, dt: datetime, other: datetime, time_unit: TimeUnit) -> int | float:
        """
        判断两个日期相差的时长，只保留绝对值

        Parameters
        ----------
        dt : datetime
            日期对象1
        other : datetime
            日期对象2
        time_unit : TimeUnit
            时间单位

        Returns
        -------
        int | float
            两个日期相差的时长
        """
        diff_in_seconds = (dt - other).total_seconds()
        return cls.convert_time(diff_in_seconds, TimeUnit.SECONDS, time_unit)

    @classmethod
    def between_days(
        cls,
        dt: datetime,
        other: datetime,
    ) -> int | float:
        """
        以天为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的天数
        """
        return cls.between(dt, other, TimeUnit.DAYS)

    @classmethod
    def between_hours(cls, dt: datetime, other: datetime) -> int | float:
        """
        以小时为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的小时数
        """
        return cls.between(dt, other, TimeUnit.HOURS)

    @classmethod
    def between_minutes(cls, dt: datetime, other: datetime) -> int | float:
        """
        以分钟为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的分钟数
        """
        return cls.between(dt, other, TimeUnit.MINUTES)

    @classmethod
    def between_seconds(cls, dt: datetime, other: datetime) -> int | float:
        """
        以秒为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的秒数
        """
        return cls.between(dt, other, TimeUnit.SECONDS)

    @classmethod
    def between_milliseconds(cls, dt: datetime, other: datetime) -> int | float:
        """
        以毫秒为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的毫秒数
        """
        return cls.between(dt, other, TimeUnit.MILLISECONDS)

    @classmethod
    def between_microseconds(cls, dt: datetime, other: datetime) -> int | float:
        """
        以微秒为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的微秒数
        """
        return cls.between(dt, other, TimeUnit.MICROSECONDS)

    @classmethod
    def between_nanoseconds(cls, dt: datetime, other: datetime) -> int | float:
        """
        以纳秒为单位返回两个日期的差值

        Parameters
        ----------
        dt : datetime
            日期1
        other : datetime
            日期2

        Returns
        -------
        int | float
            两个日期相差的纳秒数
        """
        return cls.between(dt, other, TimeUnit.NANOSECONDS)

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
        return False if date1 is None or date2 is None else date1.year == date2.year

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
    def is_weekend_by_dt(cls, dt: datetime) -> bool:
        """
        返回给定日期对象是否是周末

        Parameters
        ----------
        dt : datetime
            待检测日期对象

        Returns
        -------
        bool
            如果给定日期是周末, 则返回True,  否则返回False
        """
        week_obj = cls.get_day_of_week(dt)
        return week_obj in [Week.SATURDAY, Week.SUNDAY]

    @classmethod
    def is_weekend(
        cls,
        year: int,
        month: int,
        day: int,
    ) -> bool:
        """
        判断给定的日期是否是周末

        Parameters
        ----------
        year : int
            给定年
        month : int
            给定月
        day : int
            给定日

        Returns
        -------
        bool
            如果是周末则返回True, 否则返回False
        """
        return cls.is_weekend_by_dt(datetime(year, month, day))

    @classmethod
    def is_weekday_by_dt(cls, dt: datetime) -> bool:
        """
        返回是给定的dt对象是否是周一到周五

        Parameters
        ----------
        dt : datetime
            待检测dt对象

        Returns
        -------
        bool
            如果是周一到周五这返回True, 否则返回False
        """
        return not cls.is_weekend_by_dt(dt)

    @classmethod
    def is_weekday(cls, year: int, month: int, day: int) -> bool:
        """
        判断给定的日期是否是周一到周五

        Parameters
        ----------
        year : int
            给定年
        month : int
            给定月
        day : int
            给定日

        Returns
        -------
        bool
            如果是周一到周五这返回True, 否则返回False
        """
        return cls.is_weekday_by_dt(datetime(year, month, day))

    @classmethod
    def is_valid_year(cls, year: int) -> bool:
        """
        判断给定年份是否合规

        Parameters
        ----------
        year : int
            待检测年份

        Returns
        -------
        bool
            如果给定年份在 1900~9999 之间，则返回True, 否则返回False
        """
        return cls._is_range_contain(1900, dt_lib.MAXYEAR, year)

    @classmethod
    def is_valid_quarter(cls, quarter: Quarter | int) -> bool:
        """
        判断给定的季度是否合规

        Parameters
        ----------
        quarter : Quarter | int
            待检测季度

        Returns
        -------
        bool
            如果给定的季度在 1~4 之间，则返回True, 否则返回False
        """
        if isinstance(quarter, Quarter):
            quarter = quarter.get_value()
        return cls._is_range_contain(Quarter.get_min_value(), Quarter.get_max_value(), quarter)

    @classmethod
    def is_valid_month(cls, month: Month | int) -> bool:
        """
        判断给定的月份是否合规

        Parameters
        ----------
        month : Month | int
            待检测月份

        Returns
        -------
        bool
            如果给定的月份在 1~12 之间，则返回True, 否则返回False
        """
        if isinstance(month, Month):
            month = month.get_value()
        return cls._is_range_contain(Month.get_min_value(), Month.get_max_value(), month)

    @classmethod
    def is_valid_weekday(cls, day: int | Week) -> bool:
        """
        判断给定的星期是否合规

        Parameters
        ----------
        day : int | Week
            待检测的星期几

        Returns
        -------
        bool
            如果给定的星期在 1~7 之间，则返回True, 否则返回False
        """
        if isinstance(day, Week):
            day = day.get_iso8601_value()
        return cls._is_range_contain(Week.get_min_value(), Week.get_max_value(), day)

    @classmethod
    def is_valid_hour(cls, hour: int) -> bool:
        """
        判断给定的小时是否合规

        Parameters
        ----------
        hour : int
            待检测小时

        Returns
        -------
        bool
            如果给定的小时在 0~23 之间，则返回True, 否则返回False
        """
        return cls._is_range_contain(0, 23, hour)

    @classmethod
    def is_valid_minute(cls, minute: int) -> bool:
        """
        判断给定的分钟是否合规

        Parameters
        ----------
        minute : int
            待检测分钟

        Returns
        -------
        bool
            如果给定的分钟在 0~59 之间，则返回True, 否则返回False
        """
        return cls._is_range_contain(0, 59, minute)

    @classmethod
    def is_valid_second(cls, second: int) -> bool:
        """
        判断给定的秒是否合规

        Parameters
        ----------
        second : int
            待检测秒数

        Returns
        -------
        bool
            如果给定的秒数在 0~59 之间，则返回True, 否则返回False
        """
        return cls._is_range_contain(0, 59, second)

    @classmethod
    def is_valid_millisecond(cls, millisecond: int) -> bool:
        """
        判断给定的毫秒是否合规

        Parameters
        ----------
        millisecond : int
            待检测毫秒

        Returns
        -------
        bool
            如果给定的毫秒在 0~999 之间，则返回True, 否则返回False
        """
        return cls._is_range_contain(0, 999, millisecond)

    @classmethod
    def is_valid_datetime(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
    ) -> bool:
        """
        判断给定的日期时间是否合规

        Parameters
        ----------
        year : int
            待检测年份
        month : int
            待检测月份
        day : int
            待检测日
        hour : int
            待检测小时
        minute : int
            待检测分钟
        second : int
            待检测秒数

        Returns
        -------
        bool
            如果给定的日期时间在合规的范围内, 则返回True, 否则返回False
        """
        return cls.is_valid_date(year, month, day) and cls.is_valid_time(hour, minute, second)

    @classmethod
    def is_valid_date(cls, year: int, month: int, day: int) -> bool:
        """
        验证是否为生日

        Example:
        ----------
        >>> Validator.is_valid_date(1990, 1, 1) # returns True
        >>> Validator.is_valid_date(1990, 13, 1) # returns False

        Parameters
        ----------
        year : int
            年
        month : int
            月
        day : int
            日

        Returns
        -------
        bool
            如果是合法的日期, 则返回True, 否则返回False
        """

        # 判断年
        # NOTE datetime.MINYEAR的值是1, 这里的逻辑是否要修改
        if not cls.is_valid_year(year):
            return False

        # 判断月
        if month < 1 or month > 12:
            return False

        # 单独判断天
        if day < 1 or day > 31:
            return False

        # 处理30天的月
        if day > 30 and month in {4, 6, 9, 11}:
            return False

        # 处理闰年的情况
        if month == 2:
            return day < 29 or (day < 30 and DatetimeUtil.is_leap_year(year))

        return True

    @classmethod
    def is_valid_time(cls, hour: int, minute: int, second: int) -> bool:
        """
        验证是否为有效时间

        Example:
        ----------
        >>> Validator.is_valid_time(23, 59, 59) # returns True
        >>> Validator.is_valid_time(24, 0, 0) # returns False

        Parameters
        ----------
        hour : int
            小时
        minute : int
            分钟
        second : int
            秒

        Returns
        -------
        bool
            如果是合法的时间, 则返回True, 否则返回False
        """
        return cls.is_valid_hour(hour) and cls.is_valid_minute(minute) and cls.is_valid_second(second)

    @classmethod
    def has_tz(cls, dt: datetime) -> bool:
        """
        返回给定的日期对象是否含有时区信息

        Parameters
        ----------
        dt : datetime
            待判断日期对象

        Returns
        -------
        bool
            如果日期对象含有时区信息返回True, 否则返回False

        Notes:
        -------
        ref: https://github.com/RhetTbull/datetime-utils/blob/main/datetime_tzutils.py
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be a datetime object, but got {type(dt)}")
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None

    @classmethod
    def local_to_utc(cls, dt: datetime) -> datetime:
        """
        将 datetime 对象(带时区信息)转换成UTC时间

        Parameters
        ----------
        dt : datetime
            待转换的datetime对象

        Returns
        -------
        datetime
            转换后的datetime对象(UTC时间)

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 类型, 则抛出 TypeError 异常
        ValueError
            如果给定的对象没有时区信息, 则抛出 ValueError 异常

        Notes:
        -------
        ref: https://github.com/RhetTbull/datetime-utils/blob/main/datetime_tzutils.py
        """

        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        if cls.has_tz(dt):
            return dt.astimezone(tz=pytz.timezone("UTC"))
        else:
            raise ValueError("dt does not have timezone info")

    @classmethod
    def datetime_remove_tz(cls, dt: datetime) -> datetime:
        """
        删除时区信息

        Parameters
        ----------
        dt : datetime
            待删除的 datetime 对象

        Returns
        -------
        datetime
            删除时区信息后的 datetime 对象

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 对象, 则抛出异常
        """

        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        return dt.replace(tzinfo=None)

    @classmethod
    def utc_offset_seconds(cls, dt: datetime) -> int:
        """
        针对含有时区信息的 datetime 对象，以秒为单位返回与UTC的偏移量

        Parameters
        ----------
        dt : datetime
            待检测 datetime 对象

        Returns
        -------
        int
            以秒为单位返回与UTC的偏移量

        Raises
        ------
        TypeError
            如果给定的对象不是 datetime 对象, 则抛出异常
        ValueError
            如果 datetime 对象不包含时区信息, 则抛出异常
        """
        if not isinstance(dt, datetime):
            raise TypeError(f"dt must be type datetime.datetime, not {type(dt)}")

        if cls.has_tz(dt):
            return dt.tzinfo.utcoffset(dt).total_seconds()  # type: ignore
        else:
            raise ValueError("dt does not have timezone info")

    @classmethod
    def get_random_tz(cls) -> tzinfo:
        """
        获取随机时区
        :return: 随机时区
        """
        timezones = pytz.all_timezones

        random_tz = RandomUtil.get_random_item_from_sequence(timezones)
        return pytz.timezone(random_tz)  # type: ignore

    @classmethod
    def get_local_tz(cls) -> tzinfo | None:
        """
        获取默认时区
        :return: timezone实例
        """
        # 获取当前时间的UTC时间
        utc_time = datetime.now(pytz.utc)

        # 获取当前时区的时间
        local_time = utc_time.astimezone()

        # 获取当前时区
        return local_time.tzinfo

    @classmethod
    def get_random_date(cls, start: date | None = None, end: date | None = None) -> date:
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
        return start + timedelta(days=random_num_of_days)

    @classmethod
    def get_random_datetime(
        cls,
        start: datetime | None = None,
        end: datetime | None = None,
        *,
        random_tz: bool = False,
    ) -> datetime:
        """
        生成一个随机的 datetime 对象, 支持指定时间范围和随机时区。

        *Example*

        >>> cls.get_random_datetime(random_tz=True)
        datetime.datetime(1947, 12, 21, 9, 9, 39, tzinfo=<DstTzInfo 'Kwajalein' LMT+11:09:00 STD>)
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
        random_datetime = random_datetime.replace(hour=random_hour, minute=random_minute, second=random_second)
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
        seconds *= (datetime.resolution * 1e6).seconds
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
    def local_now(cls) -> datetime:
        """
        获取当前本地时间

        Returns
        -------
        datetime
            表示本地时间的 datetime 对象
        """
        tz = cls.get_local_tz()
        return datetime.now(tz)

    @classmethod
    def utc_to_local(cls, date_obj: datetime, tz: str) -> datetime:
        """
        UTC 时间转指定时区时间

        Parameters
        ----------
        date_obj : `datetime.datetime`
            待转换的 :py:class:`datetime.datetime` 对象
        tz : :obj:`str`, optional
            指定时区

        Returns
        -------
        :py:class:`datetime.datetime`
            转换后的 `datetime` 对象

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
    def get_age(cls, birthday: datetime, *, use_float_format: bool = False) -> int | float:
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
            return round(sub_days / 365, 1)

        age = now.year - birthday.year

        # NOTE 根据月、日判断是否对年龄 -1
        # ISSUE-1, 如果生日是闰年2-29, 则构建datetime对象时报错。
        # 这里的问题是如果是闰年，会出现2月29日，那么使用 9999-02-29 构建 datetime 对象会报错
        # 改为单独对月和日进行判断，不再构建datetime对象
        # birth_dt_with_fix_year = datetime(9999, birthday.month, birthday.day)
        # now_dt_with_fix_year = datetime(9999, now.month, now.day)

        if birthday.month > now.month or (birthday.month == now.month and birthday.day > now.day):
            age -= 1

        return age

    @classmethod
    def get_weeks_of_month(cls, year: int, month: int, start: int) -> int:
        raise NotImplementedError()

    @classmethod
    def nanos_to_seconds(cls, duration: int) -> float:
        """
        纳秒转秒
        :param duration: 时长
        :return: 秒
        """
        return cls.convert_time(duration, TimeUnit.NANOSECONDS, TimeUnit.SECONDS)

    @classmethod
    def nanos_to_millis(cls, duration: int) -> float:
        """
        纳秒转毫秒
        :param duration: 时长
        :return: 毫秒
        """
        return cls.convert_time(duration, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS)

    @classmethod
    def second_to_time(cls, seconds: int) -> str:
        """
        秒数转为时间格式(HH:mm:ss)
        :param seconds: 需要转换的秒数
        :return: 转换后的字符串
        """
        hour, other = divmod(seconds, 3600)
        minute = other / 60
        seconds = other % 60

        res_dt = datetime.now() + timedelta(hours=hour, minutes=minute, seconds=seconds)
        return res_dt.strftime("%H:%M:%S")

    @classmethod
    def get_day_of_week(cls, dt: datetime) -> Week | None:
        """
        根据日期获取星期枚举实例

        Parameters
        ----------
        dt : datetime
            待检测日期对象

        Returns
        -------
        Week | None
            根据日期对象返回的星期枚举实例, 如果日期对象为 None或者日期不合法, 则返回 None
        """
        if dt is None:
            return None
        day_of_week = dt.weekday()

        return Week.get_week(day_of_week + 1)

    @classmethod
    def get_week_monday_by_dt(cls, dt: datetime) -> datetime:
        """
        获取指定日期所在周的星期一日期

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        datetime
            日期所在周的星期一日期
        """
        return None if dt is None else dt - relativedelta(days=dt.weekday())

    @classmethod
    def get_hour_from_dt(cls, dt: datetime) -> str:
        """
        获取指定日期的小时字符串

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        str
            指定日期的小时数
        """
        return cls._process_leading_zeros(dt.strftime("%I")) if dt is not None else ""

    @classmethod
    def get_24_hour_from_dt(cls, dt: datetime) -> str:
        """
        获取指定日期的小时字符串(24小时制)

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        str
            指定日期的小时数(24小时制)
        """
        return cls._process_leading_zeros(dt.strftime("%H")) if dt is not None else ""

    @classmethod
    def get_minute_from_dt(cls, dt: datetime) -> str:
        """
        获取指定日期的分钟字符串

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        str
            指定日期对象的分钟字符串
        """
        return cls._process_leading_zeros(str(dt.minute)) if dt is not None else ""

    @classmethod
    def get_second_from_dt(cls, dt: datetime) -> str:
        """
        获取指定日期的秒字符串

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        str
            指定日期对象的秒字符串
        """
        return cls._process_leading_zeros(str(dt.second)) if dt is not None else ""

    @classmethod
    def get_am_or_pm_from_dt(cls, dt: datetime) -> str:
        """
        返回给定日期对象表示的上午还是下午

        Parameters
        ----------
        dt : datetime
            待获取日期对象

        Returns
        -------
        str
            如果日期对象表示的时刻是上午, 则返回 "AM", 如果日期对象表示的时刻是下午, 则返回 "PM"
        """
        return dt.strftime("%p").upper()

    @classmethod
    def get_time_24_from_dt(
        cls,
        dt: datetime,
        *,
        show_seconds: bool = True,
    ) -> str:
        """
        获取指定日期的24小时制时间字符串

        Parameters
        ----------
        dt : datetime
            待获取日期对象
        show_seconds : bool, optional
            是否显示秒, 默认为 True

        Returns
        -------
        str
            指定日期对象的24小时制时间字符串
        """
        format_str = "%H:%M:%S" if show_seconds else "%H:%M"
        return dt.strftime(format_str) if dt is not None else ""

    @classmethod
    def get_time_from_dt(
        cls,
        dt: datetime,
        *,
        show_seconds: bool = True,
    ) -> str:
        """
        获取指定日期的12小时制时间字符串

        Parameters
        ----------
        dt : datetime
            待获取日期对象
        show_seconds : bool, optional
            是否显示秒, 默认为 True

        Returns
        -------
        str
            指定日期对象的12小时制时间字符串
        """
        format_str = "%I:%M:%S %p" if show_seconds else "%I:%M %p"
        return dt.strftime(format_str) if dt is not None else ""

    @classmethod
    def get_cleaned_datetime(cls, day: datetime | date) -> datetime:
        """
        返回一个干净的 :py:class:`datetime.datetime` 对象, \n
        * 可以保证原始 :py:class:`datetime.datetime` 对象不变, 只返回 :py:class:`datetime.datetime` 对象
        * 可以将任何 datetime 的鸭子类型转换成 datetime 对象

        Parameters
        ----------
        day : datetime | date
            待转换对象

        Returns
        -------
        datetime
            转换后干净的对象

        Raises
        ------
        UnsupportedDateType
            如果给定的对象不是 date 或 datetime 类型, 则抛出 UnsupportedDateType 异常
        """
        if not isinstance(day, (date | datetime)):
            raise UnsupportedDateType(f"`{day}` is of unsupported type ({type(day)})")
        if isinstance(day, datetime):
            return day
        if isinstance(day, date):
            day = datetime.combine(day, datetime.min.time())
        return datetime.fromtimestamp(day.timestamp())

    @classmethod
    def get_cleaned_date(
        cls,
        day: datetime | date,
        keep_datetime=False,
    ) -> date:
        """
        返回一个"干净"的 :py:class:`datetime.date` 对象, \n
        * 可以保证原始 :py:class:`datetime.datetime` 或者 :py:class:`datetime.date` 对象不变,
            只返回 :py:class:`datetime.date` 对象
        * 可以将任何 date 的鸭子类型转换成 date 对象

        Parameters
        ----------
        day : datetime | date
            待转换对象
        keep_datetime : bool, optional
            如果是 datetime 对象, 是否保留时间信息和时区信息, by default False

        Returns
        -------
        date
            转换后的 date 类型

        Raises
        ------
        UnsupportedDateType
            如果给定的对象不是 date 或 datetime 类型, 则抛出 UnsupportedDateType 异常

        NOTES:
        ------
        ref: https://github.com/workalendar/workalendar/blob/b131f2b64377e951654652a9a32e72a34f34e88f/workalendar/core.py#L35
        """
        if not isinstance(day, (date | datetime)):
            raise UnsupportedDateType(f"`{day}` is of unsupported type ({type(day)})")
        if not keep_datetime and (hasattr(day, "date") and callable(day.date)):
            day = day.date()
        return day

    @classmethod
    def get_all_dates_in_year(cls, year: int) -> list[date]:
        """
        获取指定年份的所有日期

        Parameters
        ----------
        year : int
            待获取年份

        Returns
        -------
        list[date]
            指定年份的所有日期
        """
        return [
            date(year, month, day) for month in range(1, 13) for day in range(1, cls.days_in_month(year, month) + 1)
        ]

    @classmethod
    def get_all_mondays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期一日期

        Parameters
        ----------
        year : int
            给定的年份

        Returns
        -------
        list[date]
            给定年份的所有星期一日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.MONDAY.get_value()]

    @classmethod
    def get_all_tuesdays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期二日期

        Parameters
        ----------
        year : int
            给定的年份

        Returns
        -------
        list[date]
            给定年份的所有星期二日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.TUESDAY.get_value()]

    @classmethod
    def get_all_wednesdays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期三日期

        Parameters
        ----------
        year : int
            给定的年份

        Returns
        -------
        list[date]
            给定年份的所有星期三日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.WEDNESDAY.get_value()]

    @classmethod
    def get_all_thursdays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期四日期

        Parameters
        ----------
        year : int
            给定年份

        Returns
        -------
        list[date]
            给定年份的所有星期四日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.THURSDAY.get_value()]

    @classmethod
    def get_all_fridays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期五日期

        Parameters
        ----------
        year : int
            给定年份

        Returns
        -------
        list[date]
            给定年份的所有星期五日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.FRIDAY.get_value()]

    @classmethod
    def get_all_saturdays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期六日期

        Parameters
        ----------
        year : int
            给定年份

        Returns
        -------
        list[date]
            给定年份的所有星期六日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.SATURDAY.get_value()]

    @classmethod
    def get_all_sundays_in_year(cls, year: int) -> list[date]:
        """
        获取给定年份的所有星期日日期

        Parameters
        ----------
        year : int
            给定年份

        Returns
        -------
        list[date]
            给定年份的所有星期日日期
        """
        return [i for i in cls.get_all_dates_in_year(year) if i.weekday() == Week.SUNDAY.get_value()]

    @classmethod
    def convert_time(cls, value: int | float, from_unit: TimeUnit, to_unit: TimeUnit) -> int | float:
        """
        根据给定的时间单位转换时间

        Parameters
        ----------
        value : int | float
            待转换时间值
        from_unit : TimeUnit
            初始时间单位
        to_unit : TimeUnit
            目标时间单位

        Returns
        -------
        int | float
            转换后的时间值

        Raises
        ------
        ValueError
            如果 from_unit 或 to_unit 为 None, 则抛出 ValueError
        """
        if value is None or from_unit is None or to_unit is None:
            raise ValueError("value cannot be None")

        return value * from_unit.value.unit_val_in_ns / to_unit.value.unit_val_in_ns

    @classmethod
    def datetime_to_ISO8601(cls, dt: datetime) -> str:
        """
        将datetime对象转换为ISO8601格式的字符串

        Parameters
        ----------
        dt : datetime
            待转换的datetime对象

        Returns
        -------
        str
            转换后的字符串
        """
        return dt.isoformat() if dt is not None else ""

    @classmethod
    def parse_period(cls, period: str) -> relativedelta:
        """
        解析周期字符串, 如 "1D" 表示1天, "2W" 表示2周, "3M" 表示3个月, "4Y" 表示4年

        Examples
        --------
        >>> parse_period("1D")
        datetime.timedelta(days=1)
        >>> parse_period("2W")
        datetime.timedelta(days=14)
        >>> parse_period("15m")
        timedelta(minutes=15)
        >>> parse_period("1W")
        timedelta(weeks=1)

        Parameters
        ----------
        period : str
            代表时间间隔的字符串

        Returns
        -------
        timedelta
            timedelta对象,表示时间间隔

        Notes
        -----
        ref: https://gist.github.com/dsakovych/c1714d0c17ac0955c4b3149d42f34af5
        """
        value = int(period[:-1])
        unit = period[-1].lower()
        if unit not in cls.UNITS:
            raise ValueError(f"Invalid unit: {unit}")
        kwargs = {cls.UNITS[unit]: value}
        return relativedelta(**kwargs)

    @classmethod
    def generate_dt_range(
        cls,
        start: str,
        end: str,
        period: str,
    ) -> Generator[datetime, None, None]:
        """
        产生时间 datetime 序列

        Parameters
        ----------
        start : str
            起始时间，格式为 ISO 8601
        end : str
            结束时间，格式为 ISO 8601
        period : str
            时间周期

        Yields
        ------
        Generator[datetime, None, None]
            datetime 对象生成器
        """
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        period_delta = cls.parse_period(period)

        current_dt = start_dt

        while current_dt < end_dt:
            yield current_dt
            current_dt = min(current_dt + period_delta, end_dt)
            if current_dt >= end_dt:
                break

    @classmethod
    def check_and_get_year(cls, year: int) -> int:
        return cls._check_range_or_raise(1900, dt_lib.MAXYEAR, year)

    @classmethod
    def check_and_get_quarter(cls, quarter: int) -> int:
        """
        检查并获取季度值

        Parameters
        ----------
        quarter : int
            待检查的季度值

        Returns
        -------
        int
            如果是合法的季度值, 则返回季度值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的季度值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(1, 4, quarter)

    @classmethod
    def check_and_get_month(cls, month: int) -> int:
        """
        检查并获取月份值

        Parameters
        ----------
        month : int
            待检测月份值

        Returns
        -------
        int
            如果是合法的月份值, 则返回月份值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的月份值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(1, 12, month)

    @classmethod
    def check_and_get_weekday(cls, weekday: int) -> int:
        """
        检查并获取星期值

        Parameters
        ----------
        weekday : int
            待检测星期值

        Returns
        -------
        int
            如果是合法的星期值, 则返回星期值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的星期值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(1, 7, weekday)

    @classmethod
    def check_and_get_day(cls, year: int, month: int, day: int) -> int:
        """
        检查并获取日期值

        Parameters
        ----------
        year : int
            待检测年份
        month : int
            待检测月份
        day : int
            待检测日

        Returns
        -------
        int
            如果是合法的日期值, 则返回日期值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的日期值不合法, 则抛出 ValueError
        """
        if cls.is_valid_date(year, month, day):
            return day
        raise ValueError(f"wrong date {year}-{month}-{day}")

    @classmethod
    def check_and_get_hour(cls, hour: int) -> int:
        """
        检查并获取小时值

        Parameters
        ----------
        hour : int
            待检测小时值

        Returns
        -------
        int
            如果是合法的小时值, 则返回小时值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的小时值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(0, 23, hour)

    @classmethod
    def check_and_get_minute(cls, minute: int) -> int:
        """
        检查并获取分钟值

        Parameters
        ----------
        minute : int
            待检测分钟值

        Returns
        -------
        int
            如果是合法的分钟值, 则返回分钟值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的分钟值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(0, 59, minute)

    @classmethod
    def check_and_get_second(cls, second: int) -> int:
        """
        检查并获取秒值

        Parameters
        ----------
        second : int
            待检测秒值

        Returns
        -------
        int
            如果是合法的秒值, 则返回秒值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的秒值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(0, 59, second)

    @classmethod
    def check_and_get_millisecond(cls, millisecond: int) -> int:
        """
        检查并获取毫秒值

        Parameters
        ----------
        millisecond : int
            待检测毫秒值

        Returns
        -------
        int
            如果是合法的毫秒值, 则返回毫秒值, 否则抛出 ValueError

        Raises
        ------
        ValueError
            如果给定的毫秒值不合法, 则抛出 ValueError
        """
        return cls._check_range_or_raise(0, 999, millisecond)

    @classmethod
    def round_datetime(cls, dt: datetime, round_to: str) -> datetime:
        round_to = round_to.strip().lower()

        return dt

    @classmethod
    def nth_day_of_month(cls, *, year: int, month: int, weekday: int, n: int) -> date:
        """
        返回给定日期的第n个星期几的日期

        Parameters
        ----------
        year : int
            给定的年
        month : int
            给定的月
        weekday : int
            给定的周记
        n : int
            给定的第n个星期几

        Returns
        -------
        date | None
            给定日期的第n个星期几的日期

        Raises
        ------
        IndexError
            如果月份或星期数不合法, 则抛出异常

        Notes
        -----
        ref: https://github.com/fitnr/convertdate
        """

        if not 0 <= n <= 5:
            raise IndexError(f"Nth day of month must be 0-5. Received: {n}")

        month_obj: Month | None = Month.get_month(month)
        weekday_obj = Week.get_week(weekday)

        if month_obj is None:
            raise IndexError("month is out of range, must be 1-12")

        if weekday_obj is None:
            raise IndexError("weekday is out of range, must be 1-7")

        return cls._nth_day_of_month_obj(year, month_obj, weekday_obj, n)

    @classmethod
    def _nth_day_of_month_obj(cls, year: int, month_obj: Month, weekday_obj: Week, n: int) -> date:
        month = month_obj.get_value()
        weekday = weekday_obj.get_value()

        first_day, days_in_month = calendar.monthrange(year, month)
        # 获取当月第一个给定 weekday 是几号
        # 例如2024-08 第一个周一是2024-08-05， 第一个周四是1号
        first_weekday_of_kind = 1 + (weekday - first_day) % 7

        if n == 0:
            if first_weekday_of_kind in [1, 2, 3] and first_weekday_of_kind + 28 <= days_in_month:
                n = 5
            else:
                n = 4

        day = first_weekday_of_kind + ((n - 1) * 7)
        if day > days_in_month:
            raise IndexError(f"No {n}th day of month {month}")

        return date(year, month, day)

    @classmethod
    def parse(cls, date_str: str) -> datetime:
        if StringUtil.is_blank(date_str):
            return datetime.max
        date_str = StringUtil.remove_all(date_str, "年", "月", "日", "时", "分", "秒")
        # TODO 纯数字的日期格式解析
        # TODO 当初的时间格式
        # TODO CST时间格式
        # TODO UTC时间格式
        # TODO 标准日期格式
        return datetime.strptime(date_str, "%Y%m%d%H%M%S")

    @classmethod
    def _cyclic_acquire(cls, val: int, max_val: int, offset: int):
        return (val + offset) % max_val

    @classmethod
    def _check_range_or_raise(cls, min_val: int, max_val: int, val: int) -> int:
        if cls._is_range_contain(min_val, max_val, val):
            return val
        raise ValueError(f"value must be between {min_val} and {max_val}, but got {val}")

    @classmethod
    def _is_range_contain(cls, min_val: int, max_val: int, val: int) -> bool:
        return min_val <= val <= max_val

    @classmethod
    def _process_leading_zeros(cls, time_value: str) -> str:
        return time_value.zfill(2)

    @classmethod
    def is_valid_birthday(cls, birthday: str) -> bool:
        """
        验证是否为生日, 目前支持yyyy-MM-dd、yyyyMMdd、yyyy/MM/dd、yyyy.MM.dd、yyyy年MM月dd日

        Example:
        ----------
        >>> Validator.is_valid_birthday('1990-01-01') # returns True
        >>> Validator.is_valid_birthday('19900101') # returns True
        >>> Validator.is_valid_birthday('1990/01/01') # returns True
        >>> Validator.is_valid_birthday('1990.01.01') # returns True
        >>> Validator.is_valid_birthday('1990年01月01日') # returns True
        >>> Validator.is_valid_birthday('1990-13-01') # returns False
        >>> Validator.is_valid_birthday('1990-02-29') # returns False (非闰年)
        >>> Validator.is_valid_birthday('1990-02-30') # returns False (非30天的月份)

        Parameters
        ----------
        birthday : str
            待检测日期

        Returns
        -------
        bool
            如果是合法的生日, 则返回True, 否则返回False
        """

        if _ := ReUtil.is_match(PatternPool.BIRTHDAY_PATTERN, birthday):
            year = int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 1))
            month = int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 3))
            day = int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 5))
            return DatetimeUtil.is_valid_date(year, month, day)  # type: ignore
        return False


class NumberUtil:
    @classmethod
    def add(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确加法

        Returns
        -------
        Decimal
            加法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result += Decimal(arg)
        return result

    @classmethod
    def sub(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确减法

        Returns
        -------
        Decimal
            减法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result -= Decimal(arg)
        return result

    @classmethod
    def mul(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确乘法

        Returns
        -------
        Decimal
            乘法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result *= Decimal(arg)
        return result

    @classmethod
    def div(cls, *args) -> Decimal:
        """
        使用 Decimal 实现的精确除法

        Returns
        -------
        Decimal
            除法结果
        """
        if not args:
            return Decimal(0)

        result = Decimal(args[0])
        for arg in args[1:]:
            result /= Decimal(arg)
        return result


class ReUtil:
    # 正则表达式匹配中文汉字
    RE_CHINESE = RegexPool.CHINESE
    # 正则表达式匹配中文字符串
    RE_CHINESES = RegexPool.CHINESES
    # 正则中需要被转义的关键字
    RE_KEY = {
        "$",
        "(",
        ")",
        "*",
        "+",
        ".",
        "[",
        "]",
        "?",
        "\\",
        "^",
        "{",
        "}",
        "|",
        ":",
        "<",
        ">",
        "=",
    }

    @classmethod
    def get_group_1(cls, pattern: re.Pattern, s: str) -> str | None:
        """
        获取匹配的第一个分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回第一个分组的字符串, 否则返回None

        Notes
        ----------
        1. 依赖于`get_matched_group_by_idx`方法
        """
        cls.is_match(pattern, s, raise_exception=False)
        return cls.get_matched_group_by_idx(pattern, s, 1)

    @classmethod
    def get_group_2(cls, pattern: re.Pattern, s: str) -> str | None:
        """
        获取匹配的第二个分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回第二个分组的字符串, 否则返回None

        Notes
        ----------
        1. 依赖于`get_matched_group_by_idx`方法
        """
        cls.is_match(pattern, s, raise_exception=False)
        return cls.get_matched_group_by_idx(pattern, s, 2)

    @classmethod
    def get_matched_group_by_idx(
        cls,
        pattern: re.Pattern,
        s: str,
        group_index: int = 1,
    ) -> str | None:
        """
        获取指定的分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待提取字符串
        group_index : int, optional
            分组序号, by default 0

        Returns
        -------
        typing.Optional[str]
            如果匹配成功, 返回指定分组的字符串, 否则返回None

        Notes
        ----------
        1. 如果没有匹配, 返回None, 如果给定的分组序号大于分组数量-1, 也返回None
        2. 如果字符串为空, 也返回None
        """
        if StringUtil.is_blank(s):
            return None
        res = cls.get_matched_groups(pattern, s)
        return SequenceUtil.get_element(res, group_index - 1)

    @classmethod
    def get_matched_groups(cls, pattern: re.Pattern, s: str) -> tuple[str, ...]:
        """
        获取所有匹配的分组

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串

        Returns
        -------
        _type_
            所有匹配的分组
        """
        matched = pattern.match(s)
        return matched.groups() if matched is not None else ()

    @classmethod
    def get_match_obj(cls, pattern: re.Pattern, s: str) -> re.Match | None:
        """
        获取匹配对象

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串

        Returns
        -------
        typing.Optional[re.Match]
            如果匹配成功, 返回匹配对象, 否则返回None
        """
        return pattern.match(s)

    @classmethod
    def get_match_group(
        cls,
        pattern: re.Pattern,
        s: str,
    ) -> dict[str, T] | None:
        match_obj = cls.get_match_obj(pattern, s)
        return dict(match_obj.groupdict()) if match_obj is not None else None

    @classmethod
    def is_match(cls, pattern: re.Pattern, s: str, *, raise_exception: bool = False) -> bool:
        """
        检查是否匹配

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串
        raise_exception : bool, optional
            如果匹配失败, 是否抛出异常, by default False

        Returns
        -------
        bool
            如果匹配成功, 返回True, 如果匹配失败, 且raise_error为True, 抛出异常, 否则返回False

        Raises
        ------
        TypeError
            如果pattern不是re.Pattern对象抛出异常
        ValueError
            如果raise_error为True, 且匹配失败, 抛出ValueError异常
        """

        if not isinstance(pattern, re.Pattern):
            raise TypeError("pattern must be a re.Pattern object")

        res = pattern.match(s)
        if res is None and raise_exception:
            raise RegexValidationError(pattern, s, f"pattern {pattern} not match string {s}")

        return res is not None

    @classmethod
    def is_contains(cls, pattern: re.Pattern, s: str, *, raise_exception: bool = False) -> bool:
        """
        检查是否包含

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串
        raise_exception : bool, optional
            如果匹配失败, 是否抛出异常, by default False

        Returns
        -------
        bool
            如果匹配成功, 返回True, 如果匹配失败, 且raise_error为True, 抛出异常, 否则返回False

        Raises
        ------
        TypeError
            如果pattern不是re.Pattern对象抛出异常
        ValueError
            如果raise_error为True, 且匹配失败, 抛出ValueError异常
        """

        if not isinstance(pattern, re.Pattern):
            raise TypeError("pattern must be a re.Pattern object")

        res = pattern.search(s)
        if res is None and raise_exception:
            raise RegexValidationError(pattern, s, f"pattern {pattern} not match string {s}")

        return res is not None

    @classmethod
    def is_match_reg(cls, s: str, reg: str, *, raise_exception: bool = False) -> bool:
        """
        是否匹配正则表达式

        Parameters
        ----------
        s : str
            待匹配字符串
        reg : str
            待匹配正则表达式
        raise_exception : bool, optional
            匹配不成功是否引发异常, by default False

        Returns
        -------
        bool
            是否匹配成功
        """
        pattern = re.compile(reg)
        return cls.is_match(pattern, s, raise_exception=raise_exception)

    @classmethod
    def find_all(cls, pattern: re.Pattern, s: str, from_index: int = 0) -> list[str]:
        """
        找到所有匹配的字符串

        Parameters
        ----------
        pattern : re.Pattern
            编译后的正则模式
        s : str
            待匹配字符串

        Returns
        -------
        list[str]
            所有匹配的字符串列表
        """
        return pattern.findall(s, from_index)
