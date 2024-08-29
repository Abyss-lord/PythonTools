#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   csvutils.py
@Date       :   2024/08/15
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/15
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import csv
import io
from collections.abc import Generator
from os import PathLike
from typing import Any

from pythontools.core.constants.string_constant import CharsetUtil
from pythontools.core.io.fileutils import FileUtil


class CsvUtil:
    CSV_EXTENSION = "csv"

    @classmethod
    def is_csv(cls, f_name: str | PathLike) -> bool:
        """
        判断给定的文件是否是 csv 文件

        Parameters
        ----------
        f_name : str | PathLike
            待判断的文件路径

        Returns
        -------
        bool
            如果是 csv 文件，返回 True, 否则返回 False
        """
        path_obj = FileUtil.get_path_object(f_name)
        return FileUtil.is_match_extension(path_obj, cls.CSV_EXTENSION)
        path_obj = FileUtil.get_path_object(f_name)
        return FileUtil.is_match_extension(path_obj, cls.CSV_EXTENSION)

    @classmethod
    def get_dicts_from_csv(
        cls,
        f_name: str | PathLike,
        encoding: str = CharsetUtil.UTF_8,
        newline: str = "",
        delimiter: str = ",",
    ) -> Generator[dict[str | Any, str | Any], Any, None]:
        path_obj = FileUtil.get_path_object(f_name)
        path_obj = FileUtil.get_path_object(f_name)
        with open(path_obj, encoding=encoding, newline=newline) as f_in:
            csv_reader = csv.DictReader(f_in, delimiter=delimiter)
            yield from csv_reader
            FileUtil

    @classmethod
    def save_dicts_to_csv(
        cls,
        in_list: list[dict[str, str]],
        f_name: str,
        field_names: str,
        encoding: str = CharsetUtil.UTF_8,
        newline: str = "",
        delimiter: str = ",",
    ):
        path_obj = FileUtil.get_path_object(f_name)
        path_obj = FileUtil.get_path_object(f_name)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(path_obj, "w", encoding=encoding, newline=newline) as f_out:
            csv_writer = csv.DictWriter(f_out, fieldnames=field_names, delimiter=delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(in_list)

    @classmethod
    def get_lists_from_csv(cls, encoding="utf-8", newline="", delimiter=","):
        raise NotImplementedError()

    @classmethod
    def save_lists_to_csv(cls, f_name, field_names, encoding="utf-8", newline="", delimiter=","):
        raise NotImplementedError()

    @classmethod
    def get_fieldnames_from_csv(cls, encoding="utf-8", newline="", delimiter=","):
        raise NotImplementedError()

    @classmethod
    def get_namedtuple_from_csv(cls, f_name, encoding="utf-8", newline="", delimiter=","):
        raise NotImplementedError()

    @classmethod
    def save_namedtuple_to_csv(cls, in_list, f_name, field_names, encoding="utf-8", newline="", delimiter=","):
        raise NotImplementedError()

    @classmethod
    def create_stream_csv(cls, data: list[dict[str, str]]) -> io.StringIO:
        raise NotImplementedError()
