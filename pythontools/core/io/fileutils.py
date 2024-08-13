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
import tempfile
import time
from operator import eq
from os import PathLike
from pathlib import Path

from pythontools.core.constants.string_constant import CharsetUtil
from pythontools.core.utils.basicutils import StringUtil
from pythontools.core.utils.datetimeutils import DatetimeUtil, TimeUnit


class OsUtil:
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

        path_object = cls.__get_path_object(p)

        if path_object.exists():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

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
        path_obj = cls.__get_path_object(p)

        if path_obj.is_dir():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

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

        path_obj = cls.__get_path_object(p)

        if path_obj.is_file():
            return True

        if raise_exception:
            raise ValueError(p)

        return False

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
        path_obj = cls.__get_path_object(p)

        return path_obj.is_mount()

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
        path_obj = cls.__get_path_object(p)

        basename = cls.get_basename_from_path(path_obj)

        if StringUtil.is_starts_with(basename, ".") or StringUtil.is_starts_with(basename, "__"):
            return True

        return False

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

        path_obj = cls.__get_path_object(p)

        while not cls.is_root_path(path_obj):
            if cls.is_ignore(path_obj):
                return True
            path_obj = path_obj.parent

        return False

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
        path_obj = cls.__get_path_object(p)
        if not cls.is_dir(path_obj):
            return False

        return cls.list_files(path_obj) == [] and cls.list_dirs(path_obj) == []

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

        return eq(file_extension, extension) or eq(file_extension, "." + extension)

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

        path_obj = cls.__get_path_object(p)
        t = path_obj.stat().st_ctime_ns
        return t

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
        create_time_in_milliseconds = DatetimeUtil.conver_time(t, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS)
        return create_time_in_milliseconds

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
        create_time_in_seconds = DatetimeUtil.conver_time(t, TimeUnit.NANOSECONDS, TimeUnit.SECONDS)

        return create_time_in_seconds

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
        format_time = time.strftime(time_format, time.localtime(create_time_in_seconds))

        return format_time

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
        path_obj = cls.__get_path_object(p)
        if check_exist:
            cls.is_exist(p, raise_exception=True)
        t = path_obj.stat().st_mtime_ns
        return t

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
        last_modify_time_in_mill = DatetimeUtil.conver_time(
            last_modify_time_in_nanoseconds, TimeUnit.NANOSECONDS, TimeUnit.MILLISECONDS
        )
        return last_modify_time_in_mill

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
        last_modify_time_in_second = DatetimeUtil.conver_time(
            last_modify_time_in_nanoseconds, TimeUnit.NANOSECONDS, TimeUnit.SECONDS
        )

        return last_modify_time_in_second

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
        format_time = time.strftime(time_format, time.localtime(last_modify_time_in_second))

        return format_time

    @classmethod
    def list_dirs(
        cls,
        p: str | PathLike[str],
        *,
        ignore_hidden_dir: bool = True,
        check_exist: bool = False,
    ) -> list[Path]:
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
        path_obj = cls.__get_path_object(p)

        if ignore_hidden_dir:
            return [i.absolute() for i in path_obj.rglob("*") if cls.is_dir(i) and not cls.is_contain_ignore(i)]
        else:
            return [i.absolute() for i in path_obj.rglob("*") if cls.is_dir(i)]

    @classmethod
    def list_files(
        cls,
        p: str | PathLike[str],
        *,
        check_exist: bool = False,
        ignore_hidden_dir: bool = True,
        extension: str = "",
    ) -> list[Path]:
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
            cls.is_dir(p, raise_exception=True)
        path_obj = cls.__get_path_object(p)

        wildcard = "*" if not extension else f"*.{extension}"

        if ignore_hidden_dir:
            return [i.absolute() for i in path_obj.rglob(wildcard) if cls.is_file(i) and not cls.is_contain_ignore(i)]
        else:
            return [i.absolute() for i in path_obj.rglob(wildcard) if cls.is_file(i)]

    @classmethod
    def get_basename_from_path(cls, p: str | PathLike[str]) -> str:
        """
        从一个路径中获取文件名称
        :param p: 给定路径
        :return: 文件名称
        """
        path_obj = cls.__get_path_object(p)
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
        path_obj = cls.__get_path_object(p)

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
        return cls.list_files(p, extension=extension)

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
    def __get_path_object(
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
