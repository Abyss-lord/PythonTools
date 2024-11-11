#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   stringvalidator.py
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

import contextlib

# here put the import lib
import json
import re
import string

from pythontools.core.constants.string_constant import CharPool
from pythontools.core.utils.phoneutils import PhoneUtil
from pythontools.core.utils.typeutils import TypeUtil

from ..constants.pattern_pool import PatternPool
from ..utils.basicutils import ReUtil, StringUtil


class StringValidator:
    @classmethod
    def is_number(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        通过正则的方式判断是否只有数字组成

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            如果 raise_exception=False, 且匹配成功返回 True, 否则返回 False。
        """
        return TypeUtil.is_number(s)

    @classmethod
    def is_letter(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        返回正则方式判断字符串是否只有英文字母组成

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            如果 raise_exception=False, 且匹配成功返回 True, 否则返回 False。
        """
        return ReUtil.is_match(PatternPool.LETTER, s, raise_exception=raise_exception)

    @classmethod
    def is_json(cls, s: str) -> bool:
        """
        判断字符串是否是json字符串

        Example:
        ----------
        >>> StringValidator.is_json('{"name": "John", "age": 30, "city": "New York"}')
        True
        >>> StringValidator.is_json('{"name": "John", "age": 30, "city": "New York"')
        False
        >>> StringValidator.is_json('{"name": "John", "age": 30, "city": "New York"}')
        True

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            如果是json字符串, 则返回True, 否则返回False
        """
        if StringUtil.is_blank(s):
            return False

        if PatternPool.JSON_WRAPPER_PATTERN.match(s) is None:
            return False

        # PERF 不应该用try-except作为分支逻辑
        with contextlib.suppress(TypeError, ValueError, OverflowError):
            return isinstance(json.loads(s), dict | list)
        return False

    @classmethod
    def is_general_string(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        匹配字符串是否只由数字、字母、下划线组成

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            是否匹配

        Raises
        ------
        ValidationError
            如果raise_exception为True, 且不匹配时, 抛出ValidationError异常
        """
        return ReUtil.is_match(PatternPool.GENERAL_STRING_PATTERN, s, raise_exception=raise_exception)

    @classmethod
    def is_general_string_with_length(
        cls, s: str, min_length: int, max_length: int, *, raise_exception: bool = False
    ) -> bool:
        """
        验证是否为给定长度范围的英文字母 、数字和下划线

        Parameters
        ----------
        s : str
            待检测字符串
        min_length : int
            最小长度, 小于0则自动识别为0
        max_length : int
            最大长度, 小于0则自动识别为无限长度
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否匹配
        """
        min_length = max(min_length, 0)
        reg = "^\\w{" + str(min_length) + "," + str(max_length) + "}$"
        if max_length <= 0:
            reg = "^\\w{" + str(min_length) + ",}$"

        return ReUtil.is_match_reg(s, reg, raise_exception=raise_exception)

    @classmethod
    def is_isbn(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定的字符串是否为ISBN-10或ISBN-13

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False

        Returns
        -------
        bool
            如果是ISBN-10或ISBN-13, 则返回True, 否则返回False

        NOTES
        -----
        ISBN-10: 10位数字，由9个数字组成，最后一位是校验位。\n
        ISBN-13: 13位数字，由12个数字组成，最后一位是校验位。\n
        ref: https://zh.wikipedia.org/wiki/国际标准书号
        """
        if StringUtil.get_length(s) == 13:
            return cls.is_isbn_13(s, raise_exception=raise_exception)
        elif StringUtil.get_length(s) == 10:
            return cls.is_isbn_10(s, raise_exception=raise_exception)
        else:
            return False

    @classmethod
    def is_isbn_10(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断给定的字符串是否为ISBN-10

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False

        Returns
        -------
        bool
            如果是ISBN-10, 则返回True, 否则返回False

        Raises
        ------
        ValueError
            如果raise_exception为True, 且不匹配时, 抛出ValueError异常
        """
        s = s.replace(CharPool.DASHED, "")
        error_msg = f"ISBN-10: {s} is invalid"

        if StringUtil.get_length(s) != 10:
            return cls._raise_exception(
                False,
                error_msg,
                raise_exception=raise_exception,
                error_cls=ValueError,
            )

        with contextlib.suppress(ValueError):
            product = sum(int(digit) * (index + 1) for index, digit in enumerate(s))
            return cls._raise_exception(
                product % 11 == 0, error_msg, raise_exception=raise_exception, error_cls=ValueError
            )

        return False

    @classmethod
    def is_isbn_13(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断给定的字符串是否为ISBN-13

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False

        Returns
        -------
        bool
            如果是ISBN-13, 则返回True, 否则返回False

        Raises
        ------
        ValueError
            如果raise_exception为True, 且不匹配时, 抛出ValueError异常
        """
        s = s.replace(CharPool.DASHED, "")
        error_msg = f"ISBN-13: {s} is invalid"

        if StringUtil.get_length(s) != 13:
            return cls._raise_exception(
                False,
                error_msg,
                raise_exception=raise_exception,
                error_cls=ValueError,
            )

        with contextlib.suppress(ValueError):
            product = 0
            for index, digit in enumerate(s):
                weight = 1 if (index % 2 == 0) else 3
                product += int(digit) * weight

            return cls._raise_exception(
                product % 10 == 0, error_msg, raise_exception=raise_exception, error_cls=ValueError
            )

        return False

    @classmethod
    def is_pangram(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定的字符串是否是全字母字符串

        Parameters
        ----------
        s : str
            待检测字符串

        Returns
        -------
        bool
            如果是全字母字符串, 则返回True, 否则返回False

        NOTES
        -----
        全字母字符串: 由26个英文字母组成。\n
        https://en.wikipedia.org/wiki/Pangram
        """
        flg = set(PatternPool.SPACE.sub("", s)).issuperset(set(string.ascii_lowercase))
        return cls._raise_exception(
            flg,
            f"{s} is not a pangram",
            raise_exception=False,
            error_cls=ValueError,
        )

    @classmethod
    def is_camel_case(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定的字符串是否是驼峰命名法

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False

        Returns
        -------
        bool
            如果是驼峰命名法, 则返回True, 否则返回False

        NOTES
        -----
        驼峰命名法: 驼峰命名法是指以一个单词的第一个字母开始，后面每个单词的首字母均大写，如firstName、lastName、userName等。\n
        """  # noqa: E501
        return ReUtil.is_match(PatternPool.CAMEL_CASE, s, raise_exception=raise_exception)

    @classmethod
    def is_snake_case(cls, s: str, separator: str = "_", *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否是蛇形命名法

        Parameters
        ----------
        s : str
            待检测字符串
        separator : str, optional
            单词之间的分隔符, by default "_"

        Returns
        -------
        bool
            如果是蛇形命名法, 则返回True, 否则返回False
        """
        re_map = {
            "_": PatternPool.SNAKE_CASE_TEST,
            "-": PatternPool.SNAKE_CASE_TEST_DASH,
        }
        re_template = r"([a-z]+\d*{sign}[a-z\d{sign}]*|{sign}+[a-z\d]+[a-z\d{sign}]*)"
        r = re_map.get(
            separator,
            re.compile(re_template.format(sign=re.escape(separator)), re.IGNORECASE),
        )

        return cls._raise_exception(
            r.match(s) is not None,
            f"{s} is not a snake case string",
            raise_exception=raise_exception,
            error_cls=ValueError,
        )

    @classmethod
    def is_palindrome(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
        ignore_spaces: bool = False,
        ignore_case: bool = False,
    ) -> bool:
        """
        判断给定的字符串是否是回文字符串

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False
        ignore_spaces : bool, optional
            是否忽略空格, by default False
        ignore_case : bool, optional
            是否忽略大小写, by default False

        Returns
        -------
        bool
            如果是回文字符串, 则返回True, 否则返回False
        """
        if ignore_spaces:
            s = PatternPool.SPACE.sub("", s)

        flg = True

        string_length = StringUtil.get_length(s)
        for index in range(string_length):
            head_char = s[index]
            tail_char = s[string_length - index - 1]

            if ignore_case:
                head_char = head_char.lower()
                tail_char = tail_char.lower()

            if head_char != tail_char:
                flg = False

        return cls._raise_exception(
            flg,
            f"{s} is not a palindrome",
            raise_exception=raise_exception,
            error_cls=ValueError,
        )

    @classmethod
    def contains_html(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定的字符串是否包含html标签

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败, 是否引发异常, by default False

        Returns
        -------
        bool
            如果包含html标签, 则返回True, 否则返回False
        """
        return ReUtil.is_contains(PatternPool.HTML, s, raise_exception=raise_exception)

    @classmethod
    def is_money(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否是货币

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为货币
        """
        return ReUtil.is_match(PatternPool.MONEY, s, raise_exception=raise_exception)

    @classmethod
    def is_zip_code(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为邮政编码（中国

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为邮编
        """
        return ReUtil.is_match(PatternPool.ZIP_CODE, s, raise_exception=raise_exception)

    @classmethod
    def is_mobile(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为手机号码（中国）

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为中国手机号
        """
        return ReUtil.is_match(PatternPool.MOBILE, s, raise_exception=raise_exception)

    @classmethod
    def is_mobile_hk(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否是香港移动电话号码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否是香港移动电话号码
        """
        return PhoneUtil.is_mobile_hk(s, raise_exception=raise_exception)

    @classmethod
    def is_mobile_tw(
        cls,
        s: str,
        *,
        raise_exception: bool = False,
    ) -> bool:
        """
        判断是否是台湾移动电话号码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否是台湾移动电话号码
        """
        return PhoneUtil.is_mobile_tw(s, raise_exception=raise_exception)

    @classmethod
    def is_mobile_mo(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否是澳门移动手机电话号码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否是澳门移动电话号码
        """
        return PhoneUtil.is_mobile_mo(
            s,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_tel(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为电话号码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为电话号码
        """
        return PhoneUtil.is_tel(
            s,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_tel_400800(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        返回是否为400-800电话号码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为400-800电话号码
        """
        return PhoneUtil.is_tel_400800(
            s,
            raise_exception=raise_exception,
        )

    @classmethod
    def is_email(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为邮箱

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为邮箱
        """
        return ReUtil.is_match(PatternPool.EMAIL, s, raise_exception=raise_exception)

    @classmethod
    def is_ipv4(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为ipv4地址

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为ipv4地址
        """
        return ReUtil.is_match(PatternPool.IPV4, s, raise_exception=raise_exception)

    @classmethod
    def is_ipv6(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为IPV6地址

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为IPV6地址
        """
        return ReUtil.is_match(PatternPool.IPV6, s, raise_exception=raise_exception)

    @classmethod
    def is_mac_address(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为MAC地址

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为MAC地址
        """
        return ReUtil.is_match(PatternPool.MAC_ADDRESS, s, raise_exception=raise_exception)

    @classmethod
    def is_chinese_vehicle_number(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为中国车牌号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为中国车牌号
        """
        return ReUtil.is_match(PatternPool.CHINESE_VEHICLE_NUMBER, s, raise_exception=raise_exception)

    @classmethod
    def is_chinese(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为中文

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为中文
        """
        return ReUtil.is_match(PatternPool.CHINESE, s, raise_exception=raise_exception)

    @classmethod
    def is_general_with_chinese(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为中文字、英文字母、数字和下划线

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为中文字、英文字母、数字和下划线
        """
        return ReUtil.is_match(PatternPool.GENERAL_WITH_CHINESE, s, raise_exception=raise_exception)

    @classmethod
    def is_hex(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为Hex(16进制)字符串

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为Hex(16进制)字符串
        """
        return ReUtil.is_match(PatternPool.HEX, s, raise_exception=raise_exception) or ReUtil.is_match(
            PatternPool.HEX_WITH_PREFIX, s, raise_exception=raise_exception
        )

    @classmethod
    def is_credit_code(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        是否是有效的统一社会信用代码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否是有效的统一社会信用代码
        """
        return ReUtil.is_match(PatternPool.CHINESE_CREDIT_CODE, s, raise_exception=raise_exception)

    @classmethod
    def is_car_vin(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为车架号；别名：行驶证编号 车辆识别代号 车辆识别码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为车架号；别名：行驶证编号 车辆识别代号 车辆识别码
        """
        return ReUtil.is_match(PatternPool.CAR_VIN, s, raise_exception=raise_exception)

    @classmethod
    def is_chinese_driving_licence(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否是中国驾驶证

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否是中国驾驶证
        """
        return ReUtil.is_match(PatternPool.CHINESE_CAR_DRIVING_LICENCE, s, raise_exception=raise_exception)

    @classmethod
    def is_tencent_code(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        验证是否为腾讯QQ号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为腾讯QQ号
        """
        return ReUtil.is_match(PatternPool.TECENT_CODE, s, raise_exception=raise_exception)

    @classmethod
    def is_password(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为密码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            是否为密码
        """
        return ReUtil.is_match(PatternPool.PASSWORD, s, raise_exception=raise_exception)

    @classmethod
    def is_blank_line(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为空行

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为空行
        """
        return ReUtil.is_match(PatternPool.BLANK_LINE, s, raise_exception=raise_exception)

    @classmethod
    def is_wechat_account(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为微信号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为微信号
        """
        return ReUtil.is_match(PatternPool.WECHAT, s, raise_exception=raise_exception)

    @classmethod
    def is_train_number(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为火车车次号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为火车车次号
        """
        return ReUtil.is_match(PatternPool.TRAIN_NUMBER, s, raise_exception=raise_exception)

    @classmethod
    def is_time_in_24_hour_format(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为24小时制时间

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为24小时制时间
        """
        return ReUtil.is_match(PatternPool.TIME_IN_24_HOUR, s, raise_exception=raise_exception)

    @classmethod
    def is_time_in_12_hour_format(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为12小时制时间

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为12小时制时间
        """
        return ReUtil.is_match(PatternPool.TIME_IN_12_HOUR, s, raise_exception=raise_exception)

    @classmethod
    def is_chinese_province_name(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为中文省份名称

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为中文省份名称
        """
        return ReUtil.is_match(PatternPool.CHINESE_PROVINCE, s, raise_exception=raise_exception)

    @classmethod
    def is_linux_file_path(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为linux文件路径

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为linux文件路径
        """
        return ReUtil.is_match(PatternPool.LINUX_FILE_PATH, s, raise_exception=raise_exception)

    @classmethod
    def is_windows_file_path(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为windows文件路径

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为windows文件路径
        """
        return ReUtil.is_match(PatternPool.WINDOWS_FILE_PATH, s, raise_exception=raise_exception)

    @classmethod
    def is_hk_id(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为香港身份证号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为香港身份证号
        """
        return ReUtil.is_match(PatternPool.ID_NUMBER_HK, s, raise_exception=raise_exception)

    @classmethod
    def is_mo_id(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否为澳门身份证号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为澳门身份证号
        """
        return ReUtil.is_match(PatternPool.ID_NUMBER_MO, s, raise_exception=raise_exception)

    @classmethod
    def is_tw_id(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断是否是台湾身份证号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为台湾身份证
        """
        return ReUtil.is_match(PatternPool.ID_NUMBER_TW, s, raise_exception=raise_exception)

    @classmethod
    def has_no_letter(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否不包含英文字母

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串如果包含英文字母返回False，否则返回True
        """
        return ReUtil.is_match(PatternPool.HAS_NO_LETTER, s, raise_exception=raise_exception)

    @classmethod
    def is_java_class_path(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为java类路径

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为java类路径
        """
        return ReUtil.is_match(PatternPool.JAVA_CLASS_PATH, s, raise_exception=raise_exception)

    @classmethod
    def is_chinese_soldier_id(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否是军官证号、士兵证号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否是军官证号、士兵证号
        """
        return ReUtil.is_match(PatternPool.CHINESE_SOLDIER_ID, s, raise_exception=raise_exception)

    @classmethod
    def is_non_positive_integer(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为非正整数

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为非正整数
        """
        return ReUtil.is_match(PatternPool.NON_POSITIVE_INTEGER, s, raise_exception=raise_exception)

    @classmethod
    def is_non_negative_integer(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为非负整数

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为非负整数
        """
        return ReUtil.is_match(PatternPool.NON_NEGATIVE_INTEGER, s, raise_exception=raise_exception)

    @classmethod
    def is_non_positive_float(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为非正浮点数

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为非正浮点数
        """
        return ReUtil.is_match(PatternPool.NON_POSITIVE_FLOAT, s, raise_exception=raise_exception)

    @classmethod
    def is_non_negative_float(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为非负浮点数

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为非负浮点数
        """
        return ReUtil.is_match(PatternPool.NON_NEGATIVE_FLOAT, s, raise_exception=raise_exception)

    @classmethod
    def is_imei(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为IMEI号

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为IMEI号
        """
        return ReUtil.is_match(PatternPool.IMEI, s, raise_exception=raise_exception)

    @classmethod
    def is_thunder_link(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为迅雷链接

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为迅雷链接
        """
        return ReUtil.is_match(PatternPool.THUNDER_LINK, s, raise_exception=raise_exception)

    @classmethod
    def is_magnet_link(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为磁力链接

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为磁力链接
        """
        return ReUtil.is_match(PatternPool.MAGNET_LINK, s, raise_exception=raise_exception)

    @classmethod
    def is_a_stock(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定字符串是否为A股代码

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            给定字符串是否为A股代码
        """
        return ReUtil.is_match(PatternPool.A_STOCK, s, raise_exception=raise_exception)

    @classmethod
    def is_url(cls, s: str, *, raise_exception: bool = False) -> bool:
        """
        判断给定的字符串是否是URL地址

        Parameters
        ----------
        s : str
            待检测字符串
        raise_exception : bool, optional
            如果匹配失败是否引发异常, by default False

        Returns
        -------
        bool
            如果给定的字符串是URL地址，返回True，否则返回False
        """
        return ReUtil.is_match(PatternPool.URL, s, raise_exception=raise_exception)

    @classmethod
    def _raise_exception(
        cls,
        value: bool,
        message: str,
        *,
        raise_exception: bool,
        error_cls: type[Exception] = ValueError,
    ) -> bool:
        if not raise_exception:
            return value
        else:
            raise error_cls(message)
