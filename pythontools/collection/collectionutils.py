#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   collectionutil.py
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

# here put the import libraries
import itertools as it
import typing
from collections import abc
from collections.abc import Generator, Iterable, Sequence
from typing import Any


class CollectionUtil:
    @classmethod
    def nested_dict_iter(cls, nested_dict: typing.Mapping[Any, Any]) -> typing.Generator[Any, Any, Any]:
        """
        返回嵌套字典最深层及的键值对

        Examples
        --------
        >>> d = {'a':{'a':{'y':2}},'b':{'c':{'a':5}},'x':{'a':6}}
        ... list(nested_dict_iter(d)) # [('y', 2), ('a', 5), ('a', 6)]

        Parameters
        ----------
        nested_dict : typing.Mapping[Any, Any]
            嵌套字典

        Returns
        -------
        typing.Generator[Any, Any, Any]
            键值对生成器

        Yields
        ------
        Iterator[typing.Generator[Any, Any, Any]]
            键值对生成器, 返回键值对

        """
        for key, value in nested_dict.items():
            if isinstance(value, abc.Mapping):
                yield from cls.nested_dict_iter(value)
            else:
                yield key, value

    @classmethod
    def get_powerset(cls, iterable: typing.Iterable) -> typing.Generator[it.chain, Any, Any]:
        """
        返回iterable的幂集

        Examples
        --------
        >>> list(CollectionUtil.get_powerset([1,2,3])) # [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

        Parameters
        ----------
        iterable : typing.Iterable
            可迭代对象

        Returns
        -------
        typing.Generator[it.chain, Any, Any]
            幂集生成器

        Yields
        ------
        Iterator[typing.Generator[it.chain, Any, Any]]
            幂集生成器, 返回幂集
        """
        s = list(iterable)
        yield it.chain.from_iterable(it.combinations(s, r) for r in range(len(s) + 1))

    @classmethod
    def flatten(cls, seq: Iterable[Any]) -> Generator[Any, Any, None]:
        """
        展平嵌套序列

        Examples
        --------
        >>> list(CollectionUtil.flatten([1, [2, 3], [4, [5, 6]]])) # [1, 2, 3, 4, 5, 6]

        Parameters
        ----------
        seq : Iterable[Any]
            待展平序列

        Yields
        ------
        Generator[Any, Any, None]
            展平序列生成器, 返回展平序列
        """
        for ele in seq:
            if hasattr(ele, "__iter__") and isinstance(ele, Sequence):
                yield from cls.flatten(ele)
            else:
                yield ele

    @classmethod
    def merge_dicts(cls, *dicts: typing.Mapping[Any, Any]) -> dict[Any, Any]:
        """
        合并多个字典

        Returns
        -------
        dict[Any, Any]
            字典序列

        Raises
        ------
        TypeError
            如果参数不是字典类型
        """
        base_dict: dict[Any, Any] = {}
        for i, dict_element in enumerate(dicts):
            if not isinstance(dict_element, dict):
                raise TypeError(f"Argument {i} is not a dictionary")
            base_dict = cls.merge_two_dict(base_dict, dict_element)
        return base_dict

    @classmethod
    def merge_two_dict(cls, d1: typing.Mapping[Any, Any], d2: typing.Mapping[Any, Any]) -> dict[Any, Any]:
        """
        合并两个字典

        Examples
        --------
        >>> d1 = {'a':1, 'b':2} # {'a':1, 'b':2}
        >>> d2 = {'b':3, 'c':4} # {'b':3, 'c':4}
        >>> CollectionUtil.merge_two_dict(d1, d2) # {'a':1, 'b':3, 'c':4}

        Parameters
        ----------
        d1 : typing.Mapping[Any, Any]
            字典1
        d2 : typing.Mapping[Any, Any]
            字典2

        Returns
        -------
        dict[Any, Any]
            合并后的字典
        """
        return {**d1, **d2}
