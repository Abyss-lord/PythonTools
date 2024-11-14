# Copyright 2024 The pythontools Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

import gc
import os
import platform
import sys
import typing as t
import warnings

from .basic_utils import StringUtil


class EnvUtil:
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
        return StringUtil.starts_with(platform_info, "macos", case_insensitive=True)

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
        return StringUtil.starts_with(platform_info, "linux", case_insensitive=True)

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
        return StringUtil.starts_with(platform_info, "windows", case_insensitive=True)

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
        return sys.version_info < (3, 0)

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

        return (3, 0) <= sys.version_info <= (4, 0)

    @classmethod
    def is_notebook(cls) -> bool:
        """
        判断是否是 Notebook 环境

        Returns
        -------
        bool
            是否是 Notebook 环境
        """
        if IPython := sys.modules.get("IPython"):  # pylint: disable=invalid-name
            ipython = IPython.get_ipython()
            if ipython and "IPKernelApp" in ipython.config:
                return True
        return False

    @classmethod
    def get_system_property(
        cls,
        name: str,
        default_value: str = "",
        *,
        quiet: bool = False,
    ) -> t.Any:
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

        return dict(res)

    @classmethod
    def python_gc(cls) -> None:
        """Call python's garbage collector."""
        # gc_collect isn't perfectly synchronous, because it may
        # break reference cycles that then take time to fully
        # finalize. Call it thrice and hope for the best.
        for _ in range(3):
            gc.collect()
