#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   hashutils.py
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
import struct

from pythontools.core.constants.string_constant import CharsetUtil
from pythontools.core.errors import UnsupportedOperationError
from pythontools.core.utils.basic_utils import StringUtil
from pythontools.core.utils.encoding.hash.hash import Hash32, Hash64, Hash128


class MetroHash(Hash128, Hash64, Hash32):
    # TODO 实现该哈希类
    # 64位加盐
    k0_64 = 0xD6D018F5
    k1_64 = 0xA2AA033B
    k2_64 = 0x62992FC1
    k3_64 = 0x30BC5B29

    # 128位加盐
    k0_128 = 0xC83A91E1
    k1_128 = 0x8648DBDB
    k2_128 = 0x7BDEC03B
    k3_128 = 0x2F5870A5

    @classmethod
    def hash_32(cls, data: bytes | str) -> int:
        raise NotImplementedError

    @classmethod
    def hash_64(cls, data: bytes | str) -> int:
        if isinstance(data, str):
            data = StringUtil.to_bytes(data)
        return cls._hash_64(data)

    @classmethod
    def _hash_64(cls, data: bytes, seed: int = 1337) -> int:
        def rotate_right(value, shift):
            return ((value >> shift) | (value << (64 - shift))) & 0xFFFFFFFFFFFFFFFF

        def read_u64(data, offset):
            return struct.unpack_from("<Q", data, offset)[0]

        def read_u32(data, offset):
            return struct.unpack_from("<I", data, offset)[0]

        def read_u16(data, offset):
            return struct.unpack_from("<H", data, offset)[0]

        def read_u8(data, offset):
            return struct.unpack_from("<B", data, offset)[0]

        hash_val = (seed + cls.k2_64) * cls.k0_64
        v0 = hash_val

        if (bytes_length := StringUtil.get_length(data)) >= 32:
            while bytes_length >= 32:
                v0 += 1

        return hash_val

    @classmethod
    def hash_128(cls, data: bytes | str) -> int:
        raise NotImplementedError


class FnvHash(Hash64, Hash32, Hash128):
    """
    FNV Hash算法

    Attributes:
    ----------
        k32_prime: 32位FNV Hash算法的素数
        k64_prime: 64位FNV Hash算法的素数
        k128_prime: 128位FNV Hash算法的素数

    Methods:
    -------
        hash_32(data: bytes | str) -> int:
            计算32位FNV Hash值

        hash_64(data: bytes | str) -> int:
            计算64位FNV Hash值

        hash_128(data: bytes | str) -> int:
            计算128位FNV Hash值

    NOTES:
    ------
        FNV Hash算法是一种快速且高效的哈希算法, 它利用了哈希函数的自身特性来避免哈希冲突。
        1. FNV
        2. FNV-1
        3. FNV-1a
    FNV-1a 算法公式:
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │         hash = offset_basis                                                 │
    │         for each octet_of_data to be hashed                                 │
    │                 hash = hash xor octet_of_data                               │
    │                 hash = hash * FNV_prime                                     │
    │         return hash                                                         │
    └─────────────────────────────────────────────────────────────────────────────┘

    - offset_basis:初始的哈希值, 该值在最早的版本中是0, 为了增强哈希的可靠性, 后续修改为非0的值
    - FNV_prime: FNV用于散列的质数
    """

    k32_offset = 0x811C9DC5
    k64_offset = 0xCBF29CE484222000
    k128_offset = 0x6C62272E07BB00000000000000000000

    k32_prime = 0x1000193
    k64_prime = 0x100000001B3
    k128_prime = 0x10000000000000000000000

    def hash_128(self, data: bytes | str) -> int:
        """
        128 位哈希算法

        Parameters
        ----------
        data : bytes | str
            待哈希数据

        Returns
        -------
        int
            128 位哈希值
        """
        return self.__hash(data, FnvHash.k128_offset, FnvHash.k128_prime, 128)

    def hash_64(self, data: bytes | str) -> int:
        """
        64 位哈希算法

        Parameters
        ----------
        data : bytes | str
            待哈希数据

        Returns
        -------
        int
            64 位哈希值
        """
        return self.__hash(data, FnvHash.k64_offset, FnvHash.k64_prime, 64)

    def hash_32(self, data: bytes | str) -> int:
        """
        32 位哈希算法

        Parameters
        ----------
        data : bytes | str
            待哈希数据

        Returns
        -------
        int
            32 位哈希值
        """
        return self.__hash(data, FnvHash.k32_offset, FnvHash.k32_prime, 32)

    def hash(self, data: bytes | str) -> int:
        """
        哈希算法

        Parameters
        ----------
        data : bytes | str
            待哈希数据

        Returns
        -------
        int
            哈希值

        Raises
        ------
        UnsupportedOperationError
            调用该方法时抛出异常,请使用 hash_32, hash_64 或 hash_128 方法
        """
        raise UnsupportedOperationError("can not use hash method, please use hash_32, hash_64 or hash_128 method")

    def __hash(
        self,
        data: bytes | str,
        basic_offset: int,
        prime: int,
        bytes_length: int,
    ) -> int:
        if isinstance(data, bytes):
            data = data.decode(CharsetUtil.UTF_8)
        hash_value = basic_offset
        for char in data:
            hash_value ^= ord(char)
            if bytes_length == 32:
                hash_value = (hash_value << 5) ^ (hash_value >> 27) ^ prime
                hash_value &= 0xFFFFFFFF
            elif bytes_length == 64:
                hash_value = (hash_value << 7) ^ (hash_value >> 57) ^ prime
                hash_value &= 0xFFFFFFFFFFFFFFFF
            else:
                hash_value = (hash_value << 13) ^ (hash_value >> 116) ^ prime
                hash_value &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

        return hash_value
