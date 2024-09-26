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

import json

import allure

from .context_test import log


@allure.feature("日志模块")
@allure.description("自定义日志模块，支持日志级别、文件大小、文件数量、是否打印到控制台等功能")
class TestLog:
    @allure.title("测试日志模块日志打印功能")
    def test_log(self):
        log.init_comlog("test", is_print_console=True)

        log.debug("这是一条 debug 信息")
        log.info("这是一条 info 信息")
        log.warning("这是一条 warning 警告")
        log.error("这是一条 error 错误")
        log.critical("这是一条 critical 严重")

    @allure.title("测试打印结构化日志功能")
    def test_log_structure_mst(self):
        log.init_comlog("test", is_print_console=True)
        log.info(
            json.dumps(
                {
                    "action": "User login",
                    "username": "user123",
                    "ip_address": "123.123.123.123",
                    "status": "success",
                }
            )
        )
