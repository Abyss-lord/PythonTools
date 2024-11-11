#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   structures.py
@Date       :   2024/08/05
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/05
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import typing as t
from collections.abc import Mapping, Set

__all__ = ["ImmutableDict"]
K = t.TypeVar("K")
V = t.TypeVar("V")


def is_immutable(obj: t.Any, *args, **kwargs):
    raise TypeError(f"This {type(obj).__name__} is immutable")


class ImmutableDict(Mapping):
    def __init__(self, *args) -> None:
        self._data = dict(*args)

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def __getitem__(self, key):
        return self._data[key]

    __setattr__ = is_immutable
    __delattr__ = is_immutable
    __setitem__ = is_immutable
    __delitem__ = is_immutable
    clear = is_immutable
    update = is_immutable
    pop = is_immutable

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def get(self, key, default=None) -> Any | None:
        return self._data.get(key, default)


class ImmutableList(list):
    def __init__(self, *args) -> None:
        super().__init__(args)

    __setitem__ = is_immutable
    __delitem__ = is_immutable
    append = is_immutable
    extend = is_immutable
    insert = is_immutable
    pop = is_immutable
    remove = is_immutable
    clear = is_immutable
    reverse = is_immutable


class CaseInsensitiveDict(dict):
    def __init__(self, default=None, *args, **kw):
        self._o = {}

        if default is None:
            default = dict(kw)
        for i in default:
            self[i] = default[i]

        super().__init__()

    def items(self):
        return [(self._o[k], self[k]) for k in self]

    def __setitem__(self, k, v):
        try:
            nk = k.lower()
        except Exception:
            nk = k

        self._o[nk] = k
        super().__setitem__(nk, v)

    def __getitem__(self, k):
        try:
            nk = k.lower()
        except Exception:
            nk = k

        return super().__getitem__(nk)


class SingleValuedMapping(t.Mapping[K, V]):
    """
    Mapping where all keys return the same value.

    This rigamarole is meant to avoid copying keys, which was originally intended
    as an optimization while qualifying columns for tables with lots of columns.
    """

    def __init__(self, keys: t.Collection[K], value: V):
        self._keys = keys if isinstance(keys, Set) else set(keys)
        self._value = value

    def __getitem__(self, key: K) -> V:
        if key in self._keys:
            return self._value
        raise KeyError(key)

    def __len__(self) -> int:
        return len(self._keys)

    def __iter__(self) -> t.Iterator[K]:
        return iter(self._keys)
