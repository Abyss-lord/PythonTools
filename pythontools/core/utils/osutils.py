#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   osutils.py
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
# here put the import lib

import os
import platform
import sys
import typing
import warnings

from .basicutils import StringUtil


class SysUtil:
    @classmethod
    def get_platform_info(cls) -> str:
        """
        获取平台信息

        Returns
        -------
        str
            平台信息字符串
        """
        return platform.platform()

    @classmethod
    def is_mac_platform(cls) -> bool:
        """
        判断是否是 Mac 平台

        Returns
        -------
        bool
            是否是 Mac 平台
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "macos", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_linux_platform(cls) -> bool:
        """
        判断是否是linux 平台

        Returns
        -------
        bool
            是否是linux平台

        Notes
        -----
        1. 依赖 platform 库
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "linux", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_windows_platform(cls) -> bool:
        """
        判断平台是否是windows

        Returns
        -------
        bool
            是否是windows

        Notes
        -----
        1. 依赖 platform 库
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "windows", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_py2(cls) -> bool:
        """
        判断是否是 Python2

        Examples
        --------
        >>> SysUtil.is_py2()
        False

        Returns
        -------
        bool
            是否Python2

        Raises
        ------
        ValueError
            如果不是Python2也不是Python3, 则抛出ValueError
        """
        if sys.version_info >= (3, 0):  # noqa: UP036
            return False
        if sys.version_info < (3, 0):  # noqa: UP036
            return True
        raise ValueError("cannot determine if it's python2")

    @classmethod
    def is_py3(cls) -> bool:
        """
        判断是否是 Python3

        Examples
        --------
        >>> SysUtil.is_py3()
        True

        Returns
        -------
        bool
            是否Python3
        """

        if (3, 0) <= sys.version_info <= (4, 0):
            return True
        else:
            return False

    @classmethod
    def get_system_property(cls, name: str, default_value: str = "", *, quiet: bool = False) -> typing.Any:
        """
        获取指定名称的系统变量

        Parameters
        ----------
        name : str
            指定的变量名称
        default_value : str, optional
            默认值, by default ""
        quiet : bool, optional
            是否关闭警告信息, by default False

        Returns
        -------
        typing.Any
            指定的系统变量值
        """
        try:
            res = os.getenv(name)
        except Exception as e:
            if not quiet:
                warnings.warn(f"get system property {name} error: {e}, will return default value, {default_value}")
        else:
            return res if res is not None else default_value

    @classmethod
    def get_system_properties(cls, quiet: bool = False) -> dict[str, str]:
        """
        获取所有的系统变量

        Parameters
        ----------
        quiet : bool, optional
            是否关闭警告信息, by default False

        Returns
        -------
        typing.Dict[str, str]
            所有的系统变量
        """
        try:
            res = os.environ
        except Exception as e:
            if not quiet:
                warnings.warn(f"get system properties error: {e}")

        environ_dict = {k: v for k, v in res.items()}
        return environ_dict
