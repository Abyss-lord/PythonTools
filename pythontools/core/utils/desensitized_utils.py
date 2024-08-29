# Copyright 2024 The pythontools Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
-------------------------------------------------
@File       :   DesensitizedUtil.py
@Date       :   2024/08/08
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/08
@Author     :   Plord117
@Desc       :   完成脱敏工具类
-------------------------------------------------
"""

# here put the import lib
from ..constants.string_constant import CharPool, DesensitizedType
from ..decorator import UnCheckFunction
from .basicutils import StringUtil

DesensitizedType.mro

WARNING_ENABLED = True


class DesensitizedUtil:
    @staticmethod
    def desensitize(value: str | bytes, desensitized_type: DesensitizedType) -> str:
        """
        脱敏，使用默认的脱敏策略，及字符串替换

        Parameters
        ----------
        value : str | bytes
            待脱敏的信息字符串
        desensitized_type : DesensitizedType
            脱敏类型

        Returns
        -------
        str
            脱敏后的数据

        Raises
        ------
        ValueError
            当无法正确识别脱敏类型时抛出异常
        """
        if desensitized_type == DesensitizedType.ADDRESS:
            return DesensitizedUtil.desensitize_address(value, 10)
        elif desensitized_type == DesensitizedType.BANK_CARD:
            return DesensitizedUtil.desensitize_bank_card(value)
        elif desensitized_type == DesensitizedType.CAR_LICENSE:
            return DesensitizedUtil.desensitize_car_license(value)
        elif desensitized_type == DesensitizedType.CHINESE_NAME:
            return DesensitizedUtil.desensitize_chinese_name(value)
        elif desensitized_type == DesensitizedType.EMAIL:
            return DesensitizedUtil.desensitize_email(value)
        elif desensitized_type == DesensitizedType.FIXED_PHONE:
            return DesensitizedUtil.desensitize_fix_phone(value)
        elif desensitized_type == DesensitizedType.ID_CARD:
            return DesensitizedUtil.desensitize_id_card(value)
        elif desensitized_type == DesensitizedType.IPV4:
            return DesensitizedUtil.desensitize_ipv4(value)
        elif desensitized_type == DesensitizedType.MOBILE_PHONE:
            return DesensitizedUtil.desensitize_mobile_phone(value)
        elif desensitized_type == DesensitizedType.PASSWORD:
            return DesensitizedUtil.desensitize_password(value)
        elif desensitized_type == DesensitizedType.IPV6:
            return DesensitizedUtil.desensitize_ipv6(value)
        elif desensitized_type == DesensitizedType.ALL_MASK:
            return DesensitizedUtil.mask_all(value)
        elif desensitized_type == DesensitizedType.FIRST_MASK:
            return DesensitizedUtil.retain_first(value)
        elif desensitized_type == DesensitizedType.LAST_MASK:
            return DesensitizedUtil.retain_last(value)
        else:
            raise ValueError(f"unsupported desensitized type: {desensitized_type}")

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def retain_front_and_end(cls, value: str | bytes, front: int, end: int) -> str:
        """
        根据前后保留的位数脱敏

        Parameters
        ----------
        value : str | bytes
            待脱敏信息
        front : int
            前缀保留位数
        end : int
            后缀保留位数

        Returns
        -------
        str
            脱敏后数据

        Raises
        ------
        ValueError
            当保留位数合计大于字符串长度时抛出异常
        ValueError
            当保留位数小于0时抛出异常
        """
        if isinstance(value, bytes):
            value = value.decode()

        # NOTE 不确定添加是否正确
        value = value.strip()

        if StringUtil.is_blank(value):
            return StringUtil.EMPTY

        if (total := front + end) > StringUtil.get_length(value):
            raise ValueError(
                f"front + end should be less than or equal to the length of value, \
                now front: {front}, end: {end}, total length: {total}"
            )

        if front < 0 or end < 0:
            raise ValueError(
                f"front and end should be greater than or equal to 0, \
                now front: {front}, end: {end}"
            )

        return StringUtil.hide(value, front, StringUtil.get_length(value) - end)

    @classmethod
    def mask_all(cls, value: str | bytes) -> str:
        """
        全部掩码

        Parameters
        ----------
        value : str | bytes
            待脱敏数据

        Returns
        -------
        str
            脱敏后数据
        """
        return cls.retain_front_and_end(value, 0, 0)

    @classmethod
    def retain_first(cls, value: str | bytes) -> str:
        """
        除第一个前缀外全部掩码

        Parameters
        ----------
        value : str | bytes
            待脱敏数据

        Returns
        -------
        str
            脱敏后数据
        """
        return cls.retain_front_and_end(value, 1, 0)

    @classmethod
    def retain_last(cls, value: str | bytes) -> str:
        """
        除最后一位后缀外全部掩码

        Parameters
        ----------
        value : str | bytes
            待脱敏数据

        Returns
        -------
        str
            脱敏后数据
        """
        return cls.retain_front_and_end(value, 0, 1)

    @classmethod
    def desensitize_chinese_name(cls, name: str | bytes) -> str:
        """
        脱敏中文姓名

        Parameters
        ----------
        name : str | bytes
            待脱敏中文姓名

        Returns
        -------
        str
            脱敏后的中文姓名
        """
        return cls.retain_first(name)

    @classmethod
    def desensitize_id_card(cls, id_card: str | bytes) -> str:
        """
        脱敏身份证信息

        Parameters
        ----------
        id_card : str | bytes
            待脱敏身份证信息

        Returns
        -------
        str
            脱敏后身份证信息
        """
        return cls.retain_front_and_end(
            id_card,
            6,
            4,
        )

    @classmethod
    def desensitize_fix_phone(cls, phone: str | bytes) -> str:
        """
        脱敏固定电话号码

        Parameters
        ----------
        phone : str | bytes
            待脱敏固定电话号码

        Returns
        -------
        str
            脱敏后固定电话号码
        """
        return cls.retain_front_and_end(
            phone,
            3,
            4,
        )

    @classmethod
    def desensitize_mobile_phone(cls, phone: str | bytes) -> str:
        """
        脱敏移动电话号码

        Parameters
        ----------
        phone : str | bytes
            待脱敏移动电话号码

        Returns
        -------
        str
            脱敏后移动电话号码
        """
        return cls.retain_front_and_end(
            phone,
            3,
            4,
        )

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def desensitize_email(cls, email: str | bytes) -> str:
        """
        脱敏电子邮箱

        Parameters
        ----------
        email : str | bytes
            待脱敏电子邮箱

        Returns
        -------
        str
            脱敏后的电子邮箱
        """
        if isinstance(email, bytes):
            email = email.decode()
        if StringUtil.is_blank(email):
            return StringUtil.EMPTY
        prefix, symbol, suffix = email.partition("@")
        return cls.retain_first(prefix) + symbol + suffix

    @classmethod
    def desensitize_password(cls, password: str | bytes) -> str:
        """
        脱敏密码

        Parameters
        ----------
        password : str | bytes
            待脱敏密码

        Returns
        -------
        str
            脱敏后的密码
        """
        return cls.mask_all(password)

    @classmethod
    @UnCheckFunction(WARNING_ENABLED)
    @UnCheckFunction(WARNING_ENABLED)
    def desensitize_bank_card(cls, bank_card: str | bytes) -> str:
        """
        脱敏银行卡号

        Parameters
        ----------
        bank_card : str | bytes
            待脱敏银行卡号

        Returns
        -------
        str
            脱敏后的银行卡号
        """
        if isinstance(bank_card, bytes):
            bank_card = bank_card.decode()
        if StringUtil.is_blank(bank_card):
            return StringUtil.EMPTY

        new_bank_card = StringUtil.remove_blank(bank_card)

        str_lst = list(StringUtil.get_chunks(new_bank_card, 4))
        desensitized_bank_card = []
        for i, s in enumerate(str_lst):
            if i == 0:
                desensitized_bank_card.append(s)
                continue
            if StringUtil.get_length(s) == 4 and i != len(str_lst) - 1:
                desensitized_bank_card.append(StringUtil.repeat_by_length(CharPool.ASTERISK, 4))
            else:
                desensitized_bank_card.append(s)
        return CharPool.SPACE.join(desensitized_bank_card)

    @classmethod
    def desensitize_car_license(cls, car_license: str | bytes) -> str:
        """
        脱敏车牌号

        Parameters
        ----------
        car_license : str | bytes
            待脱敏车牌号

        Returns
        -------
        str
            脱敏后的车牌号

        Raises
        ------
        ValueError
            如果车牌号长度不为7或8时抛出异常
        """
        if isinstance(car_license, bytes):
            car_license = car_license.decode()
        if StringUtil.is_blank(car_license):
            return StringUtil.EMPTY

        if StringUtil.get_length(car_license) == 7:
            return cls.retain_front_and_end(car_license, 3, 1)
        elif StringUtil.get_length(car_license) == 8:
            return cls.retain_front_and_end(car_license, 3, 1)
        else:
            raise ValueError("car_license should be 7 or 8 length")

    @classmethod
    def desensitize_ipv4(cls, ipv4: str | bytes) -> str:
        """
        脱敏ipv4地址

        Parameters
        ----------
        ipv4 : str | bytes
            待脱敏ipv4地址

        Returns
        -------
        str
            脱敏后的ipv4地址
        """
        if isinstance(ipv4, bytes):
            ipv4 = ipv4.decode()
        return f"{StringUtil.sub_before(ipv4, CharPool.DOT, False)}.*.*.*"

    @classmethod
    def desensitize_ipv6(cls, ipv6: str | bytes) -> str:
        """
        脱敏ipv6地址

        Parameters
        ----------
        ipv6 : str | bytes
            待脱敏ipv6地址

        Returns
        -------
        str
            脱敏后的ipv6地址
        """
        if isinstance(ipv6, bytes):
            ipv6 = ipv6.decode()

        return f"{StringUtil.sub_before(ipv6, CharPool.COLON, False)}:*:*:*:*:*:*:*"

    @classmethod
    def desensitize_address(cls, address: str | bytes, sensitive_size: int) -> str:
        """
        脱敏地址信息

        Parameters
        ----------
        address : str | bytes
            待脱敏地址信息
        sensitive_size : int
            敏感信息位数

        Returns
        -------
        str
            脱敏后的地址信息
        """
        if isinstance(address, bytes):
            address = address.decode()

        if sensitive_size <= 0:
            return address

        retain_size = StringUtil.get_length(address) - sensitive_size
        if retain_size < 0:
            return StringUtil.hide(address, 0, StringUtil.get_length(address))

        return cls.retain_front_and_end(address, retain_size, 0)
