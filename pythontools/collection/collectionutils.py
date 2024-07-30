#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
from typing import Any, Dict, List, Set, Tuple


class CollectionUtil:
    @classmethod
    def nested_dict_iter(
        cls, nested_dict: typing.Mapping[Any, Any]
    ) -> typing.Generator[Any, Any, Any]:
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
    def get_powerset(
        cls, iterable: typing.Iterable
    ) -> typing.Generator[it.chain, Any, Any]:
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
