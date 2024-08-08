#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   type_validator.py
@Date       :   2024/08/05
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/05
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import inspect

from ..typehint import T


class TypeValidator:
    @classmethod
    def is_namedtuple_instance(cls, instance: T) -> bool:
        """
        返回是否是 namedtuple 实例

        Parameters
        ----------
        instance : T
            待检测实例

        Returns
        -------
        bool
            是否是 namedtuple 实例
        """
        t = type(instance)
        base_cls = t.__bases__
        if len(base_cls) != 1 or base_cls[0] is tuple:
            return False
        f = getattr(t, "_fields", None)
        if not isinstance(f, tuple):
            return False
        return all(isinstance(n, str) for n in f)

    @classmethod
    def is_iterable(obj: T) -> bool:
        try:
            iter(obj)
        except TypeError:
            return False
        else:
            return True

    @classmethod
    def is_module_object(cls, obj: T) -> bool:
        return inspect.ismodule(obj)

    @classmethod
    def is_clss_object(cls, obj: T) -> bool:
        return inspect.isclass(obj)

    @classmethod
    def is_abstract_clss_object(cls, obj: T) -> bool:
        if not cls.is_clss_object(obj):
            return False
        return inspect.isabstract(obj)

    @classmethod
    def is_function_object(cls, obj: T) -> bool:
        return inspect.isfunction(obj)

    @classmethod
    def is_method_object(cls, obj: T) -> bool:
        return inspect.ismethod(obj)
