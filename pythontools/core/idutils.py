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

from .basicutils import DatetimeUtil, SequenceUtil, StringUtil
from .constants.area_constant import AREA_INFO, PRO_DICT
from .constants.people_constant import Gender
from .convertor import BasicConvertor
from .pattern_pool import PatternPool
from .validators.datetime_validator import DatetimeValidator


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
            f"gender={self.get_gender()}"
            f")"
        )

    def get_age(self) -> float:
        """
        获取年龄

        Returns
        -------
        float
            年龄
        """
        # NOTE 应该有更好的计算方式
        return DatetimeUtil.get_age(self.birthday)

    def get_gender(self) -> str:
        """
        获取性别

        Returns
        -------
        str
            性别
        """
        gender_code = StringUtil.sub_lst(self.id, 16, 17)
        gender_code = BasicConvertor.to_int(gender_code)
        gender_obj = Gender.get_gender_by_code(gender_code)
        return gender_obj.value.sex

    def get_province(self) -> str:
        """
        获取登记省份信息

        Returns
        -------
        str
            省份信息
        """
        return PRO_DICT.get(BasicConvertor.to_str(self.province_code))

    def get_area(self) -> str:
        """
        获取地区信息

        Returns
        -------
        str
            地区信息
        """
        return AREA_INFO.get(self.area_code)


class IDCardUtil(object):
    # 最小身份证位数
    CHINA_ID_MIN_LENGTH: typing.Final[int] = 15
    # 最长身份证位数
    CHINA_ID_MAX_LENGTH: typing.Final[int] = 18
    AREA_LST: typing.List[str] = list(AREA_INFO.keys())

    @classmethod
    def generate_random_valid_card(cls, gender: str = "男") -> IDCard:
        """
        构造随机身份证实例

        Parameters
        ----------
        gender : str, optional
            性别, by default 男

        Returns
        -------
        IDCard
            身份证实例
        """
        default_code_length = 18
        gender = Gender.get_gender_by_name(gender)
        random_id = cls.generate_random_valid_id(
            code_length=default_code_length, gender=gender
        )
        return cls.get_card_from_id(random_id)

    @classmethod
    def generate_random_valid_id(
        cls, *, code_length: int = 18, gender=Gender.MALE
    ) -> str:
        """
        获取随机ID

        Parameters
        ----------
        code_length : int, optional
            身份证ID长度, by default 18
        gender : Gender, optional
            指定性别, by default Gender.MALE

        Returns
        -------
        str
            随机ID

        Raises
        ------
        ValueError
            如果指定的ID长度不是15或者18, 则抛出异常
        """
        if code_length == cls.CHINA_ID_MAX_LENGTH:
            return cls.generate_random_valid_18_id(gender=gender)

        if code_length == cls.CHINA_ID_MIN_LENGTH:
            return cls.generate_random_valid_15_id(gender=gender)
        else:
            raise ValueError("code_length must be 15 or 18")

    @classmethod
    def generate_random_valid_18_id(cls, *, gender: str = "男") -> str:
        """
        生成 18 位随机ID

        Parameters
        ----------
        gender : str, optional
            性别, by default Gender.MALE

        Returns
        -------
        str
            18 位随机ID
        """
        area = random.choice(cls.AREA_LST)
        birthday = DatetimeUtil.get_random_date()
        birthday_format_str = birthday.strftime("%Y%m%d")
        sequence_code = random.randint(10, 99)
        gender_enum_obj = Gender.get_gender_by_name(gender)
        gender_code = gender_enum_obj.value.sex_code
        code17 = f"{area}{birthday_format_str}{sequence_code}{gender_code}"
        checksum_code = cls.get_check_sum(code17)
        code18 = f"{code17}{checksum_code}"

        return code18

    @classmethod
    def generate_random_valid_15_id(cls, *, gender: str = "男") -> str:
        """
        生成15位身份证

        Parameters
        ----------
        gender : str, optional
            性别, by default "男"

        Returns
        -------
        str
            随机15位身份证
        """
        # TODO 实现15位身份证生成逻辑
        raise NotImplementedError()

    @classmethod
    def is_valid_id(cls, s: str) -> bool:
        """
        判断是否是合规的身份证 ID

        Parameters
        ----------
        s : str
            待检测身份证 ID

        Returns
        -------
        bool
            是否是合规 ID
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

        Parameters
        ----------
        s : str
            待检测18位身份证

        Returns
        -------
        bool
            是否是合规18位身份证
        """
        if cls.CHINA_ID_MAX_LENGTH != len(s):
            return False

        pro_code = SequenceUtil.sub_lst(s, 0, 2)
        # 校验省
        if pro_code not in PRO_DICT:
            return False
        # 校验生日
        birthday = SequenceUtil.sub_lst(s, 6, 14)
        if not DatetimeValidator.is_valid_birthday(birthday):
            return False
        # 校验最后一位
        check_sum = cls.get_check_sum(s)
        last_code = s[-1]
        return StringUtil.equals(check_sum, last_code)

    @classmethod
    def is_valid_id_15(cls, s: str) -> bool:
        """
        检查是否是合规的15位身份证

        Parameters
        ----------
        s : str
            待检测15位身份证

        Returns
        -------
        bool
            是否合规

        """
        # TODO 实现15位身份证校验逻辑
        raise NotImplementedError()

    @classmethod
    def get_check_sum(cls, s: str) -> str:
        """
        根据身份证计算最后的校验位

        Parameters
        ----------
        s : str
            身份证ID前n-1位

        Returns
        -------
        str
            校验位
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

        Parameters
        ----------
        s : str
            身份证ID

        Returns
        -------
        typing.Optional[datetime]
            表示生日的 datetime 对象, 如果身份证无效则返回 None
        """
        if not cls.is_valid_id(s):
            return None
        birthday = SequenceUtil.sub_lst(s, 6, 14)
        matched = PatternPool.BIRTHDAY_PATTERN.match(birthday)

        if matched is None:
            return None
        # 采用正则匹配的方式获取生日信息
        # NOTE 如果上面进行了有效性验证, 那么必然匹配, 所以不需要再次判断
        year = BasicConvertor.to_int(matched.group(1))
        month = BasicConvertor.to_int(matched.group(3))
        day = BasicConvertor.to_int(matched.group(5))
        return datetime(year, month, day)

    @classmethod
    def get_card_from_id(cls, id: str) -> IDCard:
        """
        根据身份证 ID 获取身份证对象

        Parameters
        ----------
        id : str
            身份证ID

        Returns
        -------
        IDCard
            身份证对象
        """
        return IDCard(id)
