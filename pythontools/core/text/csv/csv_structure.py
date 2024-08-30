#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   csv_structure.py
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
from collections.abc import Generator, Mapping, Sequence
from os import PathLike
from typing import Any, NamedTuple, Self

from pythontools.core.constants.string_constant import CharPool, CharsetUtil
from pythontools.core.errors import UnsupportedOperationError
from pythontools.core.io.fileutils import FileUtil
from pythontools.core.utils.basicutils import SequenceUtil


class CsvConfig:
    """
    CSV 配置类

    Attributes
    ----------
    delimiter : str
        分隔符，默认是逗号
    strict_mode : bool
        是否严格模式，默认是 False
    lineterminator : str
        行终止符，默认是 \r\n
    text_qualifier : str
        文本限定符，默认是双引号
    skip_initial_space : bool
        是否跳过初始空格，默认是 False

    Methods
    -------
    set_delimiter(delimiter: str) -> Self
        设置分隔符
    set_strict_mode(strict_mode: bool) -> Self
        设置严格模式
    set_lineterminator(lineterminator: str) -> Self
        设置行终止符
    set_text_qualifier(text_qualifier: str) -> Self
        设置文本限定符
    set_skip_initial_space(skip_initial_space: bool) -> Self
        设置是否跳过初始空格
    """

    DEFAULT_DELIMITER = CharPool.COMMA
    DEFAULT_STRICT_MODE = False
    DEFAULT_skip_initial_space = False
    DEFAULT_TEXT_QUALIFIER = CharPool.DOUBLE_QUOTES
    DEFAULT_LINE_TERMINATOR = CharPool.CR + CharPool.LF

    def __init__(
        self,
        delimiter: str = DEFAULT_DELIMITER,
        strict_mode: bool = DEFAULT_STRICT_MODE,
        lineterminator: str = DEFAULT_LINE_TERMINATOR,
        text_qualifier: str = DEFAULT_TEXT_QUALIFIER,
        skip_initial_space: bool = DEFAULT_skip_initial_space,
    ) -> None:
        self.delimiter: str = delimiter
        self.strict_mode = strict_mode
        self.lineterminator = lineterminator
        self.text_qualifier = text_qualifier
        self.skip_initial_space = skip_initial_space

    def set_delimiter(self, delimiter: str) -> Self:
        self.delimiter = delimiter
        return self

    def set_strict_mode(self, strict_mode: bool) -> Self:
        self.strict_mode = strict_mode
        return self

    def set_lineterminator(self, lineterminator: str) -> Self:
        self.lineterminator = lineterminator
        return self

    def set_text_qualifier(self, text_qualifier: str) -> Self:
        self.text_qualifier = text_qualifier
        return self

    def set_skip_initial_space(self, skip_initial_space: bool) -> Self:
        self.skip_initial_space = skip_initial_space
        return self


