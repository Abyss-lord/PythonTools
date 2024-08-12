#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   fileutils.py
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
import os
import time
from operator import eq

from pythontools.core.utils.basicutils import StringUtil


class OsUtil:
    WINDOWS_LINE_ENDING = "\r\n"
    LINUX_LINE_ENDING = "\n"

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
        ValueError
            如果路径不存在且raise_exception=True, 则引发 FileNotFoundError 异常
        """
        # 检查路径是否存在
        if StringUtil.is_blank(p):
            return False
        if os.path.exists(p):
            return True

        if raise_exception:
            raise ValueError(p)

        return False

    @classmethod
    def is_dir(cls, p: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定路径是否是文件夹

        Parameters
        ----------
        p : str
            待检测路径
        raise_exception : bool, optional
            当给定路径不存在的时候是否抛出异常, by default False

        Returns
        -------
        bool
            给定路径是否是文件夹

        Raises
        ------
        ValueError
            当给定路径不存在且 raise_exception=True 时, 则抛出 ValueError 异常
        """
        if StringUtil.is_blank(p):
            return False
        if cls.is_exist(p, raise_exception=raise_exception):
            return os.path.isdir(p)

        return False

    # @Param p: 文件路径
    # @Param raise_exception: 如果文件不存在是否引发异常, 默认不引发异常
    @classmethod
    def is_file(cls, p: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定路径是否是文件

        Parameters
        ----------
        p : str
            待检测路径
        raise_exception : bool, optional
            当给定路径不存在的时候是否抛出异常, by default False

        Returns
        -------
        bool
            给定路径是否是文件

        Raises
        ------
        ValueError
            当给定路径不存在且 raise_exception=True 时, 则抛出 ValueError 异常
        """
        if StringUtil.is_blank(p):
            return False
        if cls.is_exist(p, raise_exception=raise_exception):
            return os.path.isfile(p)

        return False

    @classmethod
    def is_root_path(cls, p: str) -> bool:
        """
        判断给定路径是否是根目录

        Parameters
        ----------
        p : str
            待检测路径

        Returns
        -------
        bool
            是否是根目录
        """
        if StringUtil.is_blank(p):
            return False

        return os.path.ismount(p)

    @classmethod
    def is_hidden_dir(cls, base_name: str) -> bool:
        """
        判断给定名称是否是隐藏文件夹

        Parameters
        ----------
        base_name : str
            待检测名称

        Returns
        -------
        bool
            是否是隐藏文件夹
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
        判断给定路径中是否含有隐藏文件夹

        Parameters
        ----------
        p : str
            待检测路径

        Returns
        -------
        bool
            是否含有隐藏文件夹
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

        Parameters
        ----------
        p : str
            待检测文件路径
        time_format : str, optional
            时间格式, by default "%Y-%m-%d %H:%M:%S"
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        str
            文件创建时间
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)
        t = os.path.getctime(p)
        format_time = time.strftime(time_format, time.localtime(t))
        return format_time

    @classmethod
    def list_dirs(cls, p: str, ignore_hidden_dir: bool = True, *, check_exist: bool = False) -> list[str]:
        """
        返回一个文件夹中的所有文件夹

        Parameters
        ----------
        p : str
            给定的路径
        ignore_hidden_dir : bool, optional
            是否忽略隐藏文件夹, by default True
        check_exist : bool, optional
            是否进行检查, by default False

        Returns
        -------
        typing.List[str]
            给定路径下的所有文件夹
        """
        if check_exist:
            cls.is_dir(p, raise_exception=True)

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
        cls,
        p: str,
        *,
        check_exist: bool = False,
        ignore_hidden_dir: bool = True,
    ) -> list[str]:
        """
        返回给定路径下的所有文件

        Parameters
        ----------
        p : str
            给定的路径
        ignore_hidden_dir : bool, optional
            是否忽略隐藏文件, by default True
        check_exist : bool, optional
            是否进行检查, by default False

        Returns
        -------
        typing.List[str]
            给定路径下的所有文件
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
    def get_extension_from_path(cls, p: str, *, check_exist: bool = False) -> str:
        """
        从给定路径中获取文件后缀

        Parameters
        ----------
        p : str
            待提取路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        str
            文件后缀
        """
        abs_path = os.path.abspath(p)
        if check_exist:
            cls.is_file(p, raise_exception=True)
        _, extension = os.path.splitext(abs_path)
        return extension

    @classmethod
    def is_match_extension(cls, p: str, extension: str, *, check_exist: bool = False) -> bool:
        """
        判断给定的文件路径是否与给定的扩展名匹配

        Parameters
        ----------
        p : str
            待检测路径
        extension : str
            要匹配的扩展名

        Returns
        -------
        bool
            是否匹配

        Raises
        ------
        ValueError
            当给定的扩展名为空时, 则抛出 ValueError 异常
        """
        if StringUtil.is_blank(extension):
            raise ValueError(f"'{p}' is not a file extension")

        # 判断是否是一个文件
        if check_exist:
            cls.is_file(p, raise_exception=True)
        # 获取文件扩展名
        file_extension = cls.get_extension_from_path(p)

        return eq(file_extension, extension) or eq(file_extension, "." + extension)

    @classmethod
    def get_file_from_dir_by_extension(cls, p: str, *, extension: str = "sql") -> list[str]:
        """
        返回给定的扩展名匹配的文件
        :param p:  给定路径
        :param extension:  给定扩展名
        :return: 所有匹配的文件
        """
        files = cls.list_files(p, check_exist=True)
        return [f for f in files if cls.is_match_extension(f, extension)]

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
        with open(f) as f_obj:
            i = -1
            for i, _ in enumerate(f_obj):
                pass
        return i + 1

    @classmethod
    def windows_to_linux_line_ending(cls, text: str | bytes) -> str:
        """
        将Windows换行符转换为Linux换行符

        Parameters
        ----------
        text : str
            待转换文本

        Returns
        -------
        str
            转换后的文本
        """
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        return text.replace(cls.WINDOWS_LINE_ENDING, cls.LINUX_LINE_ENDING)

    @classmethod
    def linux_to_windows_line_ending(cls, text: str | bytes) -> str:
        """
        将Linux换行符转换为Windows换行符

        Parameters
        ----------
        text : str
            待转换文本

        Returns
        -------
        str
            转换后的文本
        """
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        return text.replace(cls.LINUX_LINE_ENDING, cls.WINDOWS_LINE_ENDING)
