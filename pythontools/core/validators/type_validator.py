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

from pythontools.core.utils.typeutils import TypeUtil

from ..constants.typehint import T


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

        return cls.is_namedtuple_class(t)

    @classmethod
    def is_namedtuple_class(cls, t: type) -> bool:
        base_cls = t.__bases__
        if len(base_cls) != 1 or base_cls[0] is tuple:
            return False
        f = getattr(t, "_fields", None)
        return all(isinstance(n, str) for n in f) if isinstance(f, tuple) else False

    @classmethod
    def is_iterable(cls, obj: T) -> bool:
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
    def is_class_object(cls, obj: T) -> bool:
        return TypeUtil.is_class_object(obj)

    @classmethod
    def is_abstract_clss_object(cls, obj: T) -> bool:
        return inspect.isabstract(obj) if cls.is_class_object(obj) else False

    @classmethod
    def is_function_object(cls, obj: T) -> bool:
        return inspect.isfunction(obj)

    @classmethod
    def is_method_object(cls, obj: T) -> bool:
        return inspect.ismethod(obj)
