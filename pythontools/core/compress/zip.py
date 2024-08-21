#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   zip.py
@Date       :   2024/08/13
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/13
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import os
import tempfile
import zipfile
from datetime import datetime
from os import PathLike
from pathlib import Path
from zipfile import ZipInfo

from pythontools.core.io.fileutils import FileUtil
from pythontools.core.utils.basicutils import StringUtil


class ZipUtil:
    """
    压缩工具类

    Attributes
    ----------
    None

    Methods
    -------
    replace_zip_data(zip_file: str, filename: str, data: str) -> None
        替换归档文件的内容
    zip_dir(dir_path: str | PathLike, zip_name: str) -> Path
        压缩一个目录
    unzip_to_dir(zip_name: str | PathLike, path: str | PathLike) -> Path
        解压 zip 到指定目录
    remove_from_zip(zip_file: str | PathLike[str], filename: str | PathLike[str]) -> Path
        从归档文件中删除指定文件
    get_zip_infolist(zip_file) -> list[ZipInfo]
        获取压缩文件列表
    get_from_zip(zip_file: str | PathLike[str], target_file: str | PathLike[str], mode="r") -> bytes
        从归档文件中获取指定文件的内容

    NOTES:
    ------
    ref: https://gist.github.com/UmbrellaBurns/284a27690bad2a87d22201445b25ca6a
    """

    @classmethod
    def replace_zip_data(cls, zip_file: str, filename: str, data: str) -> None:
        """
        替换归档文件的内容

        Parameters
        ----------
        zip_file : str
            归档文件
        filename : str
            要替换的文件名称
        data : str
            替换数据
        """
        # 1. 构建临时文件
        now = datetime.now().strftime("%d.%m.%y_%I.%M")
        temp_zip = os.path.join(tempfile.gettempdir(), zip_file.replace(".", f"_{now}."))

        # 2. 将非替换内容写入到临时文件
        with zipfile.ZipFile(zip_file, "r") as zip_in, zipfile.ZipFile(temp_zip, "w") as zip_out:
            for item in zip_in.infolist():
                file_data = zip_in.read(item.filename)
                if StringUtil.not_equals(item.filename, filename):
                    zip_out.writestr(item, file_data)

        # 3. 删除旧的归档文件，重命名临时文件->归档文件
        os.remove(zip_file)
        os.rename(temp_zip, zip_file)

        # 4. 写入替换内容到归档文件
        with zipfile.ZipFile(zip_file, "a", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr(filename, data)

    @classmethod
    def zip_dir(cls, dir_path: str | PathLike, zip_name: str) -> Path:
        """
        压缩一个目录

        Parameters
        ----------
        dir_path : str | PathLike
            目录路径
        zip_name : str
            归档文件名称

        Returns
        -------
        Path
            表示归档文件的 Path 对象

        Raises
        ------
        ValueError
            如果 dir_path 不是一个有效的目录, 则抛出 ValueError
        """
        zip_path_obj = Path(zip_name)
        if not FileUtil.is_dir(zip_path_obj):
            raise ValueError("Must give a valid directory")

        with zipfile.ZipFile(zip_path_obj, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
            path_obj_lst = FileUtil.list_files(dir_path)
            for p in path_obj_lst:
                z.write(p, p.relative_to(dir_path))

        return zip_path_obj

    @classmethod
    def unzip_to_dir(
        cls,
        zip_name: str | PathLike,
        path: str | PathLike,
    ) -> Path:
        """
        解压 zip 到指定目录

        Parameters
        ----------
        zip_name : str | PathLike
            归档文件名称
        path : str | PathLike
            解压目录路径

        Returns
        -------
        Path
            表示解压目录的 Path 对象
        """
        path_obj = Path(path)
        with zipfile.ZipFile(path_obj, "r") as z:
            for item in z.infolist():
                z.extract(item, path)

        return path_obj

    @classmethod
    def remove_from_zip(cls, zip_file: str | PathLike[str], filename: str | PathLike[str]) -> Path:
        """
        从归档文件中删除指定文件

        Parameters
        ----------
        zip_file : str | PathLike[str]
            给定的归档文件
        filename : str | PathLike[str]
            要删除的文件

        Returns
        -------
        Path
            表示归档文件的 Path 对象
        """
        if isinstance(zip_file, PathLike):
            zip_file = str(zip_file)

        if isinstance(filename, PathLike):
            filename = str(filename)

        now = datetime.now().strftime("%d.%m.%y_%I.%M")
        temp_zip = os.path.join(tempfile.gettempdir(), zip_file.replace(".", f"_{now}."))

        with zipfile.ZipFile(zip_file, "r") as zip_in, zipfile.ZipFile(temp_zip, "w") as zip_out:
            for item in zip_in.infolist():
                file_data = zip_in.read(item.filename)
                if StringUtil.not_equals(item.filename, filename):
                    zip_out.writestr(item, file_data)

        os.remove(zip_file)
        os.rename(temp_zip, zip_file)

        return Path(zip_file)

    @classmethod
    def get_zip_infolist(cls, zip_file) -> list[ZipInfo]:
        """
        获取压缩文件列表

        Parameters
        ----------
        zip_file : _type_
            给定的归档文件

        Returns
        -------
        list[ZipInfo]
            压缩文件列表
        """

        with zipfile.ZipFile(zip_file, "r") as zip_in:
            files_list: list[ZipInfo] = zip_in.infolist()

        return files_list

    @classmethod
    def get_from_zip(
        cls,
        zip_file: str | PathLike[str],
        target_file: str | PathLike[str],
        mode="r",
    ) -> bytes:
        """
        从归档文件中获取指定文件的内容

        Parameters
        ----------
        zip_file : str | PathLike[str]
            给定的归档文件
        target_file : str | PathLike[str]
            目标文件名称
        mode : str, optional
            读取模式, by default "r"

        Returns
        -------
        bytes
            读取的数据

        Raises
        ------
        AttributeError
            如果 target_file 不存在于归档文件中, 则抛出 AttributeError
        """
        if isinstance(target_file, PathLike):
            target_file = str(target_file)

        with zipfile.ZipFile(zip_file, mode=mode) as z:
            if target_file not in [x.filename for x in z.infolist()]:
                raise AttributeError(f"File {target_file} does not exists in zip archive")

            return z.read(target_file)