class CsvRow:
    def __init__(
        self,
        line_num: int,
        data: list[Any] | Mapping[str, Any] | None,
        is_header: bool = False,
    ) -> None:
        self.ori_line_num: int = line_num
        self.is_header = is_header
        self.data: tuple[Any, ...] = None  # type: ignore

        if data is not None:
            self._set_data(data)

    def __str__(self) -> str:
        return f"{self.ori_line_num}: {self.data}, is_header: {self.is_header}"

    def get_cnt_of_fields(self) -> int:
        """
        返回数据字段的数量

        Returns
        -------
        int
            数据字段的数量
        """
        return SequenceUtil.get_length(self.data)

    def get_raw_data(self) -> tuple[Any, ...]:
        """
        返回一行的原始数据

        Returns
        -------
        tuple[Any, ...]
            行原始数据的拷贝
        """
        return tuple(list(self.data))

    def get_data_by_idx(self, idx: int) -> Any:
        """
        根据索引获取数据

        Parameters
        ----------
        idx : int
            指定的索引

        Returns
        -------
        Any
            索引对应的数据
        """
        return None if idx < 0 or idx >= self.get_cnt_of_fields() else self.data[idx]

    def to_namedtuple(self, model_cls: type[NamedTuple]) -> type[NamedTuple]:
        """
        转换成命名元祖

        Parameters
        ----------
        model_cls : NamedTuple
            要转换的命名元祖类

        Returns
        -------
        tuple
            该行数据转换成的命名元祖
        """
        return model_cls._make(self.data)  # type: ignore

    def to_dict(self, header_map: dict[str, int]) -> Mapping[str, Any]:
        """
        转换成字典

        Returns
        -------
        dict
            该行数据转换成的字典
        """
        length = self.get_cnt_of_fields()
        data_dict = {}
        for k, i in header_map.items():
            if i >= length:
                raise ValueError(f"{i} is out of range: {length}")

            data_dict[k] = self.data[i]

        return data_dict

    def _set_data(self, data) -> None:
        if self.data is not None:
            raise ValueError("already set")
        if isinstance(data, Sequence) and not isinstance(data, str):
            self.data = tuple(list(data))
        elif isinstance(data, Mapping):
            self.data = tuple(list(self.header_map.values()))
        else:
            raise TypeError("data must be a sequence or mapping")


class CsvHeader(CsvRow):
    """
    CSV 标题类

    Attributes
    ----------
    data : list[Any] | Mapping[str, Any] | None
        原始数据
    is_header : bool
        是否是标题行

    Methods
    -------
    to_dict(header_map: dict[str, int]) -> Mapping[str, Any]
        转换成字典
    to_namedtuple(model_cls: type[NamedTuple]) -> type[NamedTuple]
        转换成命名元祖

    Notes
    -----
    由于标题行数据自身即使标题也是数据, 所以无法转换成字典或命名元祖
    """

    def __init__(
        self,
        data: list[Any] | Mapping[str, Any] | None,
    ) -> None:
        super().__init__(0, data, True)

    def to_dict(self, header_map: dict[str, int]) -> Mapping[str, Any]:
        raise UnsupportedOperationError("is header, cannot convert to dict, only to the original data")

    def to_namedtuple(self, model_cls: type[NamedTuple]) -> type[NamedTuple]:
        raise UnsupportedOperationError("is header, cannot convert to namedtuple, only to the original data")


class CsvData:
    """
    CSV 数据类, 由多个CsvRow组成。
    """

    def __init__(
        self,
        header: CsvHeader,
        data: list[CsvRow] | None = None,
    ) -> None:
        self.header = header
        self.data: list[CsvRow] = [] if data is None else data
        self.header_map: dict[str, int] = {}
        self.cnt_of_row = -1

        self._initialize()

    def get_row_by_id(self, row_num: int) -> CsvRow | None:
        """
        根据行号返回 CsvRow 对象

        Parameters
        ----------
        row_num : int
            行号

        Returns
        -------
        CsvRow
            如果存在, 则返回对应的 CsvRow 对象, 否则返回 None
        """
        if row_num <= 0 or row_num > self.cnt_of_row:
            return None
        return self.data[row_num - 1]

    def get_idx_by_header(self, header_name: str) -> int:
        """
        根据给定的标题名称获取索引

        Parameters
        ----------
        header_name : str
            标题名称

        Returns
        -------
        int
            如果标题名存在, 则返回索引, 否则返回 -1
        """
        return self.header_map[header_name] if header_name in self.header_map else -1

    def get_value_by_header(self, header_name: str, row_num: int) -> Any:
        """
        根据给定的标题名称和行号获取对应的值

        Parameters
        ----------
        header_name : str
            字段名称
        row_num : int
            行号

        Returns
        -------
        Any
            返回给定的值
        """
        row: CsvRow | None = self.get_row_by_id(row_num)
        if row is None:
            return None
        idx = self.get_idx_by_header(header_name)
        return None if idx == -1 else row.get_data_by_idx(idx)

    def append_row(self, row: CsvRow) -> None:
        """
        添加数据

        Parameters
        ----------
        row : CsvRow
            要添加的 CsvRow 对象
        """
        self.data.append(row)
        self.cnt_of_row += 1

    def _initialize(self) -> None:
        header_lst = self.header.get_raw_data()
        for i, v in enumerate(header_lst):
            self.header_map[v] = i


