#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   log_test.py
@Date       :   2024/09/25
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/09/25
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
from .context_test import log


class TestLog:
    def test_log(self):
        log.init_comlog("test", log.DEBUG, "./test.log", log.ROTATION, 102400000, True)

        log.debug("这是一条 debug 信息")
        log.info("这是一条 info 信息")
        log.warning("这是一条 warning 警告")
        log.error("这是一条 error 错误")
        log.critical("这是一条 critical 严重")

    def test_trace(self):
        log.init_comlog("test", log.DEBUG, "./test.log", log.ROTATION, 102400000, True)
        log.backtrace_error("ssss", 2)

    def test_log_if(self):
        log.debug_if(True, "这是一条 debug 信息")
        log.info_if(True, "这是一条 info 信息")
        log.warn_if(True, "这是一条 warning 警告")
        log.error_if(True, "这是一条 error 错误")
        log.critical_if(True, "这是一条 critical 严重")
