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
    CHINESE = "[\u4e00-\u9fa5]"
    CHINESES = (
        "[\u2e80-\u2eff\u2f00-\u2fdf\u31c0-\u31ef\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
        "\ud840\udc00-\ud869\udedf\ud869\udf00-\ud86d\udf3f\ud86d\udf40-\ud86e\udc1f\ud86e\udc20-\ud873\udeaf\ud87e\udc00-\ud87e\ude1f]+"
    )
    # 数字+字母+下划线
    GENERAL_STRING_PATTERN = "^\\w+$"
    # 钱币
    MONEY = "^(\\d+(?:\\.\\d+)?)$"
    # 邮编，兼容港澳台
    ZIP_CODE = "^(0[1-7]|1[0-356]|2[0-7]|3[0-6]|4[0-7]|5[0-7]|6[0-7]|7[0-5]|8[0-9]|9[0-8])\\d{4}|99907[78]$"
    # 移动电话 eg: 中国大陆： +86 180 4953 1399，2位区域码标示+11位数字 中国大陆 +86 Mainland China
    MOBILE = "(?:0|86|\\+86)?1[3-9]\\d{9}"
    # 香港电话, +852 5100 4810， 三位区域码+10位数字, 中国香港手机号码8位数
    MOBILE_HK = "(?:0|852|\\+852)?\\d{8}"
    # 台湾电话，+886 09 60 000000， 三位区域码+号码以数字09开头 + 8位数字, 中国台湾手机号码10位数 中国台湾 +886 Taiwan 国际域名缩写：TW
    MOBILE_TW = "(?:0|886|\\+886)?(?:|-)09\\d{8}"
    # 澳门电话，+853 68 00000，三位区域码 +号码以数字6开头 + 7位数字, 中国澳门手机号码8位数 中国澳门 +853 Macao 国际域名缩写：MO
    MOBILE_MO = "(?:0|853|\\+853)?(?:|-)6\\d{7}"
    # 中国座机电话号码
    TEL = "(010|02\\d|0[3-9]\\d{2})-?(\\d{6,8})"
    # 座机400-800
    TEL_400_800 = "0\\d{2,3}[\\- ]?[1-9]\\d{6,7}|[48]00[\\- ]?[1-9]\\d{2}[\\- ]?\\d{4}"
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
    # 中文+英文字母+数字+下划线
    GENERAL_WITH_CHINESE = "^[\u4e00-\u9fff\\w]+$"
    # HEX
    HEX = "^[a-fA-F0-9]+$"
    HEX_WITH_PREFIX = "^0x[0-9A-Fa-f]+$"
    #   统一社会信用代码
    #   第一部分：登记管理部门代码1位 (数字或大写英文字母)
    #   第二部分：机构类别代码1位 (数字或大写英文字母)
    #   第三部分：登记管理机关行政区划码6位 (数字)
    #   第四部分：主体标识码（组织机构代码）9位 (数字或大写英文字母)
    #   第五部分：校验码1位 (数字或大写英文字母)
    CHINESE_CREDIT_CODE = "^[0-9A-HJ-NPQRTUWXY]{2}\\d{6}[0-9A-HJ-NPQRTUWXY]{10}$"
    # 车架号 别名：车辆识别代号 车辆识别码 eg:LDC613P23A1305189 eg:LSJA24U62JG269225 十七位码、车架号 车辆的唯一标示
    CAR_VIN = "^[A-HJ-NPR-Z0-9]{8}[0-9X][A-HJ-NPR-Z0-9]{2}\\d{6}$"
    # 驾驶证 别名：驾驶证档案编号、行驶证编号 eg:430101758218 12位数字字符串 仅限：中国驾驶证档案编号
    CHINESE_CAR_DRIVING_LICENCE = "^[0-9]{12}$"
    # 邮箱
    EMAIL = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)])"
    # 浮点数
    FLOAT_NUM = "^(-?\d+)(\.\d+)?$"
    # 正浮点数
    POSITIVE_FLOAT = "^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$"
    # 负浮点数
    NEGATIVE_FLOAT = "^-([1-9]\d*\.\d*|0\.\d*[1-9]\d*)$"
    # 整数
    INTEGER = "^-?\d+$"
    # 正整数
    POSITIVE_INTEGER = r"^-[1-9]\d*|0$"
    # 负整数
    NEGATIVE_INTEGER = r"^-[1-9]\d*|0$"
    # 腾讯QQ
    TECENT_CODE = r"[1-9][0-9]{4,}"
    # 强密码，必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-12之间
    STRONG_PASSWORD = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,12}$"
    # 密码， 以字母开头，长度在6~18之间，只能包含字母、数字和下划线
    PASSWORD = r"^[a-zA-Z]\w{5,17}$"
    # 空行
    BLANK_LINE = r"\n\s*\r"


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
    # 香港移动电话
    MOBILE_HK = re.compile(RegexPool.MOBILE_HK)
    # 台湾移动电话
    MOBILE_TW = re.compile(RegexPool.MOBILE_TW)
    # 澳门移动电话
    MOBILE_MO = re.compile(RegexPool.MOBILE_MO)
    # 中国座机
    TEL = re.compile(RegexPool.TEL)
    # 座机400_800
    TEL_400_800 = re.compile(RegexPool.TEL_400_800)
    # IPV4
    IPV4 = re.compile(RegexPool.IPV4)
    # IPV6
    IPV6 = re.compile(RegexPool.IPV6)
    # MAC 地址
    MAC_ADDRESS = re.compile(RegexPool.MAC_ADDRESS, re.IGNORECASE)
    # 中国车牌号码（兼容新能源车牌）
    CHINESE_VEHICLE_NUMBER = re.compile(RegexPool.CHINESE_VEHICLE_NUMBER)
    # 中文
    CHINESE = re.compile(RegexPool.CHINESE)
    # CHINESES = re.compile(RegexPool.CHINESES)
    # 中文+英文字母+数字+下划线
    GENERAL_WITH_CHINESE = re.compile(RegexPool.GENERAL_WITH_CHINESE)
    # HEX
    HEX = re.compile(RegexPool.HEX)
    # 带有前缀
    HEX_WITH_PREFIX = re.compile(RegexPool.HEX_WITH_PREFIX)
    # 统一社会信用代码
    CHINESE_CREDIT_CODE = re.compile(RegexPool.CHINESE_CREDIT_CODE)
    # 车架号 别名：车辆识别代号 车辆识别码 eg:LDC613P23A1305189 eg:LSJA24U62JG269225 十七位码、车架号 车辆的唯一标示
    CAR_VIN = re.compile(RegexPool.CAR_VIN)
    # 驾驶证 别名：驾驶证档案编号、行驶证编号 eg:430101758218 12位数字字符串 仅限：中国驾驶证档案编号
    CHINESE_CAR_DRIVING_LICENCE = re.compile(RegexPool.CHINESE_CAR_DRIVING_LICENCE)
    # 邮箱
    EMAIL = re.compile(RegexPool.EMAIL, re.IGNORECASE)
    # 浮点数
    FLOAT_NUM = re.compile(RegexPool.FLOAT_NUM)
    # 正浮点数
    POSITIVE_FLOAT = re.compile(RegexPool.POSITIVE_FLOAT)
    # 负浮点数
    NEGATIVE_FLOAT = re.compile(RegexPool.NEGATIVE_FLOAT)
    # 整数
    INTEGER = re.compile(RegexPool.INTEGER)
    # 正整数
    POSITIVE_INTEGER = re.compile(RegexPool.POSITIVE_INTEGER)
    # 负整数
    NEGATIVE_INTEGER = re.compile(RegexPool.NEGATIVE_INTEGER)
    # 腾讯qq
    TECENT_CODE = re.compile(RegexPool.TECENT_CODE)
    # 强密码，必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-12之间
    STRONG_PASSWORD = re.compile(RegexPool.STRONG_PASSWORD)
    # 密码
    PASSWORD = re.compile(RegexPool.PASSWORD)
    # 空行
    BLANK_LINE = re.compile(RegexPool.BLANK_LINE)
