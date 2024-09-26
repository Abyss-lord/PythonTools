#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   log_constant.py
@Date       :   2024/09/26
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/26
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

from enum import Enum, auto


class FileHandlerType(Enum):
    """
    文件日志处理类型
    """

    ROTATION = auto()  # 按文件大小分割日志文件
    INFINITE = auto()  # 无限滚动日志文件
    TIME_ROTATION = auto()  # 按时间间隔分割日志文件
