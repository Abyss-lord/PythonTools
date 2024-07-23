#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
@File       :   idutils.py
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

import random
import typing
from datetime import datetime

from .basic_utils import DatetimeUtil, SequenceUtil, StringUtil
from .constant import AREA_INFO, PRO_DICT, Sex
from .convertor import BasicConvertor
from .pattern_pool import PatternPool
from .validator import Validator


class IDCard(object):
    def __init__(self, id: str):
        self.id: str = id
        self.province_code: str = BasicConvertor.to_str(StringUtil.sub_lst(id, 0, 2))
        self.area_code: str = BasicConvertor.to_str(StringUtil.sub_lst(id, 0, 6))
        self.birthday: typing.Optional[datetime] = IDCardUtil.get_birthday_from_id(id)

    def __repr__(self) -> str:
        return (
            f"IDCard("
            f"id='{self.id}', "
            f"province='{self.get_province()}', "
            f"area='{self.get_area()}', "
            f"birthday='{self.birthday.strftime('%Y-%m-%d')}', "
            f"age={self.get_age()}, "
            f"sex={self.get_sex()}"
            f")"
        )

    def get_age(self) -> float:
        """
        获取年龄
        :return:
        """
        # NOTE 应该有更好的计算方式
        return DatetimeUtil.get_age(self.birthday)

    def get_sex(self) -> str:
        """
        获取性别
        :return: 男性或女性
        """
        sex_code = StringUtil.sub_lst(self.id, 16, 17)
        sex_code = BasicConvertor.to_int(sex_code)
        sex_obj = Sex.get_sex(sex_code)
        return sex_obj.value.sex

    def get_province(self) -> str:
        """
        获取省份名称
        :return: 省份名称
        """
        return PRO_DICT.get(BasicConvertor.to_str(self.province_code))

    def get_area(self) -> str:
        """
        获取地区名称
        :return: 地区名称
        """
        return AREA_INFO.get(self.area_code)


class IDCardUtil(object):
    # 最小身份证位数
    CHINA_ID_MIN_LENGTH: typing.Final[int] = 15
    # 最长身份证位数
    CHINA_ID_MAX_LENGTH: typing.Final[int] = 18
    AREA_LST: typing.List[str] = list(AREA_INFO.keys())

    @classmethod
    def generate_random_valid_card(cls, *, sex=Sex.MALE) -> IDCard:
        """
        随机产生 IDCard 实例, 默认使用18位身份证
        :param sex: 性别
        :return: IDCard 对象
        """
        default_code_length = 18
        random_id = cls.generate_random_valid_id(
            code_length=default_code_length, sex=sex
        )
        return cls.get_card_from_id(random_id)

    @classmethod
    def generate_random_valid_id(cls, *, code_length: int = 18, sex=Sex.MALE) -> str:
        """
        获取随机的身份证 ID
        :exception: ValueError
        :param code_length: 身份证长度
        :param sex: 性别
        :return: 随机的身份证ID
        """
        if code_length == cls.CHINA_ID_MAX_LENGTH:
            return cls.generate_random_valid_18_id(sex=sex)

        if code_length == cls.CHINA_ID_MIN_LENGTH:
            return cls.generate_random_valid_15_id(sex=sex)
        else:
            raise ValueError("code_length must be 15 or 18")

    @classmethod
    def generate_random_valid_18_id(cls, *, sex=Sex.MALE) -> str:
        """
        生成18位身份证
        :param sex: 性别
        :return: 18位身份证
        """
        area = random.choice(cls.AREA_LST)
        birthday = DatetimeUtil.get_random_date()
        birthday_format_str = birthday.strftime("%Y%m%d")
        sequence_code = random.randint(10, 99)
        sex_code = sex.value.sex_code
        code17 = f"{area}{birthday_format_str}{sequence_code}{sex_code}"
        checksum_code = cls.get_check_sum(code17)
        code18 = f"{code17}{checksum_code}"

        return code18

    @classmethod
    def generate_random_valid_15_id(cls, *, sex=Sex.MALE) -> str:
        """
        生成15位身份证
        :param sex: 性别
        :return: 15位身份证
        """
        raise NotImplementedError()

    @classmethod
    def is_valid_id(cls, s: str) -> bool:
        """
        判断是否是合规的身份证 ID
        :param s: 待检测 ID
        :return: 如果合规返回 True, 否则返回 False
        """
        if not StringUtil.is_string(s):
            return False
        length = len(s.strip())
        if length == 18:
            return cls.is_valid_id_18(s)
        elif length == 15:
            return cls.is_valid_id_15(s)
        else:
            return False

    @classmethod
    def is_valid_id_18(cls, s: str) -> bool:
        """
        是否是合规的18位身份证
        :param s: 待检测身份证 ID
        :return: 如果合规返回 True, 否则返回 False
        """
        if cls.CHINA_ID_MAX_LENGTH != len(s):
            return False

        pro_code = SequenceUtil.sub_lst(s, 0, 2)
        # 校验省
        if pro_code not in PRO_DICT:
            return False
        # 校验生日
        birthday = SequenceUtil.sub_lst(s, 6, 14)
        if not Validator.is_valid_birthday(birthday):
            return False
        # 校验最后一位
        check_sum = cls.get_check_sum(s)
        last_code = s[-1]
        return StringUtil.equals(check_sum, last_code)

    @classmethod
    def is_valid_id_15(cls, s: str) -> bool:
        """
        检查是否是合规的15位身份证
        :param s: 待检测身份证 ID
        :return: 如果合规返回 True, 否则返回 False
        """
        raise NotImplementedError()

    @classmethod
    def get_check_sum(cls, s: str) -> str:
        """
        根据身份证计算最后的校验位
        :param s: 身份证 ID
        :return: 校验字符
        """
        code17 = SequenceUtil.sub_lst(s, 0, 17)
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * BasicConvertor.to_int(code17[i])
        check_digit = (12 - (check_sum % 11)) % 11
        if check_digit < 10:
            return f"{check_digit}"
        else:
            return "X"

    @classmethod
    def get_birthday_from_id(cls, s: str) -> typing.Optional[datetime]:
        """
        从 ID 获取生日 datetime 对象
        :param s: id身份证号
        :return: 生日 datetime 对象
        """
        if not cls.is_valid_id(s):
            return None
        birthday = SequenceUtil.sub_lst(s, 6, 14)
        matched = PatternPool.BIRTHDAY_PATTERN.match(birthday)
        # 采用正则匹配的方式获取生日信息
        # NOTE 如果上面进行了有效性验证, 那么必然匹配, 所以不需要再次判断
        year = BasicConvertor.to_int(matched.group(1))
        month = BasicConvertor.to_int(matched.group(3))
        day = BasicConvertor.to_int(matched.group(5))
        return datetime(year, month, day)

    @classmethod
    def get_card_from_id(cls, id: str) -> IDCard:
        """
        静态方法获取对象
        :param id: 身份证 ID
        :return: IDCard 对象
        """
        return IDCard(id)
