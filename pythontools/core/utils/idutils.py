#!/usr/bin/env python
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

from pythontools.core.constants.area_constant import AREA_INFO, PRO_DICT
from pythontools.core.constants.pattern_pool import PatternPool
from pythontools.core.constants.people_constant import Gender
from pythontools.core.convert.convertor import BasicConvertor
from pythontools.core.utils.basicutils import SequenceUtil, StringUtil
from pythontools.core.utils.datetimeutils import DatetimeUtil
from pythontools.core.utils.reutils import ReUtil
from pythontools.core.validators.datetime_validator import DatetimeValidator
from pythontools.core.validators.string_validator import StringValidator


class IDCard:
    """
    ID Card 类


    Examples
    --------
    >>> id_card = IDCard("511111199108319619")
    >>> id_card.get_age()
    32
    >>> id_card.get_gender()
    '男性'
    >>> id_card.get_province()
    '四川'
    >>> id_card.get_area()
    '四川省乐山市沙湾区'


    Attributes
    ----------
    id : str
        身份证号
    province_code : str
        省份代码
    area_code : str
        地区代码
    birthday : datetime | None
        出生日期

    Methods
    -------
    get_age() -> float
        获取年龄
    get_gender() -> str
        获取性别
    get_province() -> str
        获取登记省份信息
    get_area() -> str
        获取地区信息
    """

    def __init__(self, id: str):
        self.id: str = id
        self.province_code: str = BasicConvertor.to_str(StringUtil.sub_sequence(id, 0, 2))
        self.area_code: str = BasicConvertor.to_str(StringUtil.sub_sequence(id, 0, 6))
        self.birthday: datetime | None = IDCardUtil.get_birthday_from_id(id)

    def __repr__(self) -> str:
        return (
            f"IDCard("
            f"id='{self.id}', "
            f"province='{self.get_province()}', "
            f"area='{self.get_area()}', "
            f"birthday='{self.birthday.strftime('%Y-%m-%d')}', "  # type: ignore
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
        gender_code_str = StringUtil.sub_sequence(self.id, 16, 17)
        gender_code_int = BasicConvertor.to_int(gender_code_str)
        gender_obj = Gender.get_gender_by_code(gender_code_int)
        return gender_obj.value.sex

    def get_province(self) -> str:
        """
        获取登记省份信息

        Returns
        -------
        str
            省份信息
        """
        return PRO_DICT.get(BasicConvertor.to_str(self.province_code), "")

    def get_area(self) -> str:
        """
        获取地区信息

        Returns
        -------
        str
            地区信息
        """
        return AREA_INFO.get(self.area_code, "")


class IDCardUtil:
    """
    ID Card 工具类

    Attributes
    ----------
    CHINA_ID_MIN_LENGTH : int
        最小身份证位数
    CHINA_ID_MAX_LENGTH : int
        最长身份证位数
    AREA_LST : list[str]
        地区列表

    Methods
    -------
    convert_18_to_15(id_card: str) -> str
        将 18 位身份证转换成 15 位身份证
    convert_15_to_18(id_card: str) -> str
        将 15 位身份证转换成 18 位身份证
    generate_random_valid_card(gender: str = "男") -> IDCard
        构造随机身份证实例
    generate_random_valid_id(code_length: int = 18, gender: str = "男") -> str
        获取随机ID
    generate_random_valid_18_id(gender: str = "男") -> str
        生成 18 位随机ID
    generate_random_valid_15_id(gender: str = "男") -> str
        生成15位身份证
    is_valid_id(s: str) -> bool
        判断是否是合规的身份证 ID
    is_valid_id_18(s: str) -> bool
        是否是合规的18位身份证
    is_valid_id_15(s: str) -> bool
        检查是否是合规的15位身份证
    get_card_from_id(id_card: str) -> IDCard
        根据身份证号获取身份证实例
    get_birthday_from_id(id_card: str) -> datetime | None
        根据身份证号获取出生日期
    get_check_sum(s: str) -> str
        获取身份证校验码

    NOTES:
    -----
    - 15 位身份证：省份 (2 位) + 地级市 (2 位) + 县级市 (2 位) + 出生年 (2 位) + 出生月 (2 位) + 出生日 (2 位) + 顺序号 (3 位)
    - 18 位身份证：省份 (2 位) + 地级市 (2 位) + 县级市 (2 位) + 出生年 (4 位) + 出生月 (2 位) + 出生日 (2 位) + 顺序号 (3 位) + 校验位 (1 位)


    SEE ALSO:
    ---------
    ref: https://juejin.cn/post/6844903705662210061?utm%255C_medium=be&utm%255C_source=weixinqun


    """  # noqa: E501, W291

    # 最小身份证位数
    CHINA_ID_MIN_LENGTH: typing.Final[int] = 15
    # 最长身份证位数
    CHINA_ID_MAX_LENGTH: typing.Final[int] = 18
    AREA_LST: list[str] = list(AREA_INFO.keys())

    def __init__(self) -> None:
        raise NotImplementedError("This class is not allowed to be instantiated")

    @classmethod
    def convert_18_to_15(cls, id_card: str) -> str:
        """
        将 18 位身份证转换成 15 位身份证

        Parameters
        ----------
        id_card : str
            待转换 18 位身份证

        Returns
        -------
        str
            15 位身份证

        Raises
        ------
        ValueError
            如果给出的 18 位身份证不是有效的, 则抛出异常

        NOTES:
        -----
        - 《国务院关于实行公民身份号码制度的决定》（国发〔1999〕15号），\
            这个文件规定自1999年10月1日起在全国建立和实行公民身份号码制度，根据同年颁布的国家标准，公民身份号码升至现行的18位。
        """
        if not cls.is_valid_id_18(id_card):
            raise ValueError("id card is invalid")

        length = StringUtil.get_length(id_card)

        dt = cls.get_birthday_from_id(id_card)
        # 如果是有效身份证，则不会出现 None 的情况
        if dt >= datetime(1999, 10, 1):  # type: ignore
            raise ValueError(
                "id card is invalid, because 《国务院关于实行公民身份号码制度的决定》, It stipulates that the system of\
                    ID number shall be established and implemented throughout the country from October 1, 1999"
            )
        return StringUtil.sub_sequence(id_card, 0, 6) + StringUtil.sub_sequence(id_card, 8, length - 1)

    @classmethod
    def convert_15_to_18(cls, id_card: str) -> str:
        """
        将 15 位身份证转换成 18 位身份证

        Parameters
        ----------
        id_card : str
            待转换 15 位身份证

        Returns
        -------
        str
            18 位身份证

        Raises
        ------
        ValueError
            如果给出的 15 位身份证不是有效的, 则抛出异常
        """
        if not cls.is_valid_id_15(id_card):
            raise ValueError("id card is invalid")

        birthday = "19" + StringUtil.sub_sequence(id_card, 6, 12)
        province_code = StringUtil.sub_sequence(id_card, 0, 6)
        sequence_code = StringUtil.sub_sequence(id_card, 12)
        core_17 = f"{province_code}{birthday}{sequence_code}"
        check_sum = cls.get_check_sum(core_17)
        return f"{core_17}{check_sum}"

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
        random_id = cls.generate_random_valid_id(code_length=default_code_length, gender=gender)
        return cls.get_card_from_id(random_id)

    @classmethod
    def generate_random_valid_id(cls, *, code_length: int = 18, gender: str = "男") -> str:
        """
        获取随机ID

        Parameters
        ----------
        code_length : int, optional
            身份证ID长度, by default 18
        gender : str, optional
            指定性别, by default 男

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
            性别, by default 男
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
        area = random.choice(cls.AREA_LST)
        birthday = DatetimeUtil.get_random_date(
            start=datetime(1900, 1, 1),
            end=datetime(1999, 10, 1),
        )
        sequence_code = random.randint(10, 99)
        gender_enum_obj = Gender.get_gender_by_name(gender)
        gender_code = gender_enum_obj.value.sex_code

        return f"{area}{birthday.strftime('%y%m%d')}{sequence_code}{gender_code}"

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

        pro_code = StringUtil.sub_sequence(s, 0, 2)
        # 校验省
        if pro_code not in PRO_DICT:
            return False
        # 校验生日
        birthday = StringUtil.sub_sequence(s, 6, 14)
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

        if cls.CHINA_ID_MIN_LENGTH != StringUtil.get_length(s):
            return False

        if StringValidator.is_number(s):
            province_code = StringUtil.sub_sequence(s, 0, 2)
            # 校验省
            if province_code not in PRO_DICT:
                return False

            birthday = "19" + StringUtil.sub_sequence(s, 6, 12)

            return DatetimeValidator.is_valid_birthday(birthday)

        else:
            return False

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
        code17 = SequenceUtil.sub_sequence(s, 0, 17)
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * BasicConvertor.to_int(code17[i])
        check_digit = (12 - (check_sum % 11)) % 11
        if check_digit < 10:
            return f"{check_digit}"
        else:
            return "X"

    @classmethod
    def get_birthday_from_id(cls, s: str) -> datetime | None:
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

        if StringUtil.get_length(s) == cls.CHINA_ID_MAX_LENGTH:
            return cls.get_birthday_from_id_18(s)
        elif StringUtil.get_length(s) == cls.CHINA_ID_MIN_LENGTH:
            return cls.get_birthday_from_id_15(s)
        else:
            raise ValueError("id card length must be 15 or 18")

    @classmethod
    def get_birthday_from_id_18(cls, s: str) -> datetime | None:
        """
        从 18 位 ID 中获取对应的生日 Datetime 对象

        Parameters
        ----------
        s : str
            待提取 18 ID 字符串

        Returns
        -------
        datetime | None
            对应的生日 Datetime 对象, 如果身份证无效则返回 None
        """
        birthday = StringUtil.sub_sequence(s, 6, 14)
        return cls.get_birthday_dt_obj_from_string(birthday)

    @classmethod
    def get_birthday_from_id_15(cls, s: str) -> datetime | None:
        """
        从 15 位 ID 中获取对应的生日 Datetime 对象

        Parameters
        ----------
        s : str
            待提取 15 ID 字符串

        Returns
        -------
        datetime | None
            对应的生日 Datetime 对象, 如果身份证无效则返回 None
        """
        birthday = "19" + StringUtil.sub_sequence(s, 6, 12)
        return cls.get_birthday_dt_obj_from_string(birthday)

    @classmethod
    def get_birthday_dt_obj_from_string(cls, birthday: str) -> datetime | None:
        """
        从生日日期字符串中提取对应的 Datetime 对象

        Parameters
        ----------
        birthday : str
            生日日期字符串

        Returns
        -------
        datetime | None
            对应的 Datetime 对象, 如果字符串无效则返回 None
        """
        matched = ReUtil.is_match(PatternPool.BIRTHDAY_PATTERN, birthday)
        if not matched:
            return None

        # 采用正则匹配的方式获取生日信息
        # NOTE 如果上面进行了有效性验证, 那么必然匹配, 所以不需要再次判断
        year = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 1))
        month = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 3))
        day = BasicConvertor.to_int(ReUtil.get_matched_group_by_idx(PatternPool.BIRTHDAY_PATTERN, birthday, 5))
        return datetime(year, month, day)

    @classmethod
    def get_year_from_id(cls, s: str) -> int | None:
        """
        从 ID 信息中获取出生年

        Parameters
        ----------
        s : str
            身份证 ID

        Returns
        -------
        int | None
            如果身份证无效, 则返回 None, 否则返回出生年份
        """
        dt = cls.get_birthday_from_id(s)
        if dt is None:
            return -1
        return dt.year

    @classmethod
    def get_month_from_id(cls, s: str) -> int | None:
        """
        从 ID 信息中获取出生月

        Parameters
        ----------
        s : str
            身份证 ID

        Returns
        -------
        int | None
            如果身份证无效, 则返回 None, 否则返回出生月份
        """
        dt = cls.get_birthday_from_id(s)
        if dt is None:
            return -1
        return dt.month

    @classmethod
    def get_day_from_id(cls, s: str) -> int | None:
        """
        从 ID 信息中获取出生日

        Parameters
        ----------
        s : str
            身份证 ID

        Returns
        -------
        int | None
            如果身份证无效, 则返回 None, 否则返回出生日
        """
        dt = cls.get_birthday_from_id(s)
        if dt is None:
            return -1
        return dt.day

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
