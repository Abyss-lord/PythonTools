#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   stringvalidator.py
@Date       :   2024/07/26
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/26
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import json

from ..basicutils import StringUtil
from ..pattern_pool import PatternPool
from ..reutils import ReUtil


class StringValidator:
    @classmethod
    def is_json(cls, s: str) -> bool:
        """
        判断字符串是否是json字符串

        Example:
        ----------
        >>> Validator.is_json('{"name": "John", "age": 30, "city": "New York"}') # returns True
        >>> Validator.is_json('{"name": "John", "age": 30, "city": "New York"') # returns False
        >>> Validator.is_json('{"name": "John", "age": 30, "city": "New York"} ') # returns False

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            如果是json字符串, 则返回True, 否则返回False
        """
        if StringUtil.is_blank(s):
            return False

        if PatternPool.JSON_WRAPPER_PATTERN.match(s) is None:
            return False

        # PERF 不应该用try-except作为分支逻辑
        try:
            return isinstance(json.loads(s), (dict, list))
        except (TypeError, ValueError, OverflowError):
            pass

        return False

    @classmethod
    def is_general_string(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        匹配字符串是否只由数字、字母、下划线组成

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            是否匹配

        Raises
        ------
        ValidationError
            如果raise_exception为True, 且不匹配时, 抛出ValidationError异常
        """
        return ReUtil.is_match(
            PatternPool.GENERAL_STRING_PATTERN, s, raise_exception=raise_exception
        )

    @classmethod
    def is_general_string_with_length(
        cls, s: str, min_length: int, max_length: int, *, raise_exception: bool = False
    ) -> bool:
        """
        验证是否为给定长度范围的英文字母 、数字和下划线

        Parameters
        ----------
        s : str
            待检测字符串
        min_length : int
            最小长度, 小于0则自动识别为0
        max_length : int
            最大长度, 小于0则自动识别为无限长度
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否匹配
        """
        if min_length < 0:
            min_length = 0

        reg = "^\\w{" + str(min_length) + "," + str(max_length) + "}$"
        if max_length <= 0:
            reg = "^\\w{" + str(min_length) + ",}$"

        return ReUtil.is_match_reg(s, reg, raise_exception=raise_exception)

    @classmethod
    def is_money(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.MONEY, s, raise_exception=raise_exception)

    @classmethod
    def is_zip_code(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.ZIP_CODE, s, raise_exception=raise_exception)

    @classmethod
    def is_mobile(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.MOBILE, s, raise_exception=raise_exception)

    @classmethod
    def is_ipv4(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.IPV4, s, raise_exception=raise_exception)

    @classmethod
    def is_ipv6(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.IPV6, s, raise_exception=raise_exception)

    @classmethod
    def is_mac_address(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(
            PatternPool.MAC_ADDRESS, s, raise_exception=raise_exception
        )

    @classmethod
    def is_chinese_vehicle_number(
        cls, s: str, *, raise_exception: bool = False
    ) -> bool:
        return ReUtil.is_match(
            PatternPool.CHINESE_VEHICLE_NUMBER, s, raise_exception=raise_exception
        )

    @classmethod
    def is_chinese(cls, s: str, *, raise_exception: bool = False) -> bool:
        return ReUtil.is_match(PatternPool.CHINESES, s, raise_exception=raise_exception)

    @classmethod
    def has_chinese(cls, s: str, *, raise_exception: bool = False) -> bool:
        pass

    @classmethod
    def is_general_with_chinese(cls, s: str, *, raise_exception: bool = False) -> bool:
        pass

    @classmethod
    def is_hex(cls, s: str, *, raise_exception: bool = False) -> bool:
        pass

    @classmethod
    def is_credit_code(cls, s: str, *, raise_exception: bool = False) -> bool:
        pass

    @classmethod
    def is_car_vin(cls, s: str, *, raise_exception: bool = False) -> bool:
        pass

    @classmethod
    def is_chinese_driving_licence(
        cls, s: str, *, raise_exception: bool = False
    ) -> bool:
        pass
