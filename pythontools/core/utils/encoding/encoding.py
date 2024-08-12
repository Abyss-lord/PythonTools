#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   encoding.py
@Date       :   2024/08/12
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/12
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""

# here put the import lib
import base64

from pythontools.core.constants.string_constant import CharsetUtil


class EncodingUtil:
    DECODE_FAIL_RESULT = "FAILE TO DECODE"

    @classmethod
    def encode_base64(cls, input_data: str | bytes) -> bytes:  # -> Any:
        # 如果输入是字符串，先将其转换为字节数据
        if isinstance(input_data, str):
            input_data = input_data.encode(CharsetUtil.UTF_8)

        return base64.b64encode(input_data)

    @classmethod
    def decode_base64(cls, input_data: bytes) -> str:
        """
        base64解码

        Parameters
        ----------
        input_data : bytes
            待解码数据

        Returns
        -------
        bytes
            解码后的数据
        """

        decoded_data = base64.b64decode(input_data)

        try:
            decode_str_data = decoded_data.decode(CharsetUtil.UTF_8)
        except UnicodeDecodeError:
            return cls.DECODE_FAIL_RESULT

        return decode_str_data

    @classmethod
    def encode_base32(cls, input_data: str | bytes) -> bytes:
        if isinstance(input_data, str):
            input_data = input_data.encode(CharsetUtil.UTF_8)

        return base64.b32encode(input_data)

    @classmethod
    def decode_base32(cls, input_data: bytes) -> str:
        decoded_data = base64.b32decode(input_data)
        try:
            decode_str_data = decoded_data.decode(CharsetUtil.UTF_8)
        except UnicodeDecodeError:
            return cls.DECODE_FAIL_RESULT

        return decode_str_data
