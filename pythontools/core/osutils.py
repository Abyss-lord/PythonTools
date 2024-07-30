#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
import time
import typing
import warnings
from operator import eq

from .basicutils import StringUtil


class OsUtil(object):
    @classmethod
    def is_exist(cls, p: str, *, raise_exception: bool = False) -> bool:
        """
        检查路径是否存在

        Parameters
        ----------
        p : str
            待检测路径
        raise_exception : bool, optional
            不存在是否引发异常, by default False

        Returns
        -------
        bool
            如果路径存在返回True, 如果raise_exception=False, 则返回False, 否则引发异常

        Raises
        ------
        FileNotFoundError
            如果路径不存在且raise_exception=True, 则引发FileNotFoundError异常
        """
        # 检查路径是否存在
        if StringUtil.is_blank(p):
            return False
        if os.path.exists(p):
            return True

        # 如果路径不存在且需要抛出异常，则抛出FileNotFoundError
        if raise_exception:
            raise FileNotFoundError(p)

        return False

    @classmethod
    def is_dir(cls, p: str, *, raise_exception: bool = False) -> bool:
        """
        判断路径是否是文件夹
        :param p: 文件夹路径
        :param raise_exception: 如果文件夹不存在是否引发异常, 默认不引发异常
        :return: 如果路径存在且是文件夹返回True, 如果指定raise_exception, 不存在则引发FileNotFoundError异常, 否则返回False
        """
        if StringUtil.is_blank(p):
            return False
        if os.path.isdir(p):
            return True
        if raise_exception:
            raise ValueError(f"'{p}' is not a directory or does not exist")

        return False

    # @Param p: 文件路径
    # @Param raise_exception: 如果文件不存在是否引发异常, 默认不引发异常
    @classmethod
    def is_file(cls, p: str, *, raise_exception: bool = False) -> bool:
        """
        判断路径是否是文件
        :param p: 文件路径
        :param raise_exception: 如果文件不存在是否引发异常, 默认不引发异常
        :return: 文件存在返回 True, 如果 raise_exception=False 返回False, 否则引发异常
        """
        if StringUtil.is_blank(p):
            return False
        if os.path.isfile(p):
            return True
        if raise_exception:
            raise ValueError(f"File {p} does not exist or is not a file")

        return False

    @classmethod
    def is_root_path(cls, p: str) -> bool:
        """
        判断路径是否是根路径
        :param p: 待检测路径
        :return: 是否是根路径
        """
        if StringUtil.is_blank(p):
            return False

        return os.path.ismount(p)

    @classmethod
    def is_hidden_dir(cls, base_name: str) -> bool:
        """
        判断一个名称是否是具有隐藏属性
        :param base_name: 待检测名称
        :return: 是否具有隐藏属性
        """
        if StringUtil.is_blank(base_name):
            return False

        base_name = base_name.strip()
        if base_name.startswith(".") or base_name.startswith("__"):
            return True

        return False

    @classmethod
    def is_contain_hidden_dir(cls, p: str) -> bool:
        """
        检测路径是否含有隐藏文件夹
        :param p: 待检测路径
        :return: 如果含有隐藏文件夹返回 True, 否则返回False
        """
        while not cls.is_root_path(p) and not StringUtil.is_blank(p):
            basename = cls.get_basename_from_path(p)
            if cls.is_hidden_dir(basename):
                return True
            p, _ = os.path.split(p)

        return False

    @classmethod
    def get_file_create_time(
        cls,
        p: str,
        time_format: str = "%Y-%m-%d %H:%M:%S",
        *,
        check_exist: bool = False,
    ) -> str:
        """
        以字符串形式返回文件创建时间
        :param p: 文件路径
        :param time_format: 时间格式
        :param check_exist: 是否检查存在
        :return: 如果存在则返回创建时间
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)
        t = os.path.getctime(p)
        format_time = time.strftime(time_format, time.localtime(t))
        return format_time

    @classmethod
    def list_dirs(
        cls, p: str, ignore_hidden_dir: bool = True, *, check_exist: bool = False
    ) -> typing.List[str]:
        """
        返回一个路径下所有的文件夹
        :param p: 给定路径
        :param ignore_hidden_dir: 是否忽略隐藏文件
        :param check_exist: 是否进行预检查
        :return: 返回给定路径下的所有的目录
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        lst = []
        for root, dirs, _ in os.walk(p):
            for d in dirs:
                if ignore_hidden_dir and cls.is_contain_hidden_dir(root):
                    break
                full_path = os.path.join(root, d)
                lst.append(full_path)

        return lst

    @classmethod
    def list_files(
        cls, p: str, ignore_hidden_dir: bool = True, *, check_exist: bool = False
    ) -> typing.List[str]:
        """
        返回一个路径下的所有文件
        :param p: 给定路径
        :param ignore_hidden_dir: 是否忽略隐藏文件, 默认忽略
        :param check_exist: 是否进行预检查
        :return: 返回给定路径下所有的文件路径
        """
        if check_exist:
            cls.is_exist(p)
        lst = []
        for root, _, files in os.walk(p):
            for file in files:
                if ignore_hidden_dir and cls.is_contain_hidden_dir(root):
                    break
                full_path = os.path.join(root, file)
                lst.append(full_path)

        return lst

    @classmethod
    def get_basename_from_path(cls, p: str) -> str:
        """
        从一个路径中获取文件名称
        :param p: 给定路径
        :return: 文件名称
        """
        return os.path.basename(p)

    @classmethod
    def get_extension_from_path(cls, p: str) -> str:
        """
        从一个路径中获取文件后缀
        :param p: 给定路径
        :return: 文件扩展名
        """
        abs_path = os.path.abspath(p)
        _, extension = os.path.splitext(abs_path)
        return extension

    @classmethod
    def is_match_extension(cls, p: str, extension: str) -> bool:
        """
        给定文件名是否匹配给定的
        :param p: 给定路径
        :param extension: 给定扩展名
        :return: 文件名称是否匹配
        """
        if StringUtil.is_blank(extension):
            raise ValueError(f"'{p}' is not a file extension")

        # 判断是否是一个文件
        cls.is_file(p, raise_exception=True)
        # 获取文件扩展名
        file_extension = cls.get_extension_from_path(p)

        return eq(file_extension, extension) or eq(file_extension, "." + extension)

    @classmethod
    def get_file_from_dir_by_extension(
        cls, p: str, *, extension: str = "sql"
    ) -> typing.List[str]:
        """
        返回给定的扩展名匹配的文件
        :param p:  给定路径
        :param extension:  给定扩展名
        :return: 所有匹配的文件
        """
        file_lst = []
        for f_path, dirs, fs in os.walk(p):
            for f in fs:
                abs_file_path = os.path.join(f_path, f)
                if cls.is_match_extension(abs_file_path, extension):
                    file_lst.append(abs_file_path)

        return file_lst

    @classmethod
    def get_file_lines(cls, f: str) -> int:
        """
        计算文件行数

        Parameters
        ----------
        f : str
            文件路径

        Returns
        -------
        int
            行数
        """
        with open(f, "r") as f_obj:
            i = -1
            for i, _ in enumerate(f_obj):
                pass
        return i + 1


