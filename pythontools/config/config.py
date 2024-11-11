#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   config.py
@Date       :   2024/07/29
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/29
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import enum
import json
import threading
import typing
import warnings
from copy import deepcopy

from src.utils.basic_utils import BooleanUtil, StringUtil
from src.utils.file_utils import FileUtil

ConfigItemValue = int | float | str | bool


class AutoName(enum.Enum):
    """
    This is used for creating Enum classes where `auto()` is the string form
    of the corresponding enum's identifier (e.g. FOO.value results in "FOO").

    Reference: https://docs.python.org/3/howto/enum.html#using-automatic-values
    """

    def _generate_next_value_(self, _start, _count, _last_values):
        return self


class ConfigType(AutoName):
    BOOLEAN = enum.auto()
    STRING = enum.auto()
    NUMERIC = enum.auto()

    @classmethod
    def get_type_instance(cls, value: typing.Any) -> "ConfigType":
        if isinstance(value, bool):
            return cls.BOOLEAN
        elif isinstance(value, str):
            return cls.STRING
        elif isinstance(value, (int | float)):
            return cls.NUMERIC

        raise ValueError(f"Invalid config type: {value}")

    @classmethod
    def get_type_cls(cls, value: typing.Self) -> type[bool] | type[str] | type[int] | type[float]:
        if value == ConfigType.BOOLEAN:
            return bool
        elif value == ConfigType.STRING:
            return str
        elif value == ConfigType.NUMERIC:
            return float

        raise ValueError(f"Invalid config type: {value}")


