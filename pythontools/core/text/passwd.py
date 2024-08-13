#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   passwd.py
@Date       :   2024/08/09
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/09
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import string

from ..constants.string_constant import PasswdStrength
from ..utils.basicutils import SequenceUtil, StringUtil
from ..validators.datetime_validator import DatetimeValidator


class PasswdStrengthUtil:
    """
    该工具类用于检测密码强度

    Attributes
    ----------
    SIMPLE_PWD : set
        弱密码库

    Methods
    -------
    check(cls, passwd: str) -> int
        根据密码返回强度得分
    get_level(cls, score: int) -> PasswdStrength
        根据得分返回密码强度等级

    NOTES:
    ------
    ref: https://github.com/venshine/CheckPasswordStrength
    """

    # 弱密码库
    SIMPLE_PWD = set(
        [
            "password",
            "abc123",
            "iloveyou",
            "adobe123",
            "123123",
            "sunshine",
            "1314520",
            "a1b2c3",
            "123qwe",
            "aaa111",
            "qweasd",
            "admin",
            "passwd",
        ]
    )

    @classmethod
    def get_strength_score(cls, passwd: str) -> int:
        """
        根据密码返回强度得分

        Parameters
        ----------
        passwd : str
            待检测密码

        Returns
        -------
        int
            强度得分

        Raises
        ------
        ValueError
            如果密码为空则抛出该异常

        NOTES:
        ------
        密码强度评分标准
        加分项：
        - 密码中如果有数字, 则加1分
        - 密码中如果有小写字母, 则加1分
        - 密码长度大于4, 且密码中有大写字母, 则加1分
        - 密码长度大于6, 且密码中有其他字符, 则加1分
        - 密码长度大于12, 则加1分
        - 密码长度大于16, 则加1分
        - 密码中其他字符数量大于等于3, 则加1分
        - 密码中其他字符数量大于等于6, 则加1分
        - 密码长度大于10且各种字符数量都大于等于2, 则加1分
        - 密码长度大于4+数字、小写字母数量大于1, 则加1分
        - 任意两种字符数量大于1, 则加1分
        - 密码长度大于6+数字、小写字母、大写字母数量大于1, 则加1分
        - 任意三类字符数量大于1, 则加1分
        - 密码长度大于8, 且所有种类字符数量大于1, 则加1分
        - 密码长度大于6且任意两种字符数量大于3, 则加1分
        - 密码长度大于8且任意三类字符数量大于2, 则加1分
        - 密码长度大于10且所有种类字符数量大于2, 则加1分

        减分项：
        - 连续小写或者大写字母, 则减1分
        - 键盘连续字符, 则减1分
        - 数字连续字符, 则减1分
        - 只有一种类型的字符, 则减1分
        - 如果密码能够切分成两半前后两半密码相等, 则减1分
        - 如果密码能够切分成3组, 且3组相等, 则减1分
        - 如果密码是一个日期, 则减1分
        - 如果密码和简单密码库匹配, 则判定为弱密码
        - 根据密码长度逐级减分, 长度小于3为-100分, 长度小于4为-1分, 长度小于6为-1分
        - 如果密码的所有字符相等, 则判定为弱密码
        """
        if StringUtil.is_all_blank(passwd):
            raise ValueError("密码不能为空")
        length = StringUtil.get_length(passwd)
        level_point = 0
        type_dict = StringUtil.count_letter_by_type(passwd)

        # 加分项
        # 1. 根据各类数量加分
        if type_dict["digit"] > 0:
            level_point += 1
        if type_dict["lower"] > 0:
            level_point += 1

        if length > 4 and type_dict["upper"] > 0:
            level_point += 1
        if length > 6 and type_dict["other"] > 0:
            level_point += 1

        # 2. 根据长度加分
        if length > 12:
            level_point += 1
            if length > 16:
                level_point += 1

        # 3. 根据other类型的数量加分
        if type_dict["other"] >= 3:
            level_point += 1

        if type_dict["other"] >= 6:
            level_point += 1

        # 4. 根据组合加分
        if (
            length > 10
            and type_dict["digit"] >= 2
            and type_dict["lower"] >= 2
            and type_dict["upper"] >= 2
            and type_dict["other"] >= 2
        ):
            level_point += 1

        # 5. 组合加分, 长度大于4
        if (
            (length > 4 and type_dict["digit"] >= 1 and type_dict["lower"] >= 1)
            or (type_dict["digit"] >= 1 and type_dict["upper"] >= 1)
            or (type_dict["digit"] >= 1 and type_dict["other"] >= 1)
            or (type_dict["lower"] >= 1 and type_dict["other"] >= 1)
            or (type_dict["lower"] >= 1 and type_dict["upper"] >= 1)
            or (type_dict["upper"] >= 1 and type_dict["other"] >= 1)
        ):
            level_point += 1

        # 6. 组合加分, 长度大于6
        if (
            (length > 6 and type_dict["digit"] >= 1 and type_dict["lower"] >= 1 and type_dict["upper"] >= 1)
            or (type_dict["digit"] >= 1 and type_dict["lower"] >= 1 and type_dict["other"] >= 1)
            or (type_dict["digit"] >= 1 and type_dict["upper"] >= 1 and type_dict["other"] >= 1)
            or (type_dict["lower"] >= 1 and type_dict["upper"] >= 1 and type_dict["other"] >= 1)
        ):
            level_point += 1

        # 7. 组合加分, 长度大于8
        if (
            length > 8
            and type_dict["digit"] >= 1
            and type_dict["lower"] >= 1
            and type_dict["upper"] >= 1
            and type_dict["other"] >= 1
        ):
            level_point += 1

        # 8. 组合加分, 长度大于6
        if (
            (length > 6 and type_dict["digit"] >= 3 and type_dict["lower"] >= 3)
            or (type_dict["digit"] >= 3 and type_dict["upper"] >= 3)
            or (type_dict["digit"] >= 3 and type_dict["other"] >= 2)
            or (type_dict["lower"] >= 3 and type_dict["other"] >= 2)
            or (type_dict["lower"] >= 3 and type_dict["upper"] >= 3)
            or (type_dict["upper"] >= 3 and type_dict["other"] >= 2)
        ):
            level_point += 1

        # 9. 组合加分, 长度大于8
        if (
            (length > 8 and type_dict["digit"] >= 2 and type_dict["lower"] >= 2 and type_dict["upper"] >= 2)
            or (type_dict["digit"] >= 2 and type_dict["lower"] >= 2 and type_dict["other"] >= 2)
            or (type_dict["digit"] >= 2 and type_dict["upper"] >= 2 and type_dict["other"] >= 2)
            or (type_dict["lower"] >= 2 and type_dict["upper"] >= 2 and type_dict["other"] >= 2)
        ):
            level_point += 1

        # 10. 组合加分, 长度大于10
        if (
            length > 10
            and type_dict["digit"] >= 2
            and type_dict["lower"] >= 2
            and type_dict["upper"] >= 2
            and type_dict["other"] >= 2
        ):
            level_point += 1

        # 减分项
        # 1. 连续小写字母或者大写字母
        if (
            StringUtil.first_index_of(
                string.ascii_lowercase,
                0,
                passwd,
            )
            >= 0
            or StringUtil.first_index_of(string.ascii_uppercase, 0, passwd) >= 0
        ):
            level_point -= 1
        # 2. 键盘连续字符
        if (
            StringUtil.first_index_of("qwertyuiop", 0, passwd) >= 0
            or StringUtil.first_index_of("asdfghjkl", 0, passwd) >= 0
            or StringUtil.first_index_of("zxcvbnm", 0, passwd) >= 0
        ):
            level_point -= 1

        # 3. 数字连续字符
        if (
            StringUtil.first_index_of("01234567890", 0, passwd) >= 0
            or StringUtil.first_index_of("09876543210", 0, passwd) >= 0
        ):
            level_point -= 1

        # 4. 如果只有一种类型的字符, 则减分
        if type_dict["digit"] == length or type_dict["lower"] == length or type_dict["upper"] == length:
            level_point -= 1

        # 5. 前后两半密码相等
        if length % 2 == 0:
            part1, part2 = SequenceUtil.split_half(passwd)
            if part1 == part2:
                level_point -= 1

        # 6. 如果能切分成三部分, 且三部分相等, 则减分
        if length % 3 == 0:
            part1, part2, part3 = SequenceUtil.split_sequence(passwd, 3)
            if part1 == part2 == part3:
                level_point -= 1

        # 7. 密码是一个日期, 则减分
        if DatetimeValidator.is_valid_birthday(passwd):
            level_point -= 1

        # 如果设置的密码和简单密码库匹配则判定为弱密码
        for c in cls.SIMPLE_PWD:
            if passwd == c:
                level_point = -1

                break

        # 特殊规则, 长度不够判定为弱密码
        level_point += cls._calc_grade_by_length(length)

        # 特殊规则, 所有的字符相等直接判定为弱密码
        if StringUtil.is_all_element_equal(passwd):
            level_point = 0

        return max(0, level_point)

    @classmethod
    def get_level(cls, score: int) -> PasswdStrength:
        """
        根据得分计算密码等级

        Parameters
        ----------
        score : int
            密码强度得分

        Returns
        -------
        PasswdStrength
            密码等级
        """
        if 0 <= score <= 3:
            return PasswdStrength.EASY
        elif 4 <= score <= 6:
            return PasswdStrength.MIDIUM
        elif 7 <= score <= 9:
            return PasswdStrength.STRONG
        elif 10 <= score <= 12:
            return PasswdStrength.VERY_STRONG
        else:
            return PasswdStrength.EXTREMELY_STRONG

    @classmethod
    def check(cls, passwd: str) -> PasswdStrength:
        """
        计算密码强度得分+返回密码等级

        Parameters
        ----------
        passwd : str
            待检测密码

        Returns
        -------
        PasswdStrength
            密码等级
        """
        passwd_score = cls.get_strength_score(passwd)
        return cls.get_level(passwd_score)

    @classmethod
    def _calc_grade_by_length(cls, length: int) -> int:
        grade = 0
        if length < 3:
            grade = -100
        if length <= 4:
            grade -= 1
        if length <= 6:
            grade -= 1

        return grade
