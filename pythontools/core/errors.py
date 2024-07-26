#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   errors.py
@Date       :   2024/07/26
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/07/26
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib


class ValidationError(Exception):
    def __init__(self, pattern, s, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.pattern = pattern
        self.s = s
