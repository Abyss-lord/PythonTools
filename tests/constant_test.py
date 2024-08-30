#!/usr/bin/env python
"""
-------------------------------------------------
@File       :   test_constant.py
@Date       :   2024/08/14
@Desc       :   None
@Version    :   1.0
-------------------------------------------------
Change Activity:
@Date       :   2024/08/14
@Author     :   Plord117
@Desc       :   None
-------------------------------------------------
"""
# here put the import lib

import calendar
from datetime import datetime

import allure
import pytest

from .context_test import DesensitizedType, Gender, Month, Quarter, TimeUnit, Week


@allure.feature("测试常量类")
@allure.description("各个时间、日期枚举类")
@allure.tag("constant")
class TestConstant:
    @allure.story("季度枚举类")
    @allure.description("季度枚举类, 用于获取季度的中文名称、名称、值")
    class TestQuarter:
        @allure.title("测试获取季度枚举类")
        def test_get_quarter_with_incorrect_arguments(self) -> None:
            with allure.step("步骤1:测试输入错误的类型"):
                with pytest.raises(TypeError):
                    Quarter.get_quarter([])

            with allure.step("步骤2:测试返回None的边界值"):
                assert Quarter.get_quarter(13) is None
                assert Quarter.get_quarter("q5") is None
                assert Quarter.get_quarter("第5季度") is None
                assert Quarter.get_quarter("5季度") is None

            with allure.step("步骤3:测试根据输入的数字值获取枚举类"):
                assert Quarter.get_quarter(1) == Quarter.Q1
                assert Quarter.get_quarter(4) == Quarter.Q2
                assert Quarter.get_quarter(7) == Quarter.Q3
                assert Quarter.get_quarter(10) == Quarter.Q4

            with allure.step("步骤4:测试根据输入的带前缀英文名称获取枚举类"):
                assert Quarter.get_quarter("Q1") == Quarter.Q1
                assert Quarter.get_quarter("Q2") == Quarter.Q2
                assert Quarter.get_quarter("Q3") == Quarter.Q3
                assert Quarter.get_quarter("Q4") == Quarter.Q4

                assert Quarter.get_quarter("q1") == Quarter.Q1
                assert Quarter.get_quarter("q2") == Quarter.Q2
                assert Quarter.get_quarter("q3") == Quarter.Q3
                assert Quarter.get_quarter("q4") == Quarter.Q4

            with allure.step("步骤5:测试根据输入的中文名称获取枚举类"):
                assert Quarter.get_quarter("第一季度") == Quarter.Q1
                assert Quarter.get_quarter("第二季度") == Quarter.Q2
                assert Quarter.get_quarter("第三季度") == Quarter.Q3
                assert Quarter.get_quarter("第四季度") == Quarter.Q4

                assert Quarter.get_quarter("一季度") == Quarter.Q1
                assert Quarter.get_quarter("二季度") == Quarter.Q2
                assert Quarter.get_quarter("三季度") == Quarter.Q3
                assert Quarter.get_quarter("四季度") == Quarter.Q4

                assert Quarter.get_quarter("第1季度") == Quarter.Q1
                assert Quarter.get_quarter("第2季度") == Quarter.Q2
                assert Quarter.get_quarter("第3季度") == Quarter.Q3
                assert Quarter.get_quarter("第4季度") == Quarter.Q4

                assert Quarter.get_quarter("1季度") == Quarter.Q1
                assert Quarter.get_quarter("2季度") == Quarter.Q2
                assert Quarter.get_quarter("3季度") == Quarter.Q3
                assert Quarter.get_quarter("4季度") == Quarter.Q4

        @allure.title("测试获取季度枚举类中文名称")
        def test_get_chinese_format(self) -> None:
            assert Quarter.Q1.get_chinese_format() == "第一季度"
            assert Quarter.Q2.get_chinese_format() == "第二季度"
            assert Quarter.Q3.get_chinese_format() == "第三季度"
            assert Quarter.Q4.get_chinese_format() == "第四季度"

        @allure.title("测试获取季度枚举类名称")
        def test_get_name(self) -> None:
            assert Quarter.Q1.get_name() == "Q1"
            assert Quarter.Q2.get_name() == "Q2"
            assert Quarter.Q3.get_name() == "Q3"
            assert Quarter.Q4.get_name() == "Q4"

        @allure.title("测试获取季度枚举类值")
        def test_get_val(self) -> None:
            assert Quarter.Q1.get_value() == 1
            assert Quarter.Q2.get_value() == 2
            assert Quarter.Q3.get_value() == 3
            assert Quarter.Q4.get_value() == 4

        @allure.title("测试获取季度枚举类最大、最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Quarter.get_max_value() == 4
            assert Quarter.get_min_value() == 1

        @allure.title("测试判断季度枚举类是否为第一个季度或者最后一个季度")
        def test_is_first_or_last_quarter(self) -> None:
            with allure.step("步骤1:测试判断第一个季度"):
                assert Quarter.Q1.is_first_quarter()
                assert not Quarter.Q2.is_first_quarter()
                assert not Quarter.Q3.is_first_quarter()
                assert not Quarter.Q4.is_first_quarter()

            with allure.step("步骤2:测试判断最后一个季度"):
                assert not Quarter.Q1.is_last_quarter()
                assert not Quarter.Q2.is_last_quarter()
                assert not Quarter.Q3.is_last_quarter()
                assert Quarter.Q4.is_last_quarter()

        @allure.title("测试判断给定季度值是否合法")
        def test_is_valid_quarter(self) -> None:
            assert Quarter.is_valid_quarter(1)
            assert Quarter.is_valid_quarter(2)
            assert Quarter.is_valid_quarter(3)
            assert Quarter.is_valid_quarter(4)
            assert not Quarter.is_valid_quarter(0)
            assert not Quarter.is_valid_quarter(5)
            assert not Quarter.is_valid_quarter(6)
            assert not Quarter.is_valid_quarter(7)
            assert not Quarter.is_valid_quarter(8)
            assert not Quarter.is_valid_quarter(9)
            assert not Quarter.is_valid_quarter(10)
            assert not Quarter.is_valid_quarter(11)
            assert not Quarter.is_valid_quarter(12)
            assert not Quarter.is_valid_quarter(13)

    @allure.story("月常量类")
    @allure.description("月常量枚举类, 用于获取月份的中文名称、名称、值")
    @allure.tag("constant")
    class TestMonth:
        @allure.title("测试获取月份枚举类")
        def test_get_month_by_number(self) -> None:
            with allure.step("步骤1:测试根据数字获取月份枚举类"):
                assert Month.get_month(1) == Month.JANUARY
                assert Month.get_month(2) == Month.FEBRUARY
                assert Month.get_month(3) == Month.MARCH
                assert Month.get_month(4) == Month.APRIL
                assert Month.get_month(5) == Month.MAY
                assert Month.get_month(6) == Month.JUNE
                assert Month.get_month(7) == Month.JULY
                assert Month.get_month(8) == Month.AUGUST
                assert Month.get_month(9) == Month.SEPTEMBER
                assert Month.get_month(10) == Month.OCTOBER
                assert Month.get_month(11) == Month.NOVEMBER
                assert Month.get_month(12) == Month.DECEMBER

            with allure.step("步骤2:测试根据名称获取月份枚举类"):
                assert Month.get_month("JANUARY") == Month.JANUARY
                assert Month.get_month("FEBRUARY") == Month.FEBRUARY
                assert Month.get_month("MARCH") == Month.MARCH
                assert Month.get_month("APRIL") == Month.APRIL
                assert Month.get_month("MAY") == Month.MAY
                assert Month.get_month("JUNE") == Month.JUNE
                assert Month.get_month("JULY") == Month.JULY
                assert Month.get_month("AUGUST") == Month.AUGUST
                assert Month.get_month("SEPTEMBER") == Month.SEPTEMBER
                assert Month.get_month("OCTOBER") == Month.OCTOBER
                assert Month.get_month("NOVEMBER") == Month.NOVEMBER
                assert Month.get_month("DECEMBER") == Month.DECEMBER

            with allure.step("步骤3:测试根据中文名称获取月份枚举实例"):
                assert Month.get_month("一月") == Month.JANUARY
                assert Month.get_month("二月") == Month.FEBRUARY
                assert Month.get_month("三月") == Month.MARCH
                assert Month.get_month("四月") == Month.APRIL
                assert Month.get_month("五月") == Month.MAY
                assert Month.get_month("六月") == Month.JUNE
                assert Month.get_month("七月") == Month.JULY
                assert Month.get_month("八月") == Month.AUGUST
                assert Month.get_month("九月") == Month.SEPTEMBER
                assert Month.get_month("十月") == Month.OCTOBER
                assert Month.get_month("十一月") == Month.NOVEMBER
                assert Month.get_month("十二月") == Month.DECEMBER

                assert Month.get_month("1月") == Month.JANUARY
                assert Month.get_month("2月") == Month.FEBRUARY
                assert Month.get_month("3月") == Month.MARCH
                assert Month.get_month("4月") == Month.APRIL
                assert Month.get_month("5月") == Month.MAY
                assert Month.get_month("6月") == Month.JUNE
                assert Month.get_month("7月") == Month.JULY
                assert Month.get_month("8月") == Month.AUGUST
                assert Month.get_month("9月") == Month.SEPTEMBER
                assert Month.get_month("10月") == Month.OCTOBER
                assert Month.get_month("11月") == Month.NOVEMBER
                assert Month.get_month("12月") == Month.DECEMBER

            with allure.step("步骤4:测试根据月份简写名称获取月份枚举实例"):
                assert Month.get_month("JAN") == Month.JANUARY
                assert Month.get_month("FEB") == Month.FEBRUARY
                assert Month.get_month("MAR") == Month.MARCH
                assert Month.get_month("APR") == Month.APRIL
                assert Month.get_month("MAY") == Month.MAY
                assert Month.get_month("JUN") == Month.JUNE
                assert Month.get_month("JUL") == Month.JULY
                assert Month.get_month("AUG") == Month.AUGUST
                assert Month.get_month("SEP") == Month.SEPTEMBER
                assert Month.get_month("OCT") == Month.OCTOBER
                assert Month.get_month("NOV") == Month.NOVEMBER
                assert Month.get_month("DEC") == Month.DECEMBER

            with allure.step("步骤5:测试根据输入的 datetime 对象获取月份枚举实例"):
                assert Month.get_month(datetime(2021, 1, 1)) == Month.JANUARY
                assert Month.get_month(datetime(2021, 2, 1)) == Month.FEBRUARY
                assert Month.get_month(datetime(2021, 3, 1)) == Month.MARCH
                assert Month.get_month(datetime(2021, 4, 1)) == Month.APRIL
                assert Month.get_month(datetime(2021, 5, 1)) == Month.MAY
                assert Month.get_month(datetime(2021, 6, 1)) == Month.JUNE
                assert Month.get_month(datetime(2021, 7, 1)) == Month.JULY
                assert Month.get_month(datetime(2021, 8, 1)) == Month.AUGUST
                assert Month.get_month(datetime(2021, 9, 1)) == Month.SEPTEMBER
                assert Month.get_month(datetime(2021, 10, 1)) == Month.OCTOBER
                assert Month.get_month(datetime(2021, 11, 1)) == Month.NOVEMBER
                assert Month.get_month(datetime(2021, 12, 1)) == Month.DECEMBER

            with allure.step("步骤6:测试输入错误的数值"):
                assert Month.get_month("INVALID") is None
                assert Month.get_month(13) is None
                assert Month.get_month("13月") is None

            with allure.step("步骤7:测试输入错误的类型"):
                with pytest.raises(TypeError):
                    Month.get_month([])

        @allure.title("测试获取月份枚举实例的天数")
        def test_month_get_last_day(self) -> None:
            assert Month.JANUARY.get_last_day(2021) == 31
            assert Month.FEBRUARY.get_last_day(2021) == 28
            assert Month.FEBRUARY.get_last_day(2020) == 29
            assert Month.MARCH.get_last_day(2021) == 31
            assert Month.APRIL.get_last_day(2021) == 30
            assert Month.MAY.get_last_day(2021) == 31
            assert Month.JUNE.get_last_day(2021) == 30
            assert Month.JULY.get_last_day(2021) == 31
            assert Month.AUGUST.get_last_day(2021) == 31
            assert Month.SEPTEMBER.get_last_day(2021) == 30
            assert Month.OCTOBER.get_last_day(2021) == 31
            assert Month.NOVEMBER.get_last_day(2021) == 30
            assert Month.DECEMBER.get_last_day(2021) == 31

        @allure.title("测试获取月份枚举实例的名称")
        def test_get_name(self) -> None:
            assert Month.JANUARY.get_name() == "JANUARY"
            assert Month.FEBRUARY.get_name() == "FEBRUARY"
            assert Month.MARCH.get_name() == "MARCH"
            assert Month.APRIL.get_name() == "APRIL"
            assert Month.MAY.get_name() == "MAY"
            assert Month.JUNE.get_name() == "JUNE"
            assert Month.JULY.get_name() == "JULY"
            assert Month.AUGUST.get_name() == "AUGUST"
            assert Month.SEPTEMBER.get_name() == "SEPTEMBER"
            assert Month.OCTOBER.get_name() == "OCTOBER"
            assert Month.NOVEMBER.get_name() == "NOVEMBER"
            assert Month.DECEMBER.get_name() == "DECEMBER"

        @allure.title("测试获取月份枚举实例的中文名称")
        def test_get_natest_get_chinese_format(self) -> None:
            assert Month.JANUARY.get_chinese_format() == "一月"
            assert Month.FEBRUARY.get_chinese_format() == "二月"
            assert Month.MARCH.get_chinese_format() == "三月"
            assert Month.APRIL.get_chinese_format() == "四月"
            assert Month.MAY.get_chinese_format() == "五月"
            assert Month.JUNE.get_chinese_format() == "六月"
            assert Month.JULY.get_chinese_format() == "七月"
            assert Month.AUGUST.get_chinese_format() == "八月"
            assert Month.SEPTEMBER.get_chinese_format() == "九月"
            assert Month.OCTOBER.get_chinese_format() == "十月"
            assert Month.NOVEMBER.get_chinese_format() == "十一月"
            assert Month.DECEMBER.get_chinese_format() == "十二月"

        @allure.title("测试获取月份枚举实例的简称")
        def test_get_alias(self) -> None:
            assert Month.JANUARY.get_alias() == "JAN".lower()
            assert Month.FEBRUARY.get_alias() == "FEB".lower()
            assert Month.MARCH.get_alias() == "MAR".lower()
            assert Month.APRIL.get_alias() == "APR".lower()
            assert Month.MAY.get_alias() == "MAY".lower()
            assert Month.JUNE.get_alias() == "JUN".lower()
            assert Month.JULY.get_alias() == "JUL".lower()
            assert Month.AUGUST.get_alias() == "AUG".lower()
            assert Month.SEPTEMBER.get_alias() == "SEP".lower()
            assert Month.OCTOBER.get_alias() == "OCT".lower()
            assert Month.NOVEMBER.get_alias() == "NOV".lower()
            assert Month.DECEMBER.get_alias() == "DEC".lower()

        @allure.title("测试获取月份枚举实例数字表示")
        def test_get_value(self) -> None:
            assert Month.JANUARY.get_value() == 1
            assert Month.FEBRUARY.get_value() == 2
            assert Month.MARCH.get_value() == 3
            assert Month.APRIL.get_value() == 4
            assert Month.MAY.get_value() == 5
            assert Month.JUNE.get_value() == 6
            assert Month.JULY.get_value() == 7
            assert Month.AUGUST.get_value() == 8
            assert Month.SEPTEMBER.get_value() == 9
            assert Month.OCTOBER.get_value() == 10
            assert Month.NOVEMBER.get_value() == 11
            assert Month.DECEMBER.get_value() == 12

        @allure.title("测试获取月份枚举类最大、最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Month.get_max_value() == 12
            assert Month.get_min_value() == 1

        @allure.title("测试判断月份枚举类是否为第一个月或者最后一个月")
        def test_is_first_or_last_month(self) -> None:
            with allure.step("步骤1:测试判断第一个月"):
                assert Month.JANUARY.is_first_month()
                assert not Month.FEBRUARY.is_first_month()
                assert not Month.MARCH.is_first_month()
                assert not Month.APRIL.is_first_month()
                assert not Month.MAY.is_first_month()
                assert not Month.JUNE.is_first_month()
                assert not Month.JULY.is_first_month()
                assert not Month.AUGUST.is_first_month()
                assert not Month.SEPTEMBER.is_first_month()
                assert not Month.OCTOBER.is_first_month()
                assert not Month.NOVEMBER.is_first_month()
                assert not Month.DECEMBER.is_first_month()

            with allure.step("步骤2:测试判断最后一个月"):
                assert not Month.JANUARY.is_last_month()
                assert not Month.FEBRUARY.is_last_month()
                assert not Month.MARCH.is_last_month()
                assert not Month.APRIL.is_last_month()
                assert not Month.MAY.is_last_month()
                assert not Month.JUNE.is_last_month()
                assert not Month.JULY.is_last_month()
                assert not Month.AUGUST.is_last_month()
                assert not Month.SEPTEMBER.is_last_month()
                assert not Month.OCTOBER.is_last_month()
                assert not Month.NOVEMBER.is_last_month()
                assert Month.DECEMBER.is_last_month()

        @allure.title("测试判断给定月份值是否合法")
        def test_is_valid_month(self) -> None:
            assert Month.is_valid_month(1)
            assert Month.is_valid_month(2)
            assert Month.is_valid_month(3)
            assert Month.is_valid_month(4)
            assert Month.is_valid_month(5)
            assert Month.is_valid_month(6)
            assert Month.is_valid_month(7)
            assert Month.is_valid_month(8)
            assert Month.is_valid_month(9)
            assert Month.is_valid_month(10)
            assert Month.is_valid_month(11)
            assert Month.is_valid_month(12)

            assert not Month.is_valid_month(0)
            assert not Month.is_valid_month(13)

    @allure.story("周单位枚举")
    @allure.description("周单位枚举, 表示周一到周日的枚举")
    class TestWeek:
        @allure.title("测试获取周枚举实例")
        def test_get_week_by_int(self) -> None:
            with allure.step("步骤1:测试根据数字获取周枚举实例"):
                assert Week.get_week(1) == Week.MONDAY
                assert Week.get_week(2) == Week.TUESDAY
                assert Week.get_week(3) == Week.WEDNESDAY
                assert Week.get_week(4) == Week.THURSDAY
                assert Week.get_week(5) == Week.FRIDAY
                assert Week.get_week(6) == Week.SATURDAY
                assert Week.get_week(7) == Week.SUNDAY

            with allure.step("步骤2:测试根据中文获取周枚举实例"):
                assert Week.get_week("星期一") == Week.MONDAY
                assert Week.get_week("星期二") == Week.TUESDAY
                assert Week.get_week("星期三") == Week.WEDNESDAY
                assert Week.get_week("星期四") == Week.THURSDAY
                assert Week.get_week("星期五") == Week.FRIDAY
                assert Week.get_week("星期六") == Week.SATURDAY
                assert Week.get_week("星期日") == Week.SUNDAY

                assert Week.get_week("星期1") == Week.MONDAY
                assert Week.get_week("星期2") == Week.TUESDAY
                assert Week.get_week("星期3") == Week.WEDNESDAY
                assert Week.get_week("星期4") == Week.THURSDAY
                assert Week.get_week("星期5") == Week.FRIDAY
                assert Week.get_week("星期6") == Week.SATURDAY
                assert Week.get_week("星期7") == Week.SUNDAY

                assert Week.get_week("周一") == Week.MONDAY
                assert Week.get_week("周二") == Week.TUESDAY
                assert Week.get_week("周三") == Week.WEDNESDAY
                assert Week.get_week("周四") == Week.THURSDAY
                assert Week.get_week("周五") == Week.FRIDAY
                assert Week.get_week("周六") == Week.SATURDAY
                assert Week.get_week("周日") == Week.SUNDAY

                assert Week.get_week("周1") == Week.MONDAY
                assert Week.get_week("周2") == Week.TUESDAY
                assert Week.get_week("周3") == Week.WEDNESDAY
                assert Week.get_week("周4") == Week.THURSDAY
                assert Week.get_week("周5") == Week.FRIDAY
                assert Week.get_week("周6") == Week.SATURDAY
                assert Week.get_week("周7") == Week.SUNDAY

            with allure.step("步骤3:测试根据名称获取周枚举实例"):
                assert Week.get_week("MONDAY") == Week.MONDAY
                assert Week.get_week("TUESDAY") == Week.TUESDAY
                assert Week.get_week("WEDNESDAY") == Week.WEDNESDAY
                assert Week.get_week("THURSDAY") == Week.THURSDAY
                assert Week.get_week("FRIDAY") == Week.FRIDAY
                assert Week.get_week("SATURDAY") == Week.SATURDAY
                assert Week.get_week("SUNDAY") == Week.SUNDAY

            with allure.step("步骤4:测试根据简称获取周枚举实例"):
                assert Week.get_week("MON") == Week.MONDAY
                assert Week.get_week("TUE") == Week.TUESDAY
                assert Week.get_week("WED") == Week.WEDNESDAY
                assert Week.get_week("THU") == Week.THURSDAY
                assert Week.get_week("FRI") == Week.FRIDAY
                assert Week.get_week("SAT") == Week.SATURDAY
                assert Week.get_week("SUN") == Week.SUNDAY

            with allure.step("步骤5:测试根据detetime对象获取周枚举实例"):
                assert Week.get_week(datetime(2024, 8, 26)) == Week.MONDAY
                assert Week.get_week(datetime(2024, 8, 27)) == Week.TUESDAY
                assert Week.get_week(datetime(2024, 8, 28)) == Week.WEDNESDAY
                assert Week.get_week(datetime(2024, 8, 29)) == Week.THURSDAY
                assert Week.get_week(datetime(2024, 8, 30)) == Week.FRIDAY
                assert Week.get_week(datetime(2024, 8, 31)) == Week.SATURDAY
                assert Week.get_week(datetime(2024, 9, 1)) == Week.SUNDAY
            with allure.step("步骤6:测试输入错误的数值"):
                assert Week.get_week(8) is None
                assert Week.get_week("星期八") is None
                assert Week.get_week("星期9") is None

            with allure.step("步骤7:测试输入错误的类型"):
                with pytest.raises(TypeError):
                    Week.get_week(None)

        @allure.title("测试获取周枚举实例的名称")
        def test_get_name(self) -> None:
            assert Week.MONDAY.get_name() == "MONDAY"
            assert Week.TUESDAY.get_name() == "TUESDAY"
            assert Week.WEDNESDAY.get_name() == "WEDNESDAY"
            assert Week.THURSDAY.get_name() == "THURSDAY"
            assert Week.FRIDAY.get_name() == "FRIDAY"
            assert Week.SATURDAY.get_name() == "SATURDAY"
            assert Week.SUNDAY.get_name() == "SUNDAY"

        @allure.title("测试获取周枚举实例的中文名称")
        def test_get_chinese_format(self) -> None:
            with allure.step("步骤1:测试获取中文名称, 使用默认前缀"):
                assert Week.MONDAY.get_chinese_format() == "星期一"
                assert Week.TUESDAY.get_chinese_format() == "星期二"
                assert Week.WEDNESDAY.get_chinese_format() == "星期三"
                assert Week.THURSDAY.get_chinese_format() == "星期四"
                assert Week.FRIDAY.get_chinese_format() == "星期五"
                assert Week.SATURDAY.get_chinese_format() == "星期六"
                assert Week.SUNDAY.get_chinese_format() == "星期日"

            with allure.step("步骤2:测试获取中文名称, 使用自定义前缀"):
                assert Week.MONDAY.get_chinese_format("周") == "周一"
                assert Week.TUESDAY.get_chinese_format("周") == "周二"
                assert Week.WEDNESDAY.get_chinese_format("周") == "周三"
                assert Week.THURSDAY.get_chinese_format("周") == "周四"
                assert Week.FRIDAY.get_chinese_format("周") == "周五"
                assert Week.SATURDAY.get_chinese_format("周") == "周六"
                assert Week.SUNDAY.get_chinese_format("周") == "周日"

        @allure.title("测试获取周枚举实例的简称")
        def test_get_alias(self) -> None:
            assert Week.MONDAY.get_alias() == "MON".lower()
            assert Week.TUESDAY.get_alias() == "TUE".lower()
            assert Week.WEDNESDAY.get_alias() == "WED".lower()
            assert Week.THURSDAY.get_alias() == "THU".lower()
            assert Week.FRIDAY.get_alias() == "FRI".lower()
            assert Week.SATURDAY.get_alias() == "SAT".lower()
            assert Week.SUNDAY.get_alias() == "SUN".lower()

        @allure.title("测试获取周枚举实例对应的calendar值")
        def test_get_value(self) -> None:
            assert Week.MONDAY.get_value() == calendar.MONDAY
            assert Week.TUESDAY.get_value() == calendar.TUESDAY
            assert Week.WEDNESDAY.get_value() == calendar.WEDNESDAY
            assert Week.THURSDAY.get_value() == calendar.THURSDAY
            assert Week.FRIDAY.get_value() == calendar.FRIDAY
            assert Week.SATURDAY.get_value() == calendar.SATURDAY
            assert Week.SUNDAY.get_value() == calendar.SUNDAY

        @allure.title("测试获取周枚举实例的ISO8601值")
        def test_get_iso8601_value(self) -> None:
            assert Week.MONDAY.get_iso8601_value() == 1
            assert Week.TUESDAY.get_iso8601_value() == 2
            assert Week.WEDNESDAY.get_iso8601_value() == 3
            assert Week.THURSDAY.get_iso8601_value() == 4
            assert Week.FRIDAY.get_iso8601_value() == 5
            assert Week.SATURDAY.get_iso8601_value() == 6
            assert Week.SUNDAY.get_iso8601_value() == 7

        @allure.title("测试周最大值和最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Week.get_max_value() == 7
            assert Week.get_min_value() == 1

        @allure.title("测试判断周枚举实例是否为第一个周或者最后一个周")
        def test_is_first_or_last_week(self) -> None:
            with allure.step("步骤1:测试判断第一个周"):
                assert Week.MONDAY.is_first_day_of_week()
                assert not Week.TUESDAY.is_first_day_of_week()
                assert not Week.WEDNESDAY.is_first_day_of_week()
                assert not Week.THURSDAY.is_first_day_of_week()
                assert not Week.FRIDAY.is_first_day_of_week()
                assert not Week.SATURDAY.is_first_day_of_week()
                assert not Week.SUNDAY.is_first_day_of_week()

            with allure.step("步骤2:测试判断最后一个周"):
                assert not Week.MONDAY.is_last_day_of_week()
                assert not Week.TUESDAY.is_last_day_of_week()
                assert not Week.WEDNESDAY.is_last_day_of_week()
                assert not Week.THURSDAY.is_last_day_of_week()
                assert not Week.FRIDAY.is_last_day_of_week()
                assert not Week.SATURDAY.is_last_day_of_week()
                assert Week.SUNDAY.is_last_day_of_week()

        @allure.title("测试判断给定周值是否合法")
        def test_is_valid_week(self) -> None:
            assert Week.is_valid_weekday(1)
            assert Week.is_valid_weekday(2)
            assert Week.is_valid_weekday(3)
            assert Week.is_valid_weekday(4)
            assert Week.is_valid_weekday(5)
            assert Week.is_valid_weekday(6)
            assert Week.is_valid_weekday(7)
            assert not Week.is_valid_weekday(0)
            assert not Week.is_valid_weekday(8)

    @allure.story("时间单位枚举")
    @allure.description("时间单位枚举, 表示时间单位的枚举, 纳秒,微秒,毫秒,秒,分钟,小时,天")
    class TestTimeUnit:
        @allure.title("测试时间单位之间的转换")
        def test_convert(self) -> None:
            with allure.step("步骤1:纳秒的转换"):
                assert TimeUnit.NANOSECONDS.to_nanos(1) == 1

            with allure.step("步骤2:微秒的转换"):
                assert TimeUnit.MICROSECONDS.to_micros(1) == 1
                assert TimeUnit.MICROSECONDS.to_nanos(1) == 1000

            with allure.step("步骤3:毫秒的转换"):
                assert TimeUnit.MILLISECONDS.to_millis(1) == 1
                assert TimeUnit.MILLISECONDS.to_micros(1) == 1000
                assert TimeUnit.MILLISECONDS.to_nanos(1) == 1000000

            with allure.step("步骤4:秒的转换"):
                assert TimeUnit.SECONDS.to_seconds(1) == 1
                assert TimeUnit.SECONDS.to_millis(1) == 1000
                assert TimeUnit.SECONDS.to_micros(1) == 1000000
                assert TimeUnit.SECONDS.to_nanos(1) == 1000000000

            with allure.step("步骤5:分钟的转换"):
                assert TimeUnit.MINUTES.to_minutes(1) == 1
                assert TimeUnit.MINUTES.to_seconds(1) == 60
                assert TimeUnit.MINUTES.to_millis(1) == 60000
                assert TimeUnit.MINUTES.to_micros(1) == 60000000
                assert TimeUnit.MINUTES.to_nanos(1) == 60000000000

            with allure.step("步骤6:小时的转换"):
                assert TimeUnit.HOURS.to_hours(1) == 1
                assert TimeUnit.HOURS.to_minutes(1) == 60
                assert TimeUnit.HOURS.to_seconds(1) == 3600
                assert TimeUnit.HOURS.to_millis(1) == 3600000
                assert TimeUnit.HOURS.to_micros(1) == 3600000000
                assert TimeUnit.HOURS.to_nanos(1) == 3600000000000

            with allure.step("步骤7:天的转换"):
                assert TimeUnit.DAYS.to_days(1) == 1
                assert TimeUnit.DAYS.to_hours(1) == 24
                assert TimeUnit.DAYS.to_minutes(1) == 1440
                assert TimeUnit.DAYS.to_seconds(1) == 86400
                assert TimeUnit.DAYS.to_millis(1) == 86400000
                assert TimeUnit.DAYS.to_micros(1) == 86400000000
                assert TimeUnit.DAYS.to_nanos(1) == 86400000000000

    @allure.story("性别枚举")
    @allure.description("性别枚举, 表示性别的枚举, 男,女")
    class TestGender:
        @allure.title("测试获取性别枚举实例")
        def test_get_obj(self) -> None:
            with allure.step("步骤1:测试获取男性"):
                assert Gender.get_gender_by_name("MALE") == Gender.MALE
                assert Gender.get_gender_by_name("男") == Gender.MALE
                assert Gender.get_gender_by_name("男的") == Gender.MALE
                assert Gender.get_gender_by_name("男性") == Gender.MALE

            with allure.step("步骤2:测试获取女性"):
                assert Gender.get_gender_by_name("FEMALE") == Gender.FEMALE
                assert Gender.get_gender_by_name("女性") == Gender.FEMALE
                assert Gender.get_gender_by_name("女的") == Gender.FEMALE
                assert Gender.get_gender_by_name("女") == Gender.FEMALE

            with allure.step("步骤3:测试根据数字获取性别枚举实例"):
                assert Gender.MALE == Gender.get_gender_by_code(1)
                assert Gender.FEMALE == Gender.get_gender_by_code(2)

            with allure.step("步骤4:测试获取未知性别"):
                with pytest.raises(ValueError):
                    Gender.get_gender_by_name("unknown")

    @allure.story("脱敏类型枚举")
    @allure.description(
        "脱敏类型枚举, 表示脱敏类型, 包括用户id,地址,身份证号,银行卡,手机号,\
            电子邮件,IPv4地址,IPv6地址,全部不显示,车牌号"
    )
    class TestDesensitizedType:
        @allure.title("测试获取枚举值描述信息")
        def test_get_DesensitizedType_description(self) -> None:
            assert DesensitizedType.USER_ID.get_description() == "用户id"
            assert DesensitizedType.ADDRESS.get_description() == "地址"
            assert DesensitizedType.ID_CARD.get_description() == "身份证号"
            assert DesensitizedType.BANK_CARD.get_description() == "银行卡"
            assert DesensitizedType.MOBILE_PHONE.get_description() == "手机号"
            assert DesensitizedType.EMAIL.get_description() == "电子邮件"
            assert DesensitizedType.IPV4.get_description() == "IPv4地址"
            assert DesensitizedType.IPV6.get_description() == "IPv6地址"
            assert DesensitizedType.ALL_MASK.get_description() == "全部不显示"
            assert DesensitizedType.CAR_LICENSE.get_description() == "车牌号"
