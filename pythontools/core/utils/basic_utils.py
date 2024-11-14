# Copyright 2024 The pythontools Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
import collections
import functools
import itertools as it
import os
import random
import re
import string
import sys
import typing as t
import unicodedata
from collections.abc import Generator, Mapping, Sequence, Set

from ..__typing import K, T
from ..constants.pattern_pool import PatternPool, RegexPool
from ..constants.string_constant import CharPool, CharsetUtil, Strategy
from ..decorator import UnCheckFunction
from ..errors import RegexValidationError
from .boolean_utils import BooleanUtil
from .random_utils import RandomUtil

_Tin = t.TypeVar("_Tin")
_Tout = t.TypeVar("_Tout")
_K = t.TypeVar("_K")


class SequenceUtil:
    EMPTY: t.Final[str] = CharPool.EMPTY
    SPACE: t.Final[str] = CharPool.SPACE
    INDEX_NOT_FOUND: t.Final[int] = -1

    @classmethod
    def is_empty(cls, seq: t.Sized) -> bool:
        """
        返回序列是否为空。

        Example:
        >>> SequenceUtil.is_empty(None) # True
        >>> SequenceUtil.is_empty([]) # True
        >>> SequenceUtil.is_empty([1, 2, 3]) # False

        Parameters
        ----------
        sequence : t.Sized[Any]
            待检测序列

        Returns
        -------
        bool
            如果序列为空返回True, 否则返回False
        """
        return seq is None or len(seq) == 0

    @classmethod
    def is_not_empty(cls, seq: t.Sized) -> bool:
        """
        返回序列是否为非空

        Parameters
        ----------
        sequence : t.Sized[Any]
            待检测序列

        Returns
        -------
        bool
            如果序列为非空返回True, 否则返回False
        """
        return not cls.is_empty(seq)

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
    def contains_any(
        cls,
        it: t.Iterable[T],
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
        return any(i in it for i in args)

    @classmethod
    def contains_all(
        cls,
        it: t.Iterable[T],
        *args,
    ) -> bool:
        """
        检查序列是否包含所有给定元素

        Example:
        ----------
        >>> SequenceUtil.contains_all([1, 2, 3], 2, 3) # True
        >>> SequenceUtil.contains_all([1, 2, 3], 2, 4) # False

        Parameters
        ----------
        sequence : t.Sequence[Any]
            待检测序列
        args : Any
            任意数量的元素, 用于检测是否包含其中之一

        Returns
        -------
        bool
            如果包含args中的所有元素返回True, 否则返回False
        """
        return all(i in it for i in args)

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
    def is_only(cls, it: t.Iterable[T]) -> bool:
        """
        判断一个可迭代对象是否只包含一个元素

        Parameters
        ----------
        it : t.Iterable[T]
            待判断的可迭代对象

        Returns
        -------
        bool
            如果可迭代对象只包含一个元素返回 True, 否则返回 False
        """
        if isinstance(it, t.Sized):
            return len(it) == 1

        lst = tuple(it.islice(it, 2))
        return bool(lst and len(lst) == 1)

    @classmethod
    def has_none(cls, sequence: t.Sequence[T]) -> bool:
        """
        返回序列是否含有 None 元素

        Parameters
        ----------
        sequence : t.Sequence[T]
            待检测序列

        Returns
        -------
        bool
            如果序列含有 None 元素返回 True, 否则返回 False
        """
        return any(item is None for item in sequence)

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
    def get_element(cls, it: t.Iterable[T], idx: int) -> T:
        """
        从序列中获取指定索引的元素, 如果索引越界则返回None

        Parameters
        ----------
        seq : t.Sequence[T]
            待获取的序列
        idx : int
            索引

        Returns
        -------
        T
            序列中指定索引的元素, 如果索引越界则返回None
        """
        if isinstance(it, t.Sequence):
            return it[idx] if idx < len(it) else None
        else:
            return next(iter.islice(it, idx, None), None)

    @classmethod
    def reverse_sequence(cls, seq: t.Sequence[T]) -> t.Sequence:
        """
        翻转序列，不会影响原序列

        Parameters
        ----------
        sequence : t.Sequence[T]
            待翻转序列

        Returns
        -------
        t.Sequence
            翻转后的序列
        """
        return seq[::-1]

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
    def first_idx_of_none(cls, seq: t.Sequence[T]) -> int:
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

        return cls.first_index_of(
            seq,
            0,
            None,
        )

    @classmethod
    def last_idx_of_none(cls, seq: t.Sequence[T]) -> int:
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
        return cls.last_index_of(
            seq,
            len(seq) - 1,
            None,
        )

    @t.overload
    def first_index_of(
        cls,
        seq: t.Sequence[T],
        from_idx: int,
        predicate: t.Callable[[T], bool],
    ) -> int: ...

    @t.overload
    def first_index_of(
        cls,
        seq: t.Sequence[T],
        from_idx: int,
        predicate: T,
    ) -> int: ...

    @classmethod
    def first_index_of(
        cls,
        seq: t.Sequence[T],
        from_idx: int,
        predicate,
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

        if cls.is_empty(seq):
            return cls.INDEX_NOT_FOUND
        if not isinstance(predicate, t.Callable):
            target_val = predicate

            def predicate(x):
                return x == target_val

        from_idx = max(from_idx, 0)

        return next(
            (index for index in range(from_idx, len(seq)) if predicate(seq[index])),
            cls.INDEX_NOT_FOUND,
        )

    @t.overload
    def last_index_of(
        cls,
        seq: t.Sequence[T],
        from_idx: int,
        predicate: t.Callable[[T], bool],
    ) -> int: ...

    @t.overload
    def last_index_of(
        cls,
        from_idx: int,
        predicate: T,
    ) -> int: ...

    @classmethod
    def last_index_of(
        cls,
        seq: Sequence[T],
        from_idx: int,
        predicate,
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

        if cls.is_empty(seq):
            return cls.INDEX_NOT_FOUND

        if not isinstance(predicate, t.Callable):
            target_val = predicate

            def predicate(x):
                return x == target_val

        from_idx = min(from_idx, len(seq) - 1)

        return next(
            (index for index in range(from_idx, -1, -1) if predicate(seq[index])),
            cls.INDEX_NOT_FOUND,
        )

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
    def remove_none(cls, it: t.Iterable[T]) -> list[T]:
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
        return cls.remove_item(it, None)

    @classmethod
    def remove_false(cls, it: t.Iterable[T]) -> list[T]:
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
        return cls.remove_item(it, BooleanUtil.is_false)

    @t.overload
    def remove_item(
        cls,
        it: t.Iterable[T],
        predicate: t.Callable[[T], bool],
    ) -> list[T]: ...

    @t.overload
    def remove_item(
        cls,
        it: t.Iterable[T],
        predicate: T,
    ) -> list[T]: ...

    @classmethod
    def remove_item(
        cls,
        it: t.Iterable[T],
        predicate,
    ) -> list[T]:
        """
        从可迭代对象中移除指定元素

        Parameters
        ----------
        it : t.Iterable[T]
            待处理可迭代对象
        predicate : T | t.Callable[[T], bool]
            待移除元素的条件

        Returns
        -------
        list[T]
            移除指定元素后的新列表
        """
        if not isinstance(predicate, t.Callable):
            target_val = predicate

            def predicate(x) -> bool:
                return x == target_val

        return [i for i in it if not predicate(i)]

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
        it: t.Iterable[T],
        predicate: t.Callable[[T], bool],
        default_val: T = None,
    ) -> T | None:
        """
        从可迭代对象中返回第一个符合条件的元素

        Parameters
        ----------
        it : t.Iterable[Any]
            待提取可迭代对象
        func : t.Callable[[Any], bool]
            检测函数
        default_val : Any, optional
            返回默认值, by default None

        Returns
        -------
        Any
            如果存在则返回第一个符合条件的对象, 否则返回默认值
        """
        gen = cls.filtered_elements(it, predicate)
        return next(gen, default_val)

    @classmethod
    def get_last_match(
        cls,
        it: t.Iterable[T],
        predicate: t.Callable[[T], bool],
        default_val: T = None,
    ) -> T | None:
        """
        从可迭代对象中返回最后一个符合条件的元素

        Parameters
        ----------
        it : t.Iterable[T]
            待提取可迭代对象
        predicate : t.Callable[[T], bool]
            检测函数
        default_val : T, optional
            默认值, by default None

        Returns
        -------
        T | None
            如果存在则返回最后一个符合条件的对象, 否则返回默认值
        """
        gen: Generator[T, None, None] = cls.filtered_elements(it, predicate)
        tmp = None
        for i in gen:
            tmp = i
        return tmp if tmp is not None else default_val

    @classmethod
    def filtered_elements(
        cls,
        it: t.Iterable[T],
        predicate: t.Callable[[T], bool],
    ) -> t.Generator[T, None, None]:
        """
        获取可迭代对象中所有符合条件的元素

        Parameters
        ----------
        it : t.Iterable[T]
            待提取可迭代对象
        predicate : t.Callable[[T], bool]
            检测函数

        Returns
        -------
        list[T]
            符合条件的元素组成的列表
        """
        yield from (i for i in it if predicate(i))

    @classmethod
    def split_by(
        cls,
        it: t.Iterable[T],
        predicate: t.Callable[[T], bool],
    ) -> tuple[t.Sequence[T], t.Sequence[T]]:
        """
        将可迭代对象根据predicate函数的返回值进行分割

        Parameters
        ----------
        it : t.Iterable[T]
            待分割可迭代对象
        predicate : t.Callable[[T], bool]
            分割函数, 返回True则分割为左半部分, 否则分割为右半部分

        Returns
        -------
        tuple[t.Sequence[T], t.Sequence[T]]
            分割后的两个部分，第一部分为满足predicate函数的元素，第二部分为不满足predicate函数的元素
        """
        false_list = []
        true_list = []
        for v in it:
            if predicate(v):
                true_list.append(v)
            else:
                false_list.append(v)
        return false_list, true_list

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
        return cls.split_seq(seq, 2)

    @classmethod
    def split_seq(
        cls,
        seq: t.Sequence[T],
        cnt_of_group: int,
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
        if cnt_of_group <= 0:
            raise ValueError("num_of_group should be greater than 0")

        length = cls.get_length(seq)
        if cnt_of_group == 1:
            return [seq]

        if length <= cnt_of_group:
            return [[i] for i in seq]

        cnt_of_group = int(length / cnt_of_group)
        out = []
        split_cnt_lst = []
        tmp = 0
        while tmp + cnt_of_group <= length:
            split_cnt_lst.append(cnt_of_group)
            tmp += cnt_of_group

        split_cnt_lst[-1] += length - tmp

        last = 0
        for i in split_cnt_lst:
            out.append(seq[last : last + i])
            last += i

        return out

    @classmethod
    def groupby(
        cls,
        it: t.Iterable[T],
        *,
        key_func: t.Callable[[T], _K],
        val_func: t.Callable[[T], _Tout] = None,
    ) -> dict[_K, list[_Tout]]:
        """
        根据给定的key_func和val_func, 将可迭代对象分组

        Parameters
        ----------
        it : t.Iterable[Any]
            待分组可迭代对象
        key_func : t.Callable[[Any], Any]
            键函数, 用于提取键值
        val_func : t.Callable[[Any], Any], optional
            值函数, 用于提取值, by default None

        Returns
        -------
        dict[Any, list[Any]]
            分组结果字典

        NOTES:
        ------
        参考:https://docs.python.org/zh-cn/3/library/itertools.html#itertools.groupby
        """
        if val_func is None:

            def val_func(x):
                return x

        groups = collections.defaultdict(list)
        for val in it:
            groups[key_func(val)].append(val_func(val))
        return dict(groups)

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
    def is_string(cls, obj: T) -> bool:
        """
        检查对象是否是字符串

        Parameters
        ----------
        obj : T
            待检测对象


        Returns
        -------
        bool
            如果对象是字符串则返回 True, 否则返回 False
        """
        return isinstance(obj, str)

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
        判断给定的字符串是否为空, 字符串为空定义为: \n
        1. 字符串为None \n
        2. 空字符串: "" \n
        3. 空格、全角空格、制表符、换行符, 等不可见字符, \n

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

        for c in s:
            if c in (string.ascii_letters + string.digits + string.punctuation):
                return False

        return len(s.strip()) == 0

    @classmethod
    def is_not_blank(cls, s: str) -> bool:
        """
        判断给定的字符串是否不为空, 空字符串包括null、空字符串: ""、空格、全角空格、制表符、换行符, 等不可见字符, \\n

        Parameters
        ----------
        s : str
            待检测的字符串

        Returns
        -------
        bool
            如果字符串不为空返回True, 否则返回False
        """
        return not cls.is_blank(s)

    @classmethod
    def has_blank(cls, *args) -> bool:
        """
        判断多个字符串中是否有空白字符串

        Returns
        -------
        bool
            如果有空白字符串返回 True, 否则返回 False
        """
        return True if cls.is_empty(args) else any(cls.is_blank(arg) for arg in args)

    @classmethod
    def is_all_blank(cls, *args) -> bool:
        """
        判断给定的多个字符串是否全为空白字符串

        Returns
        -------
        bool
            如果所有字符串全为空则返回 True, 否则返回 False
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
    def ends_with_any(
        cls,
        s: str,
        *suffixes: str,
        case_insensitive: bool = False,
    ) -> bool:
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
    def is_surround(
        cls,
        s: str,
        prefix: str,
        suffix: str,
        case_insensitive: bool = True,
    ) -> bool:
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

        return cls.starts_with(s, prefix, case_insensitive=case_insensitive) and cls.ends_with(
            s, suffix, case_insensitive=case_insensitive
        )

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
    def is_alphabet(cls, uchar) -> bool:
        """
        判断一个 unicode 是否是英文字母

        Parameters
        ----------
        uchar : str
            待检测的unicode字符

        Returns
        -------
        bool
            如果是英文字母则返回True, 否则返回False
        """
        if not isinstance(uchar, str):
            raise TypeError(f"Expected a string, but found {type(uchar)}")
        if len(uchar) != 1:
            return False
        return ("\u0041" <= uchar <= "\u005a") or ("\u0061" <= uchar <= "\u007a")

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
    def contain_lowercase(cls, s: str) -> bool:
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
    def contain_uppercase(cls, s: str) -> bool:
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
    def none_to_default(
        cls,
        s: str,
        default_str: str,
    ) -> str:
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
        return default_str if cls.is_blank(s) else s

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
        return None if cls.is_blank(s) else s

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
    def b2q(cls, uchar: str) -> str:
        """
        半角转全角

        Parameters
        ----------
        uchar : str
            待转换的半角字符

        Returns
        -------
        str
            如果不是半角字符则返回原字符，否则返回对应的全角字符
        """
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7E:  # 不是半角字符就返回原来的字符
            return uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xFEE0
        return chr(inside_code)

    @classmethod
    def q2b(cls, uchar: str) -> str:
        """
        全角转半角

        Parameters
        ----------
        uchar : str
            待转换的全角字符

        Returns
        -------
        str
            如果不是全角字符则返回原字符，否则返回对应的半角字符
        """
        inside_code = ord(uchar)
        if inside_code == 0x3000:  # 全角空格直接转换
            inside_code = 0x0020
        else:
            inside_code -= 0xFEE0

        return uchar if inside_code < 0x0020 or inside_code > 0x7E else chr(inside_code)

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

        tokens: list[str] = [s.title() for s in input_string.split(separator)]

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
        将已有字符串填充为规定长度, 左侧填充字符 fill_char

        Parameters
        ----------
        s : str
            待填充的字符串
        fill_char : str
            填充的字符
        length : int
            填充后的长度

        Returns
        -------
        str
            如果·s·长度超过·length·则返回·s·本身, 否则返回填充后的字符串
        """
        return s.rjust(length, fill_char)

    @classmethod
    def fill_after(cls, s: str, fill_char: str, length: int) -> str:
        """
        将已有字符串填充为规定长度, 右侧填充字符 fill_char

        Parameters
        ----------
        s : str
            待填充的字符串
        fill_char : str
            填充的字符
        length : int
            填充后的长度

        Returns
        -------
        str
            如果·s·长度超过·length·则返回·s·本身, 否则返回填充后的字符串
        """
        return s.ljust(length, fill_char)

    @classmethod
    def sub_before(
        cls,
        s: str,
        separator: str,
        use_last_separator: bool = False,
    ) -> str:
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
    def get_center_msg(
        cls,
        s: str,
        fill_char: str,
        length: int,
    ) -> str:
        """
        获取打印信息, 信息左右两侧由指定字符填充, 信息居中

        *Example:*

        >>> StringUtil.get_center_msg("hello world", "=", 40) # ==== hello world ====
        >>> StringUtil.get_center_msg("hello world", "=", 1) # hello world

        Parameters
        ----------
        s : str
            待填充的字符串
        fill_char : str
            填充的字符
        length : int
            填充后的长度

        Returns
        -------
        str
            填充后的字符串
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

        s1_length = SequenceUtil.get_length(s1)
        s2_length = SequenceUtil.get_length(s2)
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
    def equals_any(
        cls,
        s: str,
        *args,
    ) -> bool:
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
        return any(cls.equals(s, arg, case_insensitive=False) for arg in args)

    @classmethod
    def equals_any_ignore_case(
        cls,
        s: str,
        *args,
    ) -> bool:
        """
        判断字符串 s 等于任何一个给定的字符串 args 中的字符串, 忽略大小写, 则返回 True, 否则返回 False.

        Parameters
        ----------
        s : str
            待检测字符串 s
        args : str
            待比较的字符串列表

        Returns
        -------
        bool
            如果字符串 s 等于任何一个给定的字符串 args 中的字符串, 则返回 True, 否则返回 False.
        """
        if cls.is_empty(args):
            return False
        return any(cls.equals(s, arg, case_insensitive=True) for arg in args)

    @classmethod
    def hide(
        cls,
        s: str,
        start: int,
        end: int,
        *,
        replace_char: str = "*",
    ) -> str:
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

        hide_part = cls.sub_sequence(s, start, end, include_last=False)
        return s[:start] + replace_char * len(hide_part) + s[end:]

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
    def reverse_fstring(
        cls,
        pattern: str,
        string: str,
    ) -> dict[str, str] | None:
        """
        反向解析字符串中的格式化字符串

        Parameters
        ----------
        pattern : str
            待解析的字符串模板
        string : str
            待解析的字符串

        Returns
        -------
        dict[str, str] | None
            解析结果字典, 如果解析失败则返回 None
        """
        pattern = cls._pattern_cache(pattern)
        return m.groupdict() if (m := pattern.fullmatch(string)) else None

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
        else:
            new = base
            while new in taken:
                new = transform(new)

        return new

    @classmethod
    def get_random_strs(
        cls,
        n: int,
        *,
        chars: str | None = None,
    ) -> str:
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
    def get_line_separator(cls, label: str = "") -> str:
        """
        获取行分隔符

        Parameters
        ----------
        label : str, optional
            标签, by default ""

        Returns
        -------
        str
            行分隔符
        """
        separator = "-" * 40
        result = f"\n\n{separator}{label}{separator}\n\n"
        return result

    @classmethod
    def get_size_string(cls, size: int) -> str:
        """
        获取文件大小字符串

        Parameters
        ----------
        size : int
            文件大小

        Returns
        -------
        str
            文件大小字符串
        """
        if size < 1 << 10:
            return "%d B" % size
        if size < 1 << 20:
            return "%d KB" % (size >> 10)
        if size < 1 << 30:
            return "%d MB" % (size >> 20)
        return "%d GB" % (size >> 30)

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
    def get_annotation_str(
        cls,
        s: str,
        *,
        annotation_syntax: str = "--",
    ) -> str:
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
        str_lst = list(SequenceUtil.get_chunks(rev_str, 3))
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
    def remove_suffixes(
        cls,
        s: str,
        *suffixes,
        **kwargs,
    ) -> str:
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
        case_insensitive = kwargs.get("case_insensitive", True) if kwargs else True
        for suffix in suffixes:
            s = cls.remove_suffix(s, suffix, case_insensitive=case_insensitive)

        return s

    @classmethod
    def remove_suffix(
        cls,
        s: str,
        suffix: str,
        *,
        case_insensitive: bool = True,
    ) -> str:
        """
        移除字符串中的指定后缀

        Parameters
        ----------
        s : str | None
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
        if case_insensitive:
            s = s.lower()
            suffix = suffix.lower()

        # NOTE 兼容3.9之前的版本，3.9之后可以直接调用str.removesuffix()方法
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
            return s.removesuffix(suffix)
        else:
            return s[: -len(suffix)] if cls.ends_with(s, suffix, case_insensitive=case_insensitive) else s

    @classmethod
    def remove_prefixes(
        cls,
        s: str,
        *prefixes,
        **kwargs,
    ) -> str:
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
        case_insensitive = kwargs.get("case_insensitive", True) if kwargs else True
        for prefix in prefixes:
            s = cls.remove_prefix(s, prefix, case_insensitive=case_insensitive)

        return s

    @classmethod
    def remove_prefix(
        cls,
        s: str,
        prefix: str,
        *,
        case_insensitive: bool = True,
    ) -> str:
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
        if case_insensitive:
            s = s.lower()
            prefix = prefix.lower()

        # NOTE 兼容3.9之前的版本，3.9之后可以直接调用str.removesuffix()方法
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
            return s.removeprefix(prefix)
        else:
            return s[len(prefix) :] if cls.starts_with(s, prefix, case_insensitive=case_insensitive) else s

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
    def remove_range(
        cls,
        s: str,
        start: int,
        end: int,
    ) -> str:
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

    @t.overload
    def only(cls, s: str, strategy: Strategy) -> str: ...

    @t.overload
    def only(cls, s: str, strategy: str) -> str: ...

    @classmethod
    def only(cls, s: str, strategy) -> str:
        if strategy is None:
            return s

        if isinstance(strategy, str):
            strategy = Strategy(strategy.upper())

        if strategy == Strategy.NUMERICS:
            return cls.only_numerics(s)
        elif strategy == Strategy.ALPHABETIC:
            return cls.only_alphabetic(s)
        elif strategy == Strategy.ALPHANUMERIC:
            return cls.only_alphanumeric(s)
        elif strategy == Strategy.UPPERCASE:
            return cls.only_uppercase(s)
        elif strategy == Strategy.LOWERCASE:
            return cls.only_lowercase(s)
        elif strategy == Strategy.PRINTABLE:
            return cls.only_printable(s)
        elif strategy == Strategy.ASCII:
            return cls.only_ascii(s)
        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

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

    @classmethod
    @functools.cache
    def _pattern_cache(cls, pattern: str) -> re.Pattern:
        pattern = re.sub(r"\{(?P<name>\w+)\}", r"(?P<\g<name>>.+)", pattern)
        return re.compile(pattern)

    @classmethod
    def _align_text(cls, text: str, width: int, padding: str = " ", align: str = "left") -> str:
        if align == "left":
            return text.rjust(width, padding)
        elif align == "right":
            return text.ljust(width, padding)
        else:
            return text.center(width, padding)


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
    def get_group_1(
        cls,
        pattern: re.Pattern,
        s: str,
    ) -> str | None:
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
    def get_group_2(
        cls,
        pattern: re.Pattern,
        s: str,
    ) -> str | None:
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