class SysUtil(object):
    @classmethod
    def get_platform_info(cls) -> str:
        """
        获取平台信息
        :return: 平台信息
        """
        return platform.platform()

    @classmethod
    def is_mac_platform(cls) -> bool:
        """
        判断平台是否是mac
        :return: 是否是 mac 平台
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "macos", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_linux_platform(cls) -> bool:
        """
        判断平台是否是linux
        :return: 是否是linux
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "linux", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_windows_platform(cls) -> bool:
        """
        判断平台是否是windows
        :return: 是否是windows
        """
        platform_info = cls.get_platform_info()
        if StringUtil.is_startswith(platform_info, "windows", case_insensitive=True):
            return True
        return False

    @classmethod
    def is_py2(cls) -> bool:
        """
        判断是否Python2
        :return: 是否Python2
        """
        if sys.version_info >= (3, 0):
            return False
        if sys.version_info < (3, 0):
            return True
        raise ValueError("cannot determine if it's python2")

    @classmethod
    def is_py3(cls):
        """
        判断是否Python3
        :return: 是否是Python3
        """
        if (3, 0) <= sys.version_info <= (4, 0):
            return True
        else:
            return False

    @classmethod
    def get_system_property(
        cls, name: str, default_value: str = "", *, quiet: bool = False
    ) -> typing.Any:
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
                warnings.warn(
                    f"get system property {name} error: {e}, will return default value, {default_value}"
                )
        else:
            return res if res is not None else default_value

    def get_system_properties(self, quiet: bool = False) -> typing.Dict[str, str]:
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
