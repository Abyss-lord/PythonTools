#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   phoneutils.py
@Date       :   2024/08/05
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/05
@Author     :   Plord117
@Desc       :   完成第一版
-------------------------------------------------
"""
# here put the import lib

from ..decorator import UnCheckFunction
from .basicutils import StringUtil

# 是否显示Warning信息
WARNING_ENABLED = True


class PhoneUtil:
    @classmethod
    def is_mobile(
        cls,
        phone: str,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断字符串是否是中国手机号

        Parameters
        ----------
        phone : str
            待检测字符串

        Returns
        -------
        bool
            是否为移动号码
        """
        return ReUtil.is_match(
            PatternPool.MOBILE,
            phone,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_mobile_hk(
        cls,
        phone: str,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断是否是香港移动号码

        Parameters
        ----------
        phone : str
            待检测字符串

        Returns
        -------
        bool
            是否是香港移动号码
        """
        return ReUtil.is_match(
            PatternPool.MOBILE_HK,
            phone,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_mobile_tw(cls, phone: str, raise_exception: bool = False) -> bool:
        """
        判断是否是台湾移动号码

        Parameters
        ----------
        phone : str
            待检测字符串

        Returns
        -------
        bool
            是否是台湾移动号码
        """
        return ReUtil.is_match(
            PatternPool.MOBILE_TW,
            phone,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_mobile_mo(
        cls,
        phone: str,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断是否是澳门移动号码

        Parameters
        ----------
        phone : str
            待检测字符串

        Returns
        -------
        bool
            是否是澳门移动号码
        """
        return ReUtil.is_match(
            PatternPool.MOBILE_MO,
            phone,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_tel(
        cls,
        tel: str,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断是否是电话号码

        Parameters
        ----------
        tel : str
            待检测字符串

        Returns
        -------
        bool
            是否是电话号码
        """
        return ReUtil.is_match(
            PatternPool.TEL,
            tel,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_tel_400800(
        cls,
        tel: str,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断是否是座机号码（中国大陆）

        Parameters
        ----------
        tel : str
            待检测字符串

        Returns
        -------
        bool
            是否为座机号码（中国大陆）
        """
        return ReUtil.is_match(
            PatternPool.TEL_400_800,
            tel,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        """
        判断是否是有效的手机号码

        Parameters
        ----------
        phone : str
            待检测字符串

        Returns
        -------
        bool
            是否是有效的手机号码
        """
        return cls.is_mobile_hk(phone) or cls.is_mobile_tw(phone) or cls.is_mobile_mo(phone) or cls.is_mobile(phone)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def hide_before(cls, phone: str) -> str:
        """
        隐藏手机号前7位 替换字符为 "*" 栗子

        Parameters
        ----------
        phone : str
            待隐藏手机号

        Returns
        -------
        str
            隐藏完毕的手机号
        """
        return StringUtil.hide(phone, 0, 7)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def hide_between(cls, phone: str) -> str:
        """
        隐藏手机号中间4位 替换字符为"*" 栗子

        Parameters
        ----------
        phone : str
            待隐藏手机号

        Returns
        -------
        str
            隐藏完毕的手机号
        """
        return StringUtil.hide(phone, 3, 7)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def hide_after(cls, phone: str) -> str:
        """
        隐藏手机号最后4位 替换字符为"*" 栗子

        Parameters
        ----------
        phone : str
            待隐藏手机号

        Returns
        -------
        str
            隐藏完毕的手机号
        """
        return StringUtil.hide(phone, 7, 11)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def get_phone_before(cls, phone: str) -> str:
        """
        获取手机号前3位

        Parameters
        ----------
        phone : str
            待获取手机号

        Returns
        -------
        str
            前3位手机号
        """
        return StringUtil.sub_sequence(phone, 0, 3)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def get_phone_between(cls, phone: str) -> str:
        """
        获取手机号中间4位

        Parameters
        ----------
        phone : str
            待获取手机号

        Returns
        -------
        str
            手机号中间4位
        """
        return StringUtil.sub_sequence(phone, 3, 7)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def get_phone_after(cls, phone: str) -> str:
        """
        获取手机号后4位

        Parameters
        ----------
        phone : str
            待获取手机号

        Returns
        -------
        str
            手机号后4位
        """
        return StringUtil.sub_sequence(phone, 7, 11)
