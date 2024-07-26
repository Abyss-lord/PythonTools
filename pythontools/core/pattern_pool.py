#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   pattern_pool.py
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

import re


class RegexPool(object):
    # 生日
    BIRTHDAY = "^(\\d{2,4})([/\\-.年]?)(\\d{1,2})([/\\-.月]?)(\\d{1,2})日?$"
    # 十五位身份证号表达式
    ID_NUMBER_15_REGEX = (
        r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"
    )
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_REGEX = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
    # JSON 字符串
    JSON_REGEX = r"^\s*[\[{]\s*(.*)\s*[\}\]]\s*$"
    # 单个中文汉字
    CHINESE = "[\u2e80-\u2eff\u2f00-\u2fdf\u31c0-\u31ef\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\ud840\udc00-\ud869\udedf\ud869\udf00-\ud86d\udf3f\ud86d\udf40-\ud86e\udc1f\ud86e\udc20-\ud873\udeaf\ud87e\udc00-\ud87e\ude1f]"
    CHINESES = CHINESE + "+"
    # 数字+字母+下划线
    GENERAL_STRING_PATTERN = "^\\w+$"
    # 钱币
    MONEY = "^(\\d+(?:\\.\\d+)?)$"
    # 邮编，兼容港澳台
    ZIP_CODE = "^(0[1-7]|1[0-356]|2[0-7]|3[0-6]|4[0-7]|5[0-7]|6[0-7]|7[0-5]|8[0-9]|9[0-8])\\d{4}|99907[78]$"
    # 移动电话 eg: 中国大陆： +86 180 4953 1399，2位区域码标示+11位数字 中国大陆 +86 Mainland China
    MOBILE = "(?:0|86|\\+86)?1[3-9]\\d{9}"
    # IPV4
    IPV4 = "^(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)\\.(25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)$"
    # IPV6
    IPV6 = "(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\\.){3}(25[0-5]|(2[0-4]|1?[0-9])?[0-9]))"
    # MAC 地址
    MAC_ADDRESS = "((?:[a-fA-F0-9]{1,2}[:-]){5}[a-fA-F0-9]{1,2})|0x(\\d{12}).+ETHER"
    # 中国车牌号码（兼容新能源车牌）
    CHINESE_VEHICLE_NUMBER = (
        "^(([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z](([0-9]{5}[ABCDEFGHJK])|([ABCDEFGHJK]([A-HJ-NP-Z0-9])[0-9]{4})))|"
        + "([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]\\d{3}\\d{1,3}[领])|"
        + "([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳使领]))$"
    )


class PatternPool:
    # 十五位身份证号表达式
    ID_NUMBER_15_PATTERN = re.compile(RegexPool.ID_NUMBER_15_REGEX)
    # 十八位身份证号表达式 identity_util
    ID_NUMBER_18_PATTERN = re.compile(RegexPool.ID_NUMBER_18_REGEX)
    # 生日
    BIRTHDAY_PATTERN = re.compile(RegexPool.BIRTHDAY)
    # JSON 字符串
    JSON_WRAPPER_PATTERN = re.compile(RegexPool.JSON_REGEX, re.MULTILINE | re.DOTALL)
    # 数字+字母+下划线
    GENERAL_STRING_PATTERN = re.compile(RegexPool.GENERAL_STRING_PATTERN)
    # 钱币
    MONEY = re.compile(RegexPool.MONEY)
    # 邮编，兼容港澳台
    ZIP_CODE = re.compile(RegexPool.ZIP_CODE)
    # 移动电话 eg: 中国大陆： +86 180 4953 1399，2位区域码标示+11位数字 中国大陆 +86 Mainland China
    MOBILE = re.compile(RegexPool.MOBILE)
    # IPV4
    IPV4 = re.compile(RegexPool.IPV4)
    # IPV6
    IPV6 = re.compile(RegexPool.IPV6)
    # MAC 地址
    MAC_ADDRESS = re.compile(RegexPool.MAC_ADDRESS, re.IGNORECASE)
    # 中国车牌号码（兼容新能源车牌）
    CHINESE_VEHICLE_NUMBER = re.compile(RegexPool.CHINESE_VEHICLE_NUMBER)
    # 中文
    CHINESES = re.compile(RegexPool.CHINESES)
