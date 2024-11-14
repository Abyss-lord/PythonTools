#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   basicvalidator.py
@Date       :   2024/07/24
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/24
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import typing
import unicodedata

from ..constants.pattern_pool import PatternPool
from ..utils.basic_utils import ReUtil


class BasicValidator:
    FLOAT_CALCULATE_THRESHOLD = 1e-7

    @classmethod
    def is_number(cls, value: typing.Any) -> bool:
        """
        验证给定值是否是数字

        Parameters
        ----------
        value : typing.Any
            待检测值

        Returns
        -------
        bool
            是否是数字

        Notes
        -------
        1. 整数、浮点数、复数均视为数字
        2. 字符串数字格式为：整数、浮点数、科学计数法，中文数字格式为：整数、浮点数
        3. 依赖于`is_integer_num`方法和`is_float_num`方法进行判断
        """
        return cls.is_integer_num(value) or cls.is_float_num(value)

    @classmethod
    def is_integer_num(cls, value: typing.Any) -> bool:
        """
        验证给定值是否是整数

        Parameters
        ----------
        value : typing.Any
            待检测值

        Returns
        -------
        bool
            是否为整数
        """
        if isinstance(value, int | float | complex):
            return True
        elif isinstance(value, str):
            if ReUtil.is_match(PatternPool.INTEGER, value):
                return True
            else:
                return cls.is_chinese_integer_num(value)
        else:
            return False

    @classmethod
    def is_float_num(cls, value: typing.Any) -> bool:
        """
        验证给定值是否是浮点数

        Parameters
        ----------
        value : typing.Any
            待检测值

        Returns
        -------
        bool
            是否是浮点数
        """
        if isinstance(value, int | float | complex):
            return True
        elif isinstance(value, str):
            if ReUtil.is_match(PatternPool.FLOAT_NUM, value):
                return True
            else:
                return cls.is_chinese_float_num(value)
        else:
            return False

    @classmethod
    def is_chinese_num(cls, value: str) -> bool:
        """
        验证是否是中文形式的数字

        Parameters
        ----------
        value : str
            待检测值

        Returns
        -------
        bool
            是否是中文形式的数字
        """
        # PERF 优化，不要使用try-except做逻辑判断
        try:
            unicodedata.numeric(value)
            return True
        except (TypeError, ValueError):
            return False
        else:
            return False

    @classmethod
    def is_chinese_integer_num(cls, value: str) -> bool:
        """
        验证是否是中文形式的整数

        Parameters
        ----------
        value : str
            待检测值

        Returns
        -------
        bool
            是否是中文形式的整数
        """
        if not cls.is_chinese_num(value):
            return False
        float_format_val = unicodedata.numeric(value)
        return cls.is_two_num_equal(float_format_val, int(float_format_val))

    @classmethod
    def is_chinese_float_num(cls, value: str) -> bool:
        """
        验证是否是中文形式的浮点数

        Parameters
        ----------
        value : str
            待检测值

        Returns
        -------
        bool
            是否是中文形式的浮点数
        """
        return not cls.is_chinese_integer_num(value)

    @classmethod
    def is_two_num_equal(cls, num1: int | float, num2: int | float) -> bool:
        """
        判断两个数字是否相等, 允许误差范围为1e-7

        Parameters
        ----------
        num1 : Union[int, float]
            数字1
        num2 : Union[int, float]
            数字2

        Returns
        -------
        bool
            是否相等
        """
        return abs(num1 - num2) < cls.FLOAT_CALCULATE_THRESHOLD

    @classmethod
    def equals(cls, val1: typing.Any, val2: typing.Any) -> bool:
        """
        判断两个对象是否相等

        Examples
        --------
        >>> BasicValidator.equals(1, 1)
        True
        >>> BasicValidator.equals(1, 2)
        False
        >>> BasicValidator.equals("1", 1)
        False

        Parameters
        ----------
        val1 : typing.Any
            待判定对象1
        val2 : typing.Any
            待判定对象2

        Returns
        -------
        bool
            是否相等
        """
        # 如果是同一个地址则直接返回True
        if val1 is val2:
            return True
        return False if val1.__class__ != val2.__class__ else val1 == val2

    @classmethod
    def is_between(
        cls,
        val: int | float,
        min_val: int | float,
        max_val: int | float,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断数值是否在给定范围内

        Examples
        --------
        >>> BasicValidator.is_between(1, 0, 2)
        True
        >>> BasicValidator.is_between(2, 0, 1)
        False
        >>> BasicValidator.is_between(1, 0, 2)
        True
        >>> BasicValidator.is_between(1, 1, 2)
        True
        >>> BasicValidator.is_between(2, 1, 2)
        True

        Parameters
        ----------
        val : Union[int, float]
            待检测数值
        min_val : Union[int, float]
            范围下限
        max_val : Union[int, float]
            范围上限
        raise_exception : bool, optional
            不在范围内是否引发异常, by default False

        Returns
        -------
        bool
            是否在范围内

        Raises
        ------
        ValueError
            1. 如果不在范围内且raise_exception=True, 引发该异常
            2. 如果 min_val 大于 max_val, 引发该异常
        """
        if min_val > max_val:
            raise ValueError(f"min_val:{min_val} > max_val:{max_val}")
        res = min_val <= val <= max_val
        if not res and raise_exception:
            raise ValueError(f"{val} is not between {min_val} and {max_val}")
        return res