class BaseConfigItem:
    __slots__ = (
        "name",
        "description",
        "value",
        "default_value",
        "item_type",
    )

    def __init__(
        self,
        *,
        name: str,
        description: str,
        value: ConfigItemValue,
        default_value: ConfigItemValue,
        item_type: ConfigType = ConfigType.STRING,
    ) -> None:
        """
        初始化函数

        Parameters
        ----------
        name : str
            配置项名称
        description : str
            配置项描述
        value : bool | str | float | int
            配置项值
        default_value : bool | str | float | int
            配置项默认值
        item_type : ConfigType, optional
            配置项类型, by default ConfigType.STRING
        """
        self.name: str = name
        self.description: str = description
        self.value: ConfigItemValue = default_value
        self.default_value = default_value
        self.item_type: ConfigType = item_type

        self.set_value(value)

    def __repr__(self):
        return f"<vscode.{self.__class__.__name__} \t name={self.name} \t description={self.description}>, \
            \t value={self.value} \t default_value={self.default_value}"

    def to_dict(self) -> dict[str, typing.Any]:
        """
        返回该配置项的字典形式

        Returns
        -------
        dict[str, typing.Any]
            配置项的字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "item_type": self.item_type.value,
        }

    def to_json(self) -> str:
        """
        返回该配置项的 JSON 格式字符串

        Returns
        -------
        str
            Json 格式字符串
        """
        return json.dumps(self.to_dict())

    def set_value(self, value: typing.Any) -> None:
        """
        设置配置项的值

        Parameters
        ----------
        value : typing.Any
            要设置的值
        """
        self.value = value

    def get_value(self) -> ConfigItemValue:
        """
        返回配置项当前值

        Returns
        -------
        ConfigItemValue
            配置项当前值
        """
        return self.value

    def get_default_value(self) -> ConfigItemValue:
        """
        返回配置项默认值

        Returns
        -------
        ConfigItemValue
            配置项默认值
        """
        return self.default_value

    def get_description(self) -> str:
        """
        返回配置项描述信息

        Returns
        -------
        str
            配置项描述信息
        """
        return self.description

    def reset(self) -> None:
        """
        重制配置项的值
        """
        self.set_value(self.default_value)


class BooleanConfigItem(BaseConfigItem):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        value: bool,
        default_value: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            value=value,
            default_value=default_value,
            item_type=ConfigType.BOOLEAN,
        )

    def set_value(self, value: typing.Any) -> None:
        if isinstance(value, str):
            val = BooleanUtil.str_to_boolean(value)
            super().set_value(val)
        elif isinstance(value, bool):
            super().set_value(value)
        else:
            raise ValueError(f"Invalid value type: {value}")


class StringConfigItem(BaseConfigItem):
    """
    字符串配置项

    """

    def __init__(self, *, name: str, description: str, value: str, default_value: str = "") -> None:
        super().__init__(
            name=name,
            description=description,
            value=value,
            default_value=default_value,
            item_type=ConfigType.STRING,
        )

    def set_value(self, value: typing.Any) -> None:
        return super().set_value(f"{value}")


class NumericConfigItem(BaseConfigItem):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        value: int | float,
        default_value: int | float = 0,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            value=value,
            default_value=default_value,
            item_type=ConfigType.NUMERIC,
        )

    def set_value(self, value: typing.Any) -> None:
        val = float(value)
        return super().set_value(val)


BASIC_CONFIG_ITEMS: list[BaseConfigItem] = [
    BooleanConfigItem(
        name="debug_enable",
        description="是否开启调试模式",
        value=False,
        default_value=False,
    ),
    StringConfigItem(
        name="test_db_prefix",
        description="测试数据库前缀",
        value="test_",
        default_value="test_",
    ),
    StringConfigItem(
        name="test_hive_dir",
        description="测试hive目录",
        value="test_hive",
        default_value="test_hive",
    ),
    BooleanConfigItem(
        name="strict_mode",
        description="是否开启严格模式",
        value=False,
        default_value=False,
    ),
    BooleanConfigItem(
        name="use_legacy_mode",
        description="SQL 解析时是否使用 LEGACY 模式",
        value=True,
        default_value=True,
    ),
    StringConfigItem(
        name="test_spark_dir",
        description="测试spark目录",
        value="test_spark",
        default_value="test_spark",
    ),
    NumericConfigItem(
        name="text_scale",
        description="文本字段的最大长度",
        value=150,
        default_value=150,
    ),
    StringConfigItem(
        name="text_fill_char",
        description="文本字段的填充字符",
        value="#",
        default_value="#",
    ),
]


class Configurations:
    """
    配置类
    """

    _LOCK = threading.Lock()

    def __init__(self, property_file_path: str | None = None) -> None:
        # 基础配置
        self.__basic_config: dict[str, BaseConfigItem] = {}
        # 用户自定义配置，仅仅以key-value形式存储
        self.__customer_config: dict[str, typing.Any] = {}
        # 配置文件，json格式
        self.__property_file_path: str | None = property_file_path
        # 1. 读取初始化配置
        self.__load_basic_config()
        # 2. 读取配置文件、合并配置项
        self.__load_config_from_file()

    def __repr__(self) -> str:
        s = [f"{repr(i)}" for i in self.__basic_config.values()]
        repr_str = "\n".join(s)
        return f"<vscode.Configurations basic_config={repr_str}>"

    def __contains__(self, name: str) -> bool:
        return name.lower() in self.__basic_config

    def keys(self) -> typing.Generator[str, typing.Any, None]:
        """
        返回所有配置项的名称

        Returns
        -------
        typing.Generator[str, typing.Any, None]
            配置项名称迭代器

        Yields
        ------
        Iterator[typing.Generator[str, typing.Any, None]]
            配置项名称迭代器
        """
        yield from self.__basic_config.keys()

    def values(self) -> typing.Generator[BaseConfigItem, typing.Any, None]:
        """
        返回所有的配置项值

        Returns
        -------
        typing.Generator[BaseConfigItem, typing.Any, None]
            配置项迭代器

        Yields
        ------
        Iterator[typing.Generator[BaseConfigItem, typing.Any, None]]
            配置项迭代器
        """
        yield from self.__basic_config.values()

    def items(self) -> typing.Generator[tuple[str, BaseConfigItem], typing.Any, None]:
        """
        返回基础配置项键值对

        Returns
        -------
        typing.Generator[tuple[str, BaseConfigItem], typing.Any, None]
            键值对迭代器

        Yields
        ------
        Iterator[typing.Generator[tuple[str, BaseConfigItem], typing.Any, None]]
            键值对迭代器
        """
        yield from self.__basic_config.items()

    def add_config(self, item_key: str, item_value: typing.Any) -> None:
        """
        添加配置项

        Parameters
        ----------
        item_key : str
            _description_
        item_value : typing.Any
            _description_
        """
        if self.is_not_basic_config(item_key):
            warnings.warn(f"{item_key} is not a customer config item")
            self.add_customer_config(item_key, item_value)
        else:
            self.set_basic_config(item_key, item_value)

    def add_customer_config(self, item_key: str, item_value: typing.Any) -> None:
        """
        添加用户自定义配置项

        Parameters
        ----------
        item_key : str
            配置项名称
        item_value : typing.Any
            配置项值
        """
        self.__customer_config[item_key] = item_value

    def set_basic_config(self, item_key: str, item_value: ConfigItemValue) -> None:
        """
        设置基础配置项的值

        Parameters
        ----------
        item_key : str
            配置项名称
        item_value : ConfigItemValue
            配置项的值
        """
        item = self.get_configItem_by_name(item_key)
        item.set_value(item_value)

    def set_customer_config(self, item_key: str, item_value: ConfigItemValue | None) -> ConfigItemValue | None:
        """
        设置用户自定义配置项的值

        Parameters
        ----------
        item_key : str
            用户配置项的名称
        item_value : ConfigItemValue | None
            要设置的值

        Returns
        -------
        ConfigItemValue | None
            如果已经设置过值则返回旧值，否则返回None
        """
        old_value = self.__customer_config.get(item_key, None)
        self.__customer_config[item_key] = item_value
        return old_value

    def get_config_value(self, item_key: str) -> ConfigItemValue | None:
        """
        获取配置项的值

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        ConfigItemValue | None
            配置项的值
        """
        if self.is_not_basic_config(item_key) and self.is_not_customer_config(item_key):
            warnings.warn(f"{item_key} is not a valid config item")
            return None
        elif self.is_basic_config(item_key):
            return self.get_basic_config_value(item_key)
        else:
            return self.get_customer_config_value(item_key)

    def get_customer_config_value(self, item_key: str) -> str | None:
        """
        获取用户自定义配置项的值

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        str | None
            配置项的值
        """
        return self.__customer_config.get(item_key, None)

    def get_basic_config_value(self, item_key: str) -> ConfigItemValue:
        """
        获取基础配置项的值

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        ConfigItemValue
            配置项的值
        """
        item = self.get_configItem_by_name(item_key)
        return item.get_value()

    def get_configItem_by_name(self, item_key: str) -> BaseConfigItem:
        """
        根据配置项名称获取配置项

        Example:
        ----------
        >>> config = Configurations()
        ... config.get_configItem_by_name("test_db_prefix")
        <vscode.StringConfigItem name=test_db_prefix, description=测试数据库前缀, value=test_, defasult=test_, type=<ConfigType.STRING: 2>>

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        BaseConfigItem
            配置项

        Raises
        ------
        KeyError
            如果配置项不存在则抛出异常
        """
        item_key = item_key.lower()
        if self.is_not_basic_config(item_key):
            raise KeyError(f"{item_key} is not a valid config item")

        return self.__basic_config[item_key]

    def get_default_value(self, item_key: str) -> ConfigItemValue:
        """
        获取给定配置项的默认值

        Example:
        ----------
        >>> config = Configurations()
        ... config.get_default_value("test_db_prefix")
        'test_'

        Parameters
        ----------
        item_key : str
            给定配置项名称

        Returns
        -------
        ConfigItemValue
            配置项的默认值

        Raises
        ------
        KeyError
            如果配置项不存在则抛出异常

        """
        item = self.get_configItem_by_name(item_key)
        return item.get_default_value()

    def get_boolean_value(self, item_key: str) -> bool:
        """
        获取给定配置项的布尔值

        Example:
        ----------
        >>> config = Configurations()
        ... config.get_boolean_value("debug_enable")
        False

        Parameters
        ----------
        item_key : str
            给定配置项名称

        Returns
        -------
        bool
            配置项的布尔值

        Raises
        ------
        KeyError
            如果配置项不存在则抛出异常
        """
        item = self.get_configItem_by_name(item_key)
        if not item.item_type == ConfigType.BOOLEAN:
            raise ValueError(f"{item_key} is not a boolean config item")
        return item.get_value()  # type: ignore

    def get_string_value(self, item_key: str) -> str:
        """
        获取给定配置项的字符串值

        Example:
        ----------
        >>> config = Configurations()
        ... config.get_string_value("test_db_prefix")
        'test_'

        Parameters
        ----------
        item_key : str
            给定配置项名称

        Returns
        -------
        str
            配置项的字符串值

        Raises
        ------
        KeyError
            如果配置项不存在则抛出异常
        """
        item = self.get_configItem_by_name(item_key)
        if item.item_type != ConfigType.STRING:
            raise ValueError(f"{item_key} is not a string config item")
        return item.get_value()  # type: ignore

    def get_numeric_value(self, item_key: str) -> float | int:
        """
        获取给定配置项的数值

        Example:
        ----------
        >>> config = Configurations()
        ... config.get_numeric_value("text_scale")
        150.0

        Parameters
        ----------
        item_key : str
            给定配置项名称

        Returns
        -------
        float
            配置项的数值

        Raises
        ------
        KeyError
            如果配置项不存在则抛出异常
        """
        item = self.get_configItem_by_name(item_key)
        if item.item_type != ConfigType.NUMERIC:
            raise ValueError(f"{item_key} is not a numeric config item")
        return item.get_value()  # type: ignore

    def reset_all_config(self) -> None:
        """
        重置所有配置项到默认值

        Example:
        ------------
        >>> config = Configurations()
        ... config.reset_all_config()
        None
        """
        for v in self.__basic_config.values():
            v.reset()

    def reset_config(self, item_key: str) -> None:
        """
        根据给定的键重置配置项到默认值

        Example:
        ----------

        >>> config = Configurations()
        ... config.reset_config("test_db_prefix")
        None

        Parameters
        ----------
        item_key : str
            给定的键

        Raises
        ------
        KeyError
            如果键不存在则抛出异常

        """
        item = self.get_configItem_by_name(item_key)
        item.reset()

    # test
    def get(self):
        return self.__customer_config

    def is_customer_config(self, item_key: str) -> bool:
        """
        判断给定的配置项是否是用户自定义配置项

        Example:
        ----------
        >>> config = Configurations()
        ... config.is_customer_config("test_db_prefix")
        False

        Parameters
        ----------
        item_key : str
            给定的配置项名称

        Returns
        -------
        bool
            是否是用户自定义配置项
        """
        return item_key.strip().lower() in self.__customer_config

    def is_not_customer_config(self, item_key: str) -> bool:
        """
        判断给定的配置项是否不是用户自定义配置项

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        bool
            如果配置项不是用户自定义配置项则返回True, 否则返回False
        """
        return not self.is_customer_config(item_key)

    def is_basic_config(self, item_key: str) -> bool:
        """
        判断给定的配置项是否是基础配置项

        Example:
        ----------
        >>> config = Configurations()
        ... config.is_basic_config("test_db_prefix")
        True

        Parameters
        ----------
        item_key : str
            给定的配置项名称

        Returns
        -------
        bool
            是否是基础配置项
        """
        return item_key.strip().lower() in self.__basic_config

    def is_not_basic_config(self, item_key: str) -> bool:
        """
        判断给定的配置项是否不是基础配置项

        Parameters
        ----------
        item_key : str
            配置项名称

        Returns
        -------
        bool
            如果配置项不是基础配置项则返回True, 否则返回False
        """
        return not self.is_basic_config(item_key)

    def __load_basic_config(self) -> None:
        Configurations._LOCK.acquire()
        for item in BASIC_CONFIG_ITEMS:
            self.__basic_config[item.name] = deepcopy(item)

        Configurations._LOCK.release()

    def __load_config_from_file(self) -> None:
        if not StringUtil.is_blank(self.__property_file_path):
            if not FileUtil.is_file(self.__property_file_path):
                warnings.warn(f"config file {self.__property_file_path} not found")
                return
            with open(self.__property_file_path) as f:  # type: ignore
                customer_configs = json.load(f)
                # TODO 展平字典
                for key, value in customer_configs.items():
                    self.add_config(key, value)


@enum.unique
class FixSql(enum.Enum):
    """
    SQL 模版, 用于生成 SQL 语句, 使用format方法进行格式化

    Example:
    ----------
    >>> FixSql.SHOW_TABLES.format("database_name")
    'SHOW TABLES database_name'
    >>> FixSql.USE_DATABASE.format("database_name")
    'USE database_name'
    """

    SHOW_TABLES = "SHOW TABLES "
    SHOW_DATABASES = "SHOW DATABASES "
    USE_DATABASE = "USE {}"
    CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {}"
