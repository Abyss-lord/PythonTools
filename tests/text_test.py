#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_text.py
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

from collections import namedtuple

import allure  # type: ignore
import pytest
from loguru import logger

from .context_test import (
    AbstractStrFinder,
    CharsetUtil,
    CsvConfig,
    CsvReader,
    FnvHash,
    NullMode,
    PasswdStrengthUtil,
    PatternFinder,
    PatternPool,
    StrFinder,
    StringUtil,
    StrJoiner,
    UnsupportedOperationError,
)


@allure.feature("测试字符串拼接类StrJoiner")
@allure.description("""
                    测试字符串拼接类StrJoiner,该类用于拼接字符串
                    """)
@allure.tag("Text")
class TestJoiner:
    @classmethod
    def setup_class(cls):
        logger.debug("初始化")

    @classmethod
    def teardown_class(cls):
        logger.debug("清除")

    @allure.title("测试StrJoiner基础功能")
    def test_joiner(self) -> None:
        @allure.step("步骤1:测试前缀+正确参数+后缀")
        def test_input_correct_args():
            joiner = StrJoiner(",", prefix="(", suffix=")")
            joiner.append("hello")
            joiner.append("world")
            assert joiner.get_merged_string() == "(hello,world)"
            joiner.append(*[1, 2, 3]).append("4")
            assert joiner.get_merged_string() == "(1,2,3,4)"

        @allure.step("步骤2:测试指定分隔符")
        def test_input_delimiter():
            joiner = StrJoiner(" ")
            joiner.append("hello")
            joiner.append("world")
            assert joiner.get_merged_string() == "hello world"

        test_input_correct_args()
        test_input_delimiter()

    @allure.title("测试获取实例")
    def test_get_instance(self):
        @allure.step("步骤1:测试获取实例")
        def test_get_instance_by_static_method():
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            test_new_joiner_1 = StrJoiner.get_instance_from_joiner(joiner)
            test_new_joiner_1.append("hello")
            test_new_joiner_1.append("world")
            assert test_new_joiner_1.get_merged_string() == "(hello,world)"

            test_new_joiner_2 = StrJoiner.get_instance(" ")
            test_new_joiner_2.append("hello")
            test_new_joiner_2.append("world")

            assert test_new_joiner_2.get_merged_string() == "hello world"

        test_get_instance_by_static_method()

    @allure.title("测试重置实例")
    def test_reset_joiner(cls):
        @allure.story("测试重置实例")
        @allure.step("步骤1:测试重置实例")
        def test_reset_joiner():
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.__initialized = False
            assert joiner.get_merged_string() == StringUtil.EMPTY

        test_reset_joiner()

    @allure.title("测试设置实例属性")
    def test_set_params(cls):
        with allure.step("步骤1:测试链式调用"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.set_delimiter("|").set_prefix("[").set_suffix("]").set_empty_result("NULL").set_null_mode(
                NullMode.EMPTY
            )
            joiner.append("hello").append("world")
            assert joiner.get_merged_string() == "[hello|world]"

        with allure.step("步骤2:测试非链式调用"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.set_delimiter("|")
            joiner.set_prefix("[")
            joiner.set_suffix("]")
            joiner.set_empty_result("NULL")
            joiner.set_null_mode(NullMode.EMPTY)
            joiner.append("hello").append("world")
            assert joiner.get_merged_string() == "[hello|world]"

    @allure.title("测试不同Null值处理方式")
    def test_null_mode(cls):
        with allure.step("步骤1:测试 IGNORE 模式"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.set_null_mode(NullMode.IGNORE)
            joiner.append("hello").append(None).append(None)
            assert joiner.get_merged_string() == "(hello)"

        with allure.step("步骤2:测试 EMPTY 模式"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.set_null_mode(NullMode.EMPTY)
            joiner.append("hello").append(None).append(None)
            assert joiner.get_merged_string() == "(hello,,)"

        with allure.step("步骤3:测试 NULL_STRING 模式"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            joiner.set_null_mode(NullMode.NULL_STRING)
            joiner.append("hello").append(None).append(None)
            assert joiner.get_merged_string() == "(hello,NONE,NONE)"

        with allure.step("步骤4:测试非法Null值处理方式"):
            joiner = StrJoiner.get_instance(",", prefix="(", suffix=")")
            with pytest.raises(ValueError):
                joiner.set_null_mode("invalid_null_mode")
                joiner.append("hello").append(None).append(None)


@allure.feature("测试字符串拼接类StrFinder")
@allure.description("""
                    测试StrFinder,该类用于查找字符串
                    """)
@allure.tag("Text")
class TestFinder:
    @allure.story("测试StrFinder")
    class TestStrFinder:
        @allure.title("测试 StrFinder 基础功能")
        def test_finder_basic_function(cls) -> None:
            with allure.step("步骤1:测试查找字符串"):
                test_finder_1 = StrFinder("abcabc", "ab")
                test_finder_1.set_case_insensitive(True)
                start_idx = test_finder_1.start(0)

                assert start_idx == 0
                assert test_finder_1.success
                assert test_finder_1.end(start_idx) == 1

            with allure.step("步骤2:测试重置功能"):
                test_finder_1.reset()
                assert not test_finder_1.success
                assert test_finder_1.end_idx == -1
                assert test_finder_1.text == ""

            with allure.step("步骤3:测试反向查找"):
                test_finder_1.set_reverse(True).set_text("abcabc")
                assert test_finder_1.start(0) == 3

            with allure.step("步骤4:测试查找失败的情况"):
                test_finder_2 = StrFinder("abcabc", "assb")
                start_idx = test_finder_2.set_case_insensitive(True).start(0)
                assert start_idx == -1

            with allure.step("步骤5:测试忽略大小写"):
                test_finder_2.reset()
                test_finder_2.set_text("AssbAssb").set_case_insensitive(False)
                test_finder_2.start(0)
                assert not test_finder_2.success
                assert test_finder_2.end_idx == -1

                test_finder_2.reset()
                test_finder_2.set_text("AssbAssb").set_case_insensitive(True)
                start_idx = test_finder_2.start(3)
                assert start_idx == 4
                assert test_finder_2.success
                assert test_finder_2.end(start_idx) == 7

    @allure.story("测试抽象类AbstractStrFinder")
    class TestAbstractStrFinder:
        @allure.title("测试实例化抽象类")
        @allure.description("测试实例化抽象类AbstractStrFinder")
        @allure.severity("critical")
        def test_create_abstract_finder_instance(cls) -> None:
            with allure.step("步骤1:测试实例化抽象类"):
                with pytest.raises(TypeError):
                    AbstractStrFinder("abc")  # type: ignore

    @allure.story("测试PatternFinder")
    class TestPatternFinder:
        @allure.title("测试 PatternFinder 基础功能")
        def test_PatternFinder(self) -> None:
            finder = PatternFinder("SSSS13812345678", PatternPool.MOBILE)
            assert finder.start(3) == 4


@allure.feature("测试密码强度工具类PasswdStrengthUtil")
@allure.description("""
                    测试密码强度工具类PasswdStrengthUtil,该类用于计算密码强度
                    """)
@allure.tag("Text", "util")
class TestPasswd:
    @allure.title("测试密码强度")
    def test_passwd(self) -> None:
        with allure.step("步骤1:测试强密码"):
            test_passwd_1 = "2hAj5#mne-ix.86H"
            assert PasswdStrengthUtil.get_strength_score(test_passwd_1) == 13

        with allure.step("步骤2:测试弱密码"):
            test_passwd_2 = "123456"
            assert PasswdStrengthUtil.get_strength_score(test_passwd_2) == 0


@allure.feature("哈希工具类")
@allure.description("哈希工具类，提供哈希方法")
@allure.tag("Hash", "tag")
class TestHash:
    @allure.title("测试哈希方法")
    def test_hash(cls) -> None:
        test_cases = [
            "",  # 空字符串
            "a",  # 单个字符
            "abc",  # 短字符串
            "Hello, World!",  # 常见短语
            "1234567890",  # 数字字符串
            "The quick brown fox jumps over the lazy dog",  # 长句子
            "aaaaaa",  # 重复字符
            "😀",  # Emoji 表情
            "Hello, 世界",  # 包含Unicode字符
            " " * 1000,  # 长空格字符串
        ]
        print("32-bit Hash Results:")
        h = FnvHash()
        for case in test_cases:
            hash_value_32 = h.hash_32(case)
            _ = h.hash_64(case)
            _ = h.hash_128(case)
            logger.debug(f"32-bit Hash value: {hash_value_32}")

        with pytest.raises(UnsupportedOperationError):
            h.hash("sdadsa")

        h.hash_32("hello world".encode(CharsetUtil.UTF_8))


@allure.feature("CSV工具类")
@allure.description("CSV工具类，提供CSV读取方法")
@allure.tag("CSV", "tag")
class TestCsv:
    TEST_CSV_FILE = "tests/resources/test_csv.csv"

    @allure.title("测试默认配置项")
    def test_get_config(cls) -> None:
        config = CsvConfig()
        assert config.delimiter == ","
        assert not config.strict_mode
        assert not config.skip_initial_space
        assert config.lineterminator == "\r\n"
        assert config.text_qualifier == '"'

    @allure.title("测试设置配置项")
    def test_set_config(cls) -> None:
        config = CsvConfig()
        config.set_skip_initial_space(True).set_strict_mode(True).set_delimiter("|").set_lineterminator("\n")
        assert config.delimiter == "|"
        assert config.strict_mode
        assert config.skip_initial_space
        assert config.lineterminator == "\n"

    @allure.title("测试读取CSV文件文件头")
    def test_reader_get_header(cls) -> None:
        reader = CsvReader(cls.TEST_CSV_FILE)
        csv_data = reader.read()
        logger.debug(csv_data.header)
        for row in csv_data.data:
            logger.debug(row)

    @allure.title("测试以字典方式读取CSV文件数据")
    def test_get_dicts_from_csv(cls) -> None:
        data_dict = CsvReader.get_dicts_from_csv(cls.TEST_CSV_FILE)
        for i in data_dict:
            logger.debug(i)

    @allure.title("测试以命名元祖的方式读取CSV文件数据")
    def test_get_namedtuple_from_csv(cls) -> None:
        Row = namedtuple("Row", ["id", "name", "age", "gender"])
        namedtuple_lst = CsvReader.get_namedtuple_from_csv(cls.TEST_CSV_FILE, Row)
        for row in namedtuple_lst:
            logger.debug(row)
