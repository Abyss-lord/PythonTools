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

import itertools as it
import string
import typing
from collections.abc import Sequence, Set
from typing import Any

from ..constants.string_constant import CharPool
from ..decorator import UnCkeckFucntion
from .randomutils import RandomUtil


class CharsetUtil:
    ISO_8859_1: typing.Final[str] = "ISO-8859-1"
    UTF_8: typing.Final[str] = "UTF-8"
    GBK: typing.Final[str] = "GBK"


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
        return bool(val)

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
    def to_string(cls, value: bool, true_str: str, false_str: str, *, strict_mode: bool = False) -> str:
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
        StringUtil.EMPTY
        return bool(value)


class SequenceUtil:
    EMPTY: typing.Final[str] = CharPool.EMPTY
    SPACE: typing.Final[str] = CharPool.SPACE
    INDEX_NOT_FOUND: typing.Final[int] = -1

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
    def is_sub_equal(
        cls, main_seq: Sequence[Any], start_idx: int, sub_seq: Sequence[Any], sub_start_idx: int, split_length: int
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

        for i, j in zip(main_split_seq, sub_split_seq):
            if i != j:
                return False

        return True

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
        for i, v in enumerate(sequence):
            if v is None:
                return i
        return cls.INDEX_NOT_FOUND

    @classmethod
    def last_idx_of_none(cls, sequence: typing.Sequence[Any]) -> int:
        """
        返回序列中最后一个None元素的索引

        Parameters
        ----------
        sequence : typing.Sequence[Any]
            待检测序列

        Returns
        -------
        int
            最后一个None元素的索引位置
        """
        return cls.last_index_of(sequence, None)

    @classmethod
    def first_index_of(cls, sequence: typing.Sequence[Any], value: Any) -> int:
        """
        寻找序列中第一个指定元素的索引

        Parameters
        ----------
        sequence : typing.Sequence[Any]
            待检测序列
        value : Any
            待查找元素

        Returns
        -------
        int
            如果
        """
        if cls.is_empty(sequence):
            return cls.INDEX_NOT_FOUND

        idx = sequence.index(value)
        return cls.INDEX_NOT_FOUND if idx == -1 else idx

    @classmethod
    def last_index_of(cls, sequence: typing.Sequence[Any], value: Any) -> int:
        """
        寻找序列中最后一个指定元素的索引

        Parameters
        ----------
        sequence : typing.Sequence[Any]
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
        for i, item in enumerate(reversed(sequence)):
            if item == value:
                return length - i - 1
        return cls.INDEX_NOT_FOUND

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
    def new_list(cls, capacity: int, fill_val: Any = None) -> list[Any]:
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
    def set_or_append(cls, lst: typing.Sequence[Any], idx: int, value: Any) -> Sequence[Any]:
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
            res = [i for i in lst[:idx]]
            res += [value] + [i for i in lst[idx:]]

            return res
        else:
            return [i for i in lst] + [value]

    @classmethod
    def resize(cls, lst: typing.Sequence[Any], new_length: int, *, fill_val: Any = None) -> typing.Sequence[Any]:
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
    def get_first_n_item_from_iter(cls, iterable: typing.Iterable[Any], n: int) -> typing.Iterable[Any]:
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
    def is_all_element_equal(cls, iterable: typing.Iterable[Any]) -> bool:
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

    @classmethod
    def is_items_eauql(cls, seq: typing.Sequence[Any]) -> bool:
        """
        判断序列中y元素是否都相等

        Parameters
        ----------
        seq : typing.Sequence[Any]
            待检测序列

        Returns
        -------
        bool
            如果所有元素相等或者序列为空返回 True, 否则返回False
        """
        if cls.is_empty(seq):
            return True
        first_item = seq[0]
        return seq.count(first_item) == len(seq)

    @classmethod
    def rotate(cls, seq: typing.Sequence[Any], move_length: int) -> typing.Sequence[Any]:
        """
        将列表滚动移动 n 位

        Parameters
        ----------
        seq : typing.Sequence[Any]
            待滚动序列
        move_length : int
            滚动位数, 正数向后移动, 负数向前移动

        Returns
        -------
        typing.Sequence[Any]
            滚动后的新列表
        """
        if cls.is_empty(seq):
            return cls.EMPTY
        seq_length = len(seq)

        if abs(move_length) > seq_length:
            move_length %= seq_length

        res = []
        for i in seq[-move_length:]:
            res.append(i)
        for i in seq[:-move_length]:
            res.append(i)

        return res


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
        if s is None or len(s) == 0:
            return False
        for c in s:
            if not c.isspace():
                return False

        return True

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
        for c in s:
            if not (ord(c) < 32 or ord(c) == 127):
                return False
        return True

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
    def is_blank(cls, s: str | None, *, raise_type_exception: bool = False) -> bool:
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

        val = str(s) if not isinstance(s, str) else s
        for c in val:
            if c in (string.ascii_letters + string.digits + string.punctuation):
                return False

        return len(val.strip()) == 0

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

        if strict_mode:
            return s.startswith(prefix)

        s = s.strip()
        prefix = prefix.strip()

        if case_insensitive:
            return s.lower().startswith(prefix.lower())

        return s.startswith(prefix)

    @classmethod
    def is_starts_with_any(cls, s: str, *prefixes: str, case_insensitive: bool = False) -> bool:
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
        if cls.is_empty(prefixes) or cls.is_blank(s):
            return False
        for prefix in prefixes:
            if cls.is_startswith(s, prefix, case_insensitive=case_insensitive):
                return True

        return False

    @classmethod
    def is_endswith(
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
    def is_ends_with_any(cls, s: str, *suffixes: str, case_insensitive: bool = False) -> bool:
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
        for suffix in suffixes:
            if cls.is_endswith(s, suffix, case_insensitive=case_insensitive):
                return True

        return False

    @classmethod
    def has_number(cls, s: str) -> bool:
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
    def empty_to_none(cls, s: str) -> str | None:
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
    def to_bytes(cls, byte_or_str: bytes | str, encoding=CharsetUtil.UTF_8) -> bytes:
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
    def to_str(cls, byte_or_str: bytes | str, encoding=CharsetUtil.UTF_8) -> str:
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
    def as_set(cls, *args, froze: bool = False) -> Set[Any]:
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
        return set(args) if not froze else frozenset(args)

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
        if 1 <= number <= 20:
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
            separator_idx = s.index(separator) if not use_last_separator else s.rindex(separator)
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
            separator_idx = s.index(separator) if not use_last_separator else s.rindex(separator)
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
        s1 = s1.strip()
        s2 = s2.strip()

        if len(s1) != len(s2):
            return False

        if case_insensitive:
            return s1.lower() == s2.lower()
        return s1.strip() == s2.strip()

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
        for arg in args:
            if cls.equals(s, arg, case_insensitive=case_insensitive):
                return True

        return False

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
    def get_random_strs(cls, n: int, *, chars: str | None = None) -> str:
        """
        返回给定数量的随机字符串

        Parameters
        ----------
        n : int
            字符数量
        chars : typing.Optional[str], optional
            源字符串, 如果为None则使用默认的字符集, by default None

        Returns
        -------
        str
            随机字符串
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

    @classmethod
    def generate_box_string_from_dict(
        cls,
        data: typing.Mapping[str, Any],
        *,
        title: str = " RESULT ",
    ) -> str:
        """
        从字典数据生成箱体信息

        Parameters
        ----------
        data : typing.Mapping[str, Any]
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
                return " " + title + " "
            if not title.startswith(" "):
                return " " + title

            if not title.endswith(" "):
                return title + " "
            return title

        def get_max_length_from_dict(data: typing.Mapping[str, Any], level: int = 0) -> tuple[int, int]:
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
                    _append_content_line(k, v, level)

        def _append_content_line(key: str, value: str, level: int) -> None:
            prefix = "| "
            symbol = " : "
            sufix = " |"

            current_key_length = get_length_with_level(str(key), level)
            current_key_padding_length = max_key_length - current_key_length

            current_value_length = cls.get_width(str(value))
            current_value_padding_length = max_value_length - current_value_length

            level_padding = get_left_padding_str(level)

            key_padding = ""
            value_padding = ""

            if current_key_padding_length > 0:
                key_padding = " " * current_key_padding_length
            if current_value_padding_length > 0:
                value_padding = " " * current_value_padding_length

            content.append(f"{prefix}{level_padding}{key}{key_padding}{symbol}{value}{value_padding}{sufix}")

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
        for line in lines:
            if not line.startswith(annotation_syntax):
                line_lst.append(annotation_syntax + " " + line)
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
        if align not in ["left", "right", "center"]:
            raise ValueError(f"align must be 'left', 'right' or 'center', but got {align}")
        if align in ["left", "right"]:
            return cls._align_text(text, len(text) + 1, padding, align)
        else:
            return cls._align_text(text, len(text) + 2, padding, align)

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
        typing.List[str]
            分组后的字符串
        """
        if SequenceUtil.is_empty(s):
            return []
        return [s[i : i + n] for i in range(0, len(s), n)]

    @classmethod
    @UnCkeckFucntion()
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
        res_lst = []
        for i in str_lst[::-1]:
            res_lst.append(i[::-1])

        integer_str = ",".join(res_lst)
        decimal_str = "." + decimal_part if StringUtil.is_not_blank(decimal_part) else ""
        sign_str = "-" if negative_flg else ""

        return f"{sign_str}{integer_str}{decimal_str}"

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
        if cls.is_endswith(s, suffix, case_insensitive=case_insensitive):
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
        str_length = len(s)
        if str_length >= length:
            return s[:length]
        else:
            return s + cls.repeat_by_length(s, length - str_length)

    @classmethod
    @UnCkeckFucntion()
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
    @UnCkeckFucntion()
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
    @UnCkeckFucntion()
    def get_roman_range(cls, start: int, end: int, step: int = 1) -> typing.Generator[str, None, None]:
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
        typing.Generator[str, None, None]
            罗马数字字符串生成器

        Yields
        ------
        Iterator[typing.Generator[str, None, None]]
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
        if cls.is_endswith(s, suffix, case_insensitive=case_insensitive):
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
        if cls.is_startswith(s, prefix, case_insensitive=case_insensitive):
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

        if idx >= length or idx == length - 1:
            return s[:-1]

        return s[:idx] + s[idx + 1 :]

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

        if end >= cls.get_length(s):
            return s[:start]

        return s[:start] + s[end:]

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
        return dest[:start] + str(source) + dest[start + source_len :]

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
        if idx >= length:
            return s + sub_str

        return s[:idx] + sub_str + s[idx:]

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
            return cls.sub_lst(s, 0, length - cls.get_length(ellipsis)) + ellipsis  # type: ignore

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
        basic_str = cls.get_random_strs(k)
        return basic_str.capitalize()

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
    def _align_text(cls, text: str, width: int, padding: str = " ", align: str = "left") -> str:
        if align == "left":
            return text.rjust(width, padding)
        elif align == "right":
            return text.ljust(width, padding)
        else:
            return text.center(width, padding)
