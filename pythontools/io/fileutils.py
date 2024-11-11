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
import functools
import os
import re
import tempfile
import time
import unicodedata
import uuid
from datetime import datetime
from operator import eq
from os import PathLike
from pathlib import Path

from pythontools.core.constants.string_constant import CharsetUtil
from pythontools.core.utils.basicutils import DatetimeUtil, SequenceUtil, StringUtil, TimeUnit


class FileUtil:
    """
    文件、系统工具类

    Attributes
    ----------
    WINDOWS_LINE_ENDING : str
        windows 换行符
    LINUX_LINE_ENDING : str
        linux 换行符

    Methods
    -------
    is_exist(p: str | PathLike[str], raise_exception: bool = False) -> bool
        检查路径是否存在
    is_dir(p: str | PathLike[str], raise_exception: bool = False) -> bool
        判断给定路径是否是文件夹
    is_file(p: str | PathLike[str], raise_exception: bool = False) -> bool
        判断给定路径是否是文件
    is_root_path(p: str | PathLike[str]) -> bool
        判断给定路径是否是根目录
    is_ignore(p: str | PathLike[str]) -> bool
        判断给定名称是否是隐藏文件夹
    is_contain_ignore(p: str | PathLike[str]) -> bool
        判断给定路径中是否含有隐藏文件夹
    is_empty_dir(p: str | PathLike[str]) -> bool
        判断给定路径是否为空文件夹
    is_not_empty_dir(p: str | PathLike[str]) -> bool
        判断给定路径是否是空文件夹
    is_match_extension(p: str | PathLike[str], extension: str, check_exist: bool = False) -> bool
        判断给定的文件路径是否与给定的扩展名匹配
    is_newer_than(p: str | PathLike[str], reference: float | int | str | PathLike[str], *raise_exception: bool) -> bool
        判断给定的文件是否比给定的参考文件或者参考时间更新
    get_temp_file() -> tempfile._TemporaryFileWrapper
        获取一个临时文件对象
    get_create_time_in_nanoseconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录创建时间(纳秒)
    get_create_time_in_milliseconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录创建时间(毫秒)
    get_create_time_in_seconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录创建时间(秒)
    get_create_time_in_string_format(p: str | PathLike[str], check_exist: bool = False) -> str
        返回文件或目录创建时间(字符串格式)
    get_last_modify_time_in_nanoseconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录最后修改时间(纳秒)
    get_last_modify_time_in_milliseconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录最后修改时间(毫秒)
    get_last_modify_time_in_seconds(p: str | PathLike[str], check_exist: bool = False) -> int
        返回文件或目录最后修改时间(秒)
    get_last_modify_time_in_string_format(p: str | PathLike[str], check_exist: bool = False) -> str
        返回文件或目录最后修改时间(字符串格式)
    get_extension_from_path(p: str | PathLike[str]) -> str
        获取文件扩展名
    get_basename_from_path(p: str | PathLike[str]) -> str
        获取文件名
    get_extension_from_filename(filename: str) -> str
        获取文件扩展名
    get_line_cnt_of_file(p: str | PathLike[str], encoding: str = CharsetUtil.UTF_8) -> int
        获取文件行数
    list_files(p: str | PathLike[str], recursive: bool = False, include_ignore: bool = False) -> list[str]
        获取给定路径下的文件列表
    list_dirs(p: str | PathLike[str], recursive: bool = False, include_ignore: bool = False) -> list[str]
        获取给定路径下的文件夹列表
    windows_to_linux_line_ending(s: str) -> str
        windows 换行符转化为 linux 换行符
    linux_to_windows_line_ending(s: str) -> str
        linux 换行符转化为 windows 换行符
    """

    WINDOWS_LINE_ENDING = "\r\n"
    LINUX_LINE_ENDING = "\n"
    FILENAME_ASCII_STRIP_RE = re.compile(r"[^A-Za-z0-9_.-]")
    WINDOWS_DEVICE_FILES = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(10)),
        *(f"LPT{i}" for i in range(10)),
    }

    @classmethod
    def is_exist(
        cls,
        p: str | PathLike[str],
        *,
        raise_exception: bool = False,
    ) -> bool:
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

        path_object = cls.get_path_object(p)

        if path_object.exists():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

    @classmethod
    def is_not_exist(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否不存在

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            路径是否不存在
        """
        return not cls.is_exist(p)

    @classmethod
    def is_dir(
        cls,
        p: str | PathLike[str],
        *,
        raise_exception: bool = False,
    ) -> bool:
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
        path_obj = cls.get_path_object(p)

        if path_obj.is_dir():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

    @classmethod
    def is_not_dir(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否不是文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            给定路径是否不是文件夹
        """
        return not cls.is_dir(p)

    # @Param p: 文件路径
    # @Param raise_exception: 如果文件不存在是否引发异常, 默认不引发异常
    @classmethod
    def is_file(
        cls,
        p: str | PathLike[str],
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断给定路径是否是文件

        Parameters
        ----------
        p : str | PathLike[str]
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

        path_obj = cls.get_path_object(p)

        if path_obj.is_file():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

    @classmethod
    def is_not_file(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否不是文件

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            给定路径是否不是文件
        """
        return not cls.is_file(p)

    @classmethod
    def is_root_path(
        cls,
        p: str | PathLike[str],
    ) -> bool:
        """
        判断给定路径是否是根目录

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            是否是根目录
        """
        path_obj = cls.get_path_object(p)

        return path_obj.is_mount()

    @classmethod
    def is_not_root_path(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否不是根目录

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            是否不是根目录
        """
        return not cls.is_root_path(p)

    @classmethod
    def is_ignore(
        cls,
        p: str | PathLike[str],
    ) -> bool:
        """
        判断给定名称是否是隐藏文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测名称

        Returns
        -------
        bool
            是否是隐藏文件夹或者
        """
        path_obj = cls.get_path_object(p)

        basename = cls.get_basename_from_path(path_obj)
        #
        return bool(
            StringUtil.starts_with(basename, ".") or StringUtil.starts_with(basename, "__"),
        )

    @classmethod
    def is_not_ignore(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定名称是否不是隐藏文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测名称

        Returns
        -------
        bool
            是否不是隐藏文件夹
        """
        return not cls.is_ignore(p)

    @classmethod
    def is_contain_ignore(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径中是否含有隐藏文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            是否含有隐藏文件夹
        """

        path_obj = cls.get_path_object(p)

        while not cls.is_root_path(path_obj):
            if cls.is_ignore(path_obj):
                return True
            path_obj = path_obj.parent

        return False

    @classmethod
    def is_not_contain_ignore(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径中是否不含有隐藏文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            是否不含有隐藏文件夹
        """
        return not cls.is_contain_ignore(p)

    @classmethod
    def is_empty_dir(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否为空文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            是否为空文件夹
        """
        path_obj = cls.get_path_object(p)
        if not cls.is_dir(path_obj):
            return False

        return cls.list_files_from_path(path_obj) == [] and cls.list_dirs_from_path(path_obj) == []

    @classmethod
    def is_not_empty_dir(cls, p: str | PathLike[str]) -> bool:
        """
        判断给定路径是否是空文件夹

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            文件夹是否为非空文件夹
        """
        return not cls.is_empty_dir(p)

    @classmethod
    def is_match_extension(
        cls,
        p: str | PathLike[str],
        extension: str,
        *,
        check_exist: bool = False,
    ) -> bool:
        """
        判断给定的文件路径是否与给定的扩展名匹配

        Parameters
        ----------
        p : str | PathLike[str]
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

        return eq(file_extension, extension) or eq(file_extension, f".{extension}")

    def is_match_extensions(
        self,
        p: str | PathLike[str],
        *extensions,
    ) -> bool:
        """
        判断给定的文件路径是否与给定的扩展名匹配

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        bool
            如果文件扩展名在给定的扩展名列表中则返回True, 否则返回False
        """
        return any(self.is_match_extension(p, extension) for extension in extensions)

    @classmethod
    def is_newer_than(
        cls, p: str | PathLike[str], reference: float | int | str | PathLike[str], *raise_exception: bool
    ) -> bool:
        """
        判断给定的文件是否比给定的参考文件或者参考时间更新

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件路径
        reference : int | str | PathLike[str],
            参考时间(秒), 或者参考文件

        Returns
        -------
        bool
            如果文件比参考文件或者参考时间更新返回True, 否则返回False

        Raises
        ------
        ValueError
            如果参考文件不存在则抛出 ValueError 异常
        """
        if isinstance(reference, PathLike) and not cls.is_exist(reference, raise_exception=False):  # type: ignore
            return False

        if isinstance(reference, (float | int)):
            reference_modified_time_in_seconds = reference
        else:
            reference_modified_time_in_seconds = cls.get_last_modify_time_in_seconds(reference, check_exist=True)

        file_modified_time_in_seconds = cls.get_last_modify_time_in_seconds(p, check_exist=True)

        if file_modified_time_in_seconds > reference_modified_time_in_seconds:
            return True

        if raise_exception:
            raise ValueError(f"{p} is not newer than {reference}")

        return False

    @classmethod
    def get_temp_file(cls) -> tempfile._TemporaryFileWrapper:
        """
        获取一个临时文件对象

        Returns
        -------
        tempfile._TemporaryFileWrapper
            临时文件对象
        """
        return tempfile.NamedTemporaryFile(delete=False)

    @classmethod
    def get_create_time_in_nanoseconds(
        cls,
        p: str | PathLike[str],
        *,
        check_exist: bool = False,
    ) -> int:
        """
        返回文件或目录创建时间(纳秒)

        Parameters
        ----------
        p : str | PathLike[str]
            给定的文件或者目录路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        int
            返回文件或目录创建时间(纳秒)
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        path_obj = cls.get_path_object(p)
        return path_obj.stat().st_ctime_ns

    @classmethod
    def get_create_time_in_milliseconds(
        cls,
        p: str | PathLike[str],
        *,
        check_exist: bool = False,
    ) -> float | int:
        """
        返回文件或目录创建时间(毫秒)

        Parameters
        ----------
        p : str | PathLike[str]
            文件或目录路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        float | int
            返回文件或目录创建时间(毫秒)
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        t = cls.get_create_time_in_nanoseconds(p, check_exist=True)
        return DatetimeUtil.convert_time(
            t,
            TimeUnit.NANOSECONDS,
            TimeUnit.MILLISECONDS,
        )

    @classmethod
    def get_create_time_in_seconds(
        cls,
        p: str | PathLike[str],
        *,
        check_exist: bool = False,
    ) -> float:
        """
        返回文件或目录创建时间(秒)

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件或目录路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        float
            返回文件或目录创建时间(秒)
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        t = cls.get_create_time_in_nanoseconds(p, check_exist=True)
        return DatetimeUtil.convert_time(
            t,
            TimeUnit.NANOSECONDS,
            TimeUnit.SECONDS,
        )

    @classmethod
    def get_create_time_in_string_format(
        cls,
        p: str | PathLike[str],
        time_format: str = "%Y-%m-%d %H:%M:%S",
        *,
        check_exist: bool = False,
    ) -> str:
        """
        以字符串形式返回文件或者目录创建时间

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件或者目录路径
        time_format : str, optional
            时间格式, by default "%Y-%m-%d %H:%M:%S"
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        str
            文件创建时间(字符串格式)
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        create_time_in_seconds = cls.get_create_time_in_seconds(p, check_exist=True)
        return time.strftime(
            time_format,
            time.localtime(create_time_in_seconds),
        )

    @classmethod
    def get_last_modify_time_in_nanoseconds(cls, p: str | PathLike[str], *, check_exist: bool = False) -> int:
        """
        以纳秒为单位返回文件最后修改时间

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        int
            文件最后修改时间(纳秒)
        """
        path_obj = cls.get_path_object(p)
        if check_exist:
            cls.is_exist(p, raise_exception=True)
        return path_obj.stat().st_mtime_ns

    @classmethod
    def get_last_modify_time_in_milliseconds(cls, p: str | PathLike[str], *, check_exist: bool = False) -> float | int:
        """
        以毫秒为单位返回文件最后修改时间

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        int
            文件最后修改时间(毫秒)
        """
        last_modify_time_in_nanoseconds = cls.get_last_modify_time_in_nanoseconds(p, check_exist=check_exist)
        return DatetimeUtil.convert_time(
            last_modify_time_in_nanoseconds,
            TimeUnit.NANOSECONDS,
            TimeUnit.MILLISECONDS,
        )

    @classmethod
    def get_last_modify_time_in_seconds(cls, p: str | PathLike[str], *, check_exist: bool = False) -> float:
        """
        以秒为单位返回文件最后修改时间

        Parameters
        ----------
        p : str | PathLike[str]
            待检测文件路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        int
            文件最后修改时间(秒)
        """
        last_modify_time_in_nanoseconds = cls.get_last_modify_time_in_nanoseconds(p, check_exist=check_exist)
        return DatetimeUtil.convert_time(last_modify_time_in_nanoseconds, TimeUnit.NANOSECONDS, TimeUnit.SECONDS)

    @classmethod
    def get_last_modify_time_in_string_format(
        cls,
        p: str | PathLike[str],
        time_format: str = "%Y-%m-%d %H:%M:%S",
        *,
        check_exist: bool = False,
    ) -> str:
        """
        以字符串形式返回文件最后修改时间

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
            文件最后修改时间(字符串格式)
        """
        if check_exist:
            cls.is_exist(p, raise_exception=True)

        last_modify_time_in_second = cls.get_last_modify_time_in_seconds(p, check_exist=True)
        return time.strftime(time_format, time.localtime(last_modify_time_in_second))

    @classmethod
    def list_dirs_from_path_ignore_hidden(cls, p: str | PathLike[str]) -> list[Path]:
        """
        列出给定路径下所有的非隐藏文件夹

        Parameters
        ----------
        p : str | PathLike[str] | Path
            待检测路径

        Returns
        -------
        list[Path]
            非隐藏文件夹列表
        """
        return cls.list_dirs_from_path(
            p,
            cls.is_not_contain_ignore,
        )

    @classmethod
    def list_dirs_from_path(
        cls,
        p: str | PathLike[str],
        *predicates,
    ) -> list[Path]:
        path_obj = cls.get_path_object(p).absolute()
        return [
            cls.get_path_object(f_path)
            for f_path, _, _ in os.walk(path_obj)
            if SequenceUtil.is_empty(predicates)
            or all(predicate(f_path) for predicate in predicates)
            and cls.is_dir(f_path)
        ]

    @classmethod
    def list_files_from_path_ignore_hidden(
        cls,
        p: str | Path,
    ) -> list[Path]:
        """
        列出给定路径下所有的非隐藏文件

        Parameters
        ----------
        p : str | PathLike[str]
            待检测路径

        Returns
        -------
        list[Path]
            非隐藏文件列表
        """
        return cls.list_files_from_path(
            p,
            cls.is_not_contain_ignore,
        )

    @classmethod
    def list_files_from_path(
        cls,
        p: str | Path,
        *predicates,
    ) -> list[Path]:
        """
        列出给定路径下所有的符合规则的文件

        Parameters
        ----------
        p : str | Path
            待检测路径

        Returns
        -------
        list[Path]
            给定路径下所有符合提取规则的文件列表
        """
        path_obj = cls.get_path_object(p)

        return [
            Path(f_path) / f
            for f_path, _, fs in os.walk(path_obj)
            for f in fs
            if SequenceUtil.is_empty(predicates) or all(predicate(Path(f_path) / f) for predicate in predicates)
        ]

    @classmethod
    def get_basename_from_path(cls, p: str | PathLike[str]) -> str:
        """
        从一个路径中获取文件名称
        :param p: 给定路径
        :return: 文件名称
        """
        path_obj = cls.get_path_object(p)
        return path_obj.name

    @classmethod
    def get_extension_from_path(
        cls,
        p: str | PathLike[str],
        *,
        check_exist: bool = False,
    ) -> str:
        """
        从给定路径中获取文件后缀

        Parameters
        ----------
        p : str | PathLike[str]
            待提取路径
        check_exist : bool, optional
            是否进行路径检查, by default False

        Returns
        -------
        str
            文件后缀
        """
        path_obj = cls.get_path_object(p)

        if check_exist:
            cls.is_file(path_obj, raise_exception=True)

        return path_obj.suffix

    @classmethod
    def get_file_from_dir_by_extension(cls, p: str, *, extension: str = "sql") -> list[Path]:
        """
        返回给定的扩展名匹配的文件

        Parameters
        ----------
        p : str
            给定的目录
        extension : str, optional
            匹配的扩展名, by default "sql"

        Returns
        -------
        list[Path]
            符合条件的文件列表
        """
        predicate_func = functools.partial(cls.is_match_extension, extension=extension, check_exist=False)
        return cls.list_files_from_path(p, predicate_func)

    @classmethod
    def get_line_cnt_of_file(cls, f: str) -> int:
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
        with open(Path(f)) as f_obj:
            i = -1
            for i, _ in enumerate(f_obj):
                pass
        return i + 1

    @classmethod
    def get_lines(cls, fs: str) -> list[str]:
        """
        读取文件所有行

        Parameters
        ----------
        f : str | Path
            文件路径

        Returns
        -------
        list[str]
            文件所有行
        """
        encoding_lst = ["utf-8", "gbk", "gb2312", "gb18030"]
        path_obj = cls.get_path_object(fs)
        for encoding in encoding_lst:
            try:
                with open(path_obj, encoding=encoding) as file:
                    return list(file)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Can not decode file {fs}")

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

    @classmethod
    def get_path_object(
        cls,
        p: str | PathLike[str],
    ) -> Path:
        if isinstance(p, Path):
            return p
        if isinstance(p, str):
            return Path(p)
        elif isinstance(p, bytes):
            return Path(p.decode(CharsetUtil.UTF_8))

        return Path(p)  # type: ignore

    @classmethod
    def generate_random_file_name(cls, seed_name: str) -> str:
        """
        创建随机文件名称

        Parameters
        ----------
        seed_name : str
            初始名称

        Returns
        -------
        str
            随机文件名
        """
        dt = datetime.now()
        return f'{dt.strftime("%Y%m%d_%H%M%S%f")}_{uuid.uuid4().hex[:6]}_{cls.secure_filename(seed_name)}'

    @classmethod
    def secure_filename(cls, filename: str) -> str:
        """
        传入一个文件名，它会返回一个安全版本。这文件名可以安全地存储在普通文件系统中并传递

        Parameters
        ----------
        filename : str
            待转换文件名

        Returns
        -------
        str
            安全的文件名称，可能会出现空字符串

        Notes
        -------
        ref: https://github.com/pallets/werkzeug/blob/65d3a84a28bad7752f333a082360682adb3d925c/src/werkzeug/utils.py#L195
        """
        filename = unicodedata.normalize("NFKD", filename)
        filename = filename.encode("ascii", "ignore").decode("ascii")

        for sep in os.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, " ")
        filename = str(cls.FILENAME_ASCII_STRIP_RE.sub("", "_".join(filename.split()))).strip("._")

        if os.name == "nt" and filename and filename.split(".")[0].upper() in cls.WINDOWS_DEVICE_FILES:
            filename = f"_{filename}"

        return filename
