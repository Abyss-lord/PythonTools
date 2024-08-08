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

from collections.abc import Mapping
from typing import Any

__all__ = ["ImmutableDict"]


def is_immutable(obj: Any, *args, **kwargs):
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
