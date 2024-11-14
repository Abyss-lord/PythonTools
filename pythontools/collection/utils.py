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
import typing as t
from collections import abc
from collections.abc import Collection, Generator, Iterable

Unpack = t.Any
_KeyT = t.TypeVar("_KeyT")
_ValuesT = t.Any


class CollectionUtil:
    @classmethod
    def nested_dict_iter(cls, nested_dict: t.Mapping[t.Any, t.Any]) -> t.Generator[t.Any, t.Any, t.Any]:
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
    def get_powerset(cls, iterable: t.Iterable) -> t.Generator[it.chain, t.Any, t.Any]:
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
    def flatten(cls, seq: Iterable[t.Any]) -> Generator[t.Any, t.Any, None]:
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
            if hasattr(ele, "__iter__") and isinstance(ele, str | bytes):
                yield from cls.flatten(ele)
            else:
                yield ele

    @classmethod
    def merge_dicts(cls, *dicts: t.Mapping[t.Any, t.Any]) -> dict[t.Any, t.Any]:
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
        base_dict: dict[t.Any, t.Any] = {}
        for i, dict_element in enumerate(dicts):
            if not isinstance(dict_element, dict):
                raise TypeError(f"Argument {i} is not a dictionary")
            base_dict = cls.merge_two_dict(base_dict, dict_element)
        return base_dict

    @classmethod
    def merge_two_dict(cls, d1: t.Mapping[t.Any, t.Any], d2: t.Mapping[t.Any, t.Any]) -> dict[t.Any, t.Any]:
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

    @t.overload
    def ensure_collection(value: t.Collection[t.Any]) -> t.Collection[t.Any]: ...

    @t.overload
    def ensure_collection(value: t.Any) -> t.Collection[t.Any]: ...

    @t.overload
    def ensure_collection(value: None) -> t.Collection[t.Any]: ...

    @classmethod
    def ensure_collection(cls, value) -> t.Collection[t.Any]:
        """
        确保值是一个集合，否则强制转换或封装为一个集合。

        Parameters
        ----------
        value : None | t.Any | t.Collection[t.Any]
            待转换的值

        Returns
        -------
        t.Collection[t.Any]
            转换后的集合
        """
        if value is None:
            return []
        return value if isinstance(value, Collection) and not isinstance(value, str | bytes) else [value]

    @t.overload
    def ensure_list(value: t.Collection[t.Any]) -> list[t.Any]: ...

    @t.overload
    def ensure_list(value: t.Any) -> list[t.Any]: ...

    @t.overload
    def ensure_list(value: None) -> list[t.Any]: ...

    @classmethod
    def ensure_list(cls, value) -> list[t.Any]:
        """
        确保值是一个列表，否则强制转换或封装为一个列表。

        Parameters
        ----------
        value : None | t.Any | t.Collection[t.Any]
            待转换的值

        Returns
        -------
        list[t.Any]
            转换后的列表
        """
        if value is None:
            return []

        return value if isinstance(value, list | tuple) else [value]

    @classmethod
    def dict_depth(cls, d: dict) -> int:
        """
        返回字典的深度

        Parameters
        ----------
        d : dict
            待计算的字典

        Returns
        -------
        int
            字典的深度
        """
        try:
            return 1 + cls.dict_depth(next(iter(d.values())))
        except AttributeError:
            return 0
        except StopIteration:
            return 1

    @classmethod
    def zip_dict(cls, *dicts: dict[_KeyT, _ValuesT]) -> t.Generator[tuple[_KeyT, tuple[_ValuesT]], None, None]:
        all_keys = set(it.chain(*dicts))
        d0 = dicts[0]
        if len(all_keys) != len(d0):
            raise KeyError(f"Missing keys: {all_keys ^ set(d0)}")

        for key in d0:
            yield key, tuple(d[key] for d in dicts)