class CsvReader:
    """
    CSV Reader 包装类

    Attributes
    ----------
    file_path : str | PathLike
        CSV 文件路径
    encoding : str
        文件编码
    config : CsvConfig
        CSV 配置

    Methods
    -------
    read() -> CsvData
        读取 CSV 文件
    get_dicts_from_csv(f_name: str | PathLike) -> Generator[Mapping[str, Any], None, None]
        获取 CSV 数据字典生成器
    get_namedtuple_from_csv(f_name: str | PathLike, model_cls: type[NamedTuple]) -> \
    Generator[type[NamedTuple], None, None]
        获取 CSV 数据命名元祖生成器
    """

    DEFAULT_ENCODING = CharsetUtil.UTF_8

    def __init__(
        self,
        file_path: str | PathLike = "",
        encoding: str = DEFAULT_ENCODING,
        config: CsvConfig | None = None,
    ) -> None:
        self.file_path: str | PathLike = file_path
        self.encoding = encoding
        self.config: CsvConfig = CsvConfig() if config is None else config

    @classmethod
    def get_dicts_from_csv(
        cls,
        f_name: str | PathLike,
    ) -> Generator[Mapping[str, Any], None, None]:
        """
        根据 CSV 文件名获取 CSV 数据字典生成器

        Parameters
        ----------
        f_name : str | PathLike
            文件描述符

        Yields
        ------
        Generator[Mapping[str, Any], None, None]
            字典生成器
        """
        reader = cls(f_name)
        csv_data = reader.read()
        for row in csv_data.data:
            yield row.to_dict(csv_data.header_map)

    @classmethod
    def get_namedtuple_from_csv(
        cls,
        f_name: str | PathLike,
        model_cls: type[NamedTuple],
    ) -> Generator[type[NamedTuple], None, None]:
        """
        根据给定的文件描述符和命名元祖获取元祖生成器

        Parameters
        ----------
        f_name : str | PathLike
            文件描述符
        model_cls : type[NamedTuple]
            命名元祖类

        Yields
        ------
        Generator[type[NamedTuple], None, None]
            命名元祖生成器
        """
        reader = cls(f_name)
        csv_data = reader.read()
        for row in csv_data.data:
            yield row.to_namedtuple(model_cls)

    def read(self) -> CsvData:
        """
        读取 CSV 文件

        Returns
        -------
        CsvData
            读取到的 CSV 数据, 包含 header 和 data
        """
        self._check_path()
        path_obj = FileUtil.get_path_object(self.file_path)
        with open(path_obj, encoding=self.encoding) as csv_file:
            reader = csv.reader(
                csv_file,
                delimiter=self.config.delimiter,
                strict=self.config.strict_mode,
                lineterminator=self.config.lineterminator,
                skipinitialspace=self.config.skip_initial_space,
                quotechar=self.config.text_qualifier,
            )
            header_line = next(reader)
            header_obj = CsvHeader(header_line)

            csv_data = CsvData(header_obj)
            for row_num, row in enumerate(reader):
                row_obj = CsvRow(row_num + 1, row, False)
                csv_data.append_row(row_obj)

            return csv_data

    def _check_path(self) -> None:
        if not FileUtil.is_exist(self.file_path):
            raise FileNotFoundError(f"file {self.file_path} not found")

        if not FileUtil.is_match_extension(self.file_path, "csv"):
            raise ValueError(f"file {self.file_path} is not a csv file")
