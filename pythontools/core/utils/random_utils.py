#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   randomutils.py
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
import random
import typing as t

from pythontools.core.__typing import T


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
