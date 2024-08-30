#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   hash.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from abc import ABC, abstractmethod


class Hash(ABC):
    @abstractmethod
    def hash(self, data: bytes | str) -> int: ...


class Hash128(Hash):
    def hash(self, data: bytes | str) -> int:
        return self.hash_128(data)

    @abstractmethod
    def hash_128(self, data: bytes | str) -> int: ...


class Hash64(Hash):
    def hash(self, data: bytes | str) -> int:
        return self.hash_64(data)

    @abstractmethod
    def hash_64(self, data: bytes | str) -> int: ...


class Hash32(Hash):
    def hash(self, data: bytes | str) -> int:
        return self.hash_32(data)

    @abstractmethod
    def hash_32(self, data: bytes | str) -> int: ...
