#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   booleanutils.py
@Date       :   2024/11/13
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/11/13
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import itertools
import string
import typing as t

from pythontools.core.__typing import T


class BooleanUtil:
    TRUE_SET: frozenset[str] = frozenset([
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
    FALSE_SET: frozenset[str] = frozenset([
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
        return not cls.is_true(val)

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
        if cls._is_blank(expr):
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
        return cls.to_string(
            state,
            cls.DEFAULT_EN_TRUE_STR,
            cls.DEFAULT_EN_FALSE_STR,
        )

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

        if cls._is_blank(true_expr):
            true_expr = cls.DEFAULT_EN_TRUE_STR
        if cls._is_blank(false_expr):
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
        if cls._is_empty(values):
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
        if cls._is_empty(values):
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
        if cls._is_empty(values):
            raise ValueError("Empty sequence")
        result = cls._get_element(values, 0)
        for state in values[1:]:
            state = cls._get_bool_from_val(state)
            result = result ^ state
        return result

    @classmethod
    def _get_bool_from_val(cls, value: T) -> bool:
        if value is None:
            raise ValueError("None value is not a boolean value")
        if isinstance(value, bool):
            return value
        elif isinstance(value, int | float):
            return cls.number_to_boolean(value)
        elif isinstance(value, str):
            return cls.str_to_boolean(value)

        return bool(value)

    @classmethod
    def _is_empty(cls, seq: t.Sequence[T]) -> bool:
        return seq is None or len(seq) == 0

    @classmethod
    def _is_blank(cls, s: str) -> bool:
        if s is None:
            return True

        if not isinstance(s, str):
            raise TypeError(f"{s} is not a string")

        for c in s:
            if c in (string.ascii_letters + string.digits + string.punctuation):
                return False

        return not s.strip()

    @classmethod
    def _get_element(cls, it: t.Iterable[T], idx: int) -> T:
        if isinstance(it, t.Sequence):
            return it[idx] if idx < len(it) else None
        else:
            return next(itertools.islice(it, idx, None), None)
