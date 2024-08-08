#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   typeutils.py
@Date       :   2024/08/06
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/06
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import inspect
from collections.abc import Callable, Mapping
from typing import Any

from .basicutils import StringUtil
from .constants.type_constant import FunctionType
from .decorator import UnCkeckFucntion
from .validators.type_validator import TypeValidator

WARNING_ENABLED = True


class TypeUtil:
    @classmethod
    def get_class_name(cls, obj) -> str:
        """
        获取待检测对象的类名

        Parameters
        ----------
        obj : _type_
            待检测对象

        Returns
        -------
        str
            对象的类名
        """
        func_module = "Unknown" if (module := inspect.getmodule(obj)) is None else module.__name__

        return func_module

    @classmethod
    def get_class_mro(cls, obj) -> list[str]:
        """
        获取待检测对象的原始类列表

        Parameters
        ----------
        obj : _type_
            待检测对象

        Returns
        -------
        List[str]
            对象的原始类列表
        """
        if TypeValidator.is_clss_object(obj):
            mro = inspect.getmro(obj)
            return [name for c in mro if (name := c.__name__) != "object"]
        else:
            mro = inspect.getmro(obj.__class__)
            return [name for c in mro if (name := c.__name__) != "object"]

    @classmethod
    def get_function_info(cls, func: Callable[[Any], Any], *, show_detail: bool = False) -> Mapping[str, Any]:
        """
        获取一个函数的基本信息，包括函数名、类型、模块、文件路径、签名、参数信息（可选）。

        Parameters
        ----------
        func : Callable[[Any], Any]
            待检测函数
        show_detail : bool, optional
            是否显示细节, by default False

        Returns
        -------
        Mapping[str, Any]
            函数基本信息
        """
        # 函数基本信息
        func_name = func.__name__
        func_module = "Unknown" if (module := inspect.getmodule(func)) is None else module.__name__
        func_type_desc = cls.get_function_type_description(func)
        file_path = inspect.getfile(func)
        sig = inspect.signature(func)

        func_info_dict = dict(
            func_name=func_name,
            func_type=func_type_desc,
            func_module=func_module,
            file_path=file_path,
            signature=str(sig),
        )
        # 函数详细信息
        if show_detail:
            arguments_dict: Mapping[str, Mapping[str, str]] = {}
            for i, (arg_name, arg_info) in enumerate(sig.parameters.items()):
                arg_type = arg_info.kind.description
                arg_default = (
                    "UNDEFINED" if (default_value := arg_info.default) is inspect.Parameter.empty else default_value
                )
                arg_annotation = (
                    "UNDEFINED"
                    if (annotation := arg_info.annotation) is inspect.Parameter.empty
                    else annotation.__name__
                )

                argument_title = f"arg_{i + 1}"
                sub_dict: Mapping[str, str] = dict(
                    arg_name=arg_name,
                    arg_type=arg_type,
                    arg_default=arg_default,
                    arg_annotation=arg_annotation,
                )

                arguments_dict[argument_title] = sub_dict

                func_info_dict.update(arguments_dict)

        return func_info_dict

    @classmethod
    @UnCkeckFucntion(WARNING_ENABLED)
    def get_function_type_description(cls, func) -> str:
        """
        获取函数的类型描述。

        Parameters
        ----------
        func : _type_
            待检测函数

        Returns
        -------
        str
            函数的类型描述
        """
        if inspect.iscoroutinefunction(func):
            return FunctionType.COROUTINE_METHOD.value.description
        elif inspect.isgeneratorfunction(func):
            return FunctionType.GENERATOR_METHOD.value.description
        elif inspect.isbuiltin(func):
            return FunctionType.BUILT_IN_METHOD.value.description
        elif inspect.ismethod(func):
            return FunctionType.NORMAL_FUNCTION.value.description
        elif inspect.isfunction(func):
            return FunctionType.UNBIND_METHOD.value.description
        elif inspect.ismethod(func):
            return FunctionType.NORMAL_FUNCTION.value.description

        return FunctionType.UNKNOWN_METHOD.value.description

    @classmethod
    @UnCkeckFucntion(WARNING_ENABLED)
    def show_function_info(cls, func: Callable[[Any], Any], show_detail: bool = False) -> None:
        """
        显示一个函数的基本信息，包括函数名、类型、模块、文件路径、签名、参数信息（可选）。

        Parameters
        ----------
        func : Callable[[Any], Any]
            待检测方法
        show_detail : bool, optional
            是否显示细节, by default False

        Returns
        -------
        None
        """
        func_info_dict = cls.get_function_info(func, show_detail=show_detail)
        box_content = StringUtil.generate_box_string_from_dict(func_info_dict, title="FUNCTION INFO")
        print("\n" + box_content)

        return None
