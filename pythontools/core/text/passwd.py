#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   passwd.py
@Date       :   2024/08/09
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/09
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from ..constants.string_constant import PasswdStrength


class PasswdStrengthUtil:
    @classmethod
    def check(cls, passwd: str) -> int:
        # TODO 实现密码强度检测
        raise NotImplementedError()

    @classmethod
    def get_level(cls, strength: int) -> PasswdStrength:
        # TODO 根据密码强度返回等级
        raise NotImplementedError()
