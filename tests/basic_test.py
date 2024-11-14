#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_basic.py
@Date       :   2024/07/23
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/23
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import inspect

from .context_test import (
    BasicValidator,
    BooleanUtil,
    DatetimeUtil,
    DatetimeValidator,
    DesensitizedUtil,
    EnvUtil,
    FileUtil,
    IDCard,
    IDCardUtil,
    NumberUtil,
    PhoneUtil,
    RadixUtil,
    RandomUtil,
    ReUtil,
    StringUtil,
    StringValidator,
    TypeUtil,
    TypeValidator,
)

BooleanUtil
StringUtil
DatetimeUtil
DesensitizedUtil
IDCardUtil
IDCard
NumberUtil
EnvUtil
PhoneUtil
RadixUtil
RandomUtil
ReUtil
TypeUtil
BasicValidator
DatetimeValidator
StringValidator
TypeValidator
FileUtil


class TestBasic:
    def test_get_cls_info(self):
        clss = FileUtil
        print()
        self.get_cls_methods(clss)
        print()
        self.get_cls_attributes(clss)
        print()
        self.get_cls_instance_attributes(clss)

    def get_cls_methods(self, clss):
        funcs = inspect.getmembers(clss, predicate=inspect.ismethod)
        for name, func in funcs:
            if name.startswith("_"):
                continue
            res = self.format_signature(name, func)

            print(res)

    def format_signature(self, name, func):
        sig: inspect.Signature = inspect.signature(func)

        if sig.return_annotation is inspect._empty:
            return_type = "None"
        else:
            return_type = (
                sig.return_annotation.__name__
                if isinstance(sig.return_annotation, type)
                else str(sig.return_annotation)
            )

        param_strings = [f"{param}" for _, param in sig.parameters.items()]
        return f"+ {name}(" + ", ".join(param_strings) + ")" + ": " + return_type

    def get_cls_attributes(self, clss):
        attributes = [
            f"+ {name}:  {value.__class__.__name__}"
            for name, value in inspect.getmembers(clss)
            if not inspect.ismethod(value) and not name.startswith("__")
        ]

        if not attributes:
            print("No attributes found.")

        for attr in attributes:
            print(attr)

    def get_cls_instance_attributes(self, clss):
        instance_attributes = [
            f"+ {name}:  {value.__class__.__name__}"
            for name, value in inspect.getmembers(clss, predicate=inspect.ismemberdescriptor)
            if name.startswith("__")
        ]
        if not instance_attributes:
            print("No instance attributes found.")

        for attr in instance_attributes:
            print(attr)


def test_basic():
    print("中文".isalpha())


class A:
    def val(self):
        return 1


def test_get_current_year(mocker):
    mock_utcnow = mocker.patch("tests.basic_test.A.val")
    mock_utcnow.return_value = 7

    # 运行测试并检查结果
    assert get_current_year() == 7


def get_current_year():
    """获取当前年份"""
    return A().val()
