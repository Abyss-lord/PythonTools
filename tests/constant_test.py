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

from datetime import datetime

import allure  # type: ignore
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
        @pytest.mark.parametrize(
            "quarter_name, expected",
            [
                (13, None),
                ("q5", None),
                ("第5季度", None),
                ("5季度", None),
                (1, Quarter.Q1),
                (2, Quarter.Q1),
                (3, Quarter.Q1),
                (4, Quarter.Q2),
                (5, Quarter.Q2),
                (6, Quarter.Q2),
                (7, Quarter.Q3),
                (8, Quarter.Q3),
                (9, Quarter.Q3),
                (10, Quarter.Q4),
                (11, Quarter.Q4),
                (12, Quarter.Q4),
                ("Q1", Quarter.Q1),
                ("Q2", Quarter.Q2),
                ("Q3", Quarter.Q3),
                ("Q4", Quarter.Q4),
                ("第一季度", Quarter.Q1),
                ("第二季度", Quarter.Q2),
                ("第三季度", Quarter.Q3),
                ("第四季度", Quarter.Q4),
                ("一季度", Quarter.Q1),
                ("二季度", Quarter.Q2),
                ("三季度", Quarter.Q3),
                ("四季度", Quarter.Q4),
                ("1季度", Quarter.Q1),
                ("2季度", Quarter.Q2),
                ("3季度", Quarter.Q3),
                ("4季度", Quarter.Q4),
                pytest.param([], None, marks=pytest.mark.xfail(raises=TypeError)),
            ],
        )
        def test_get_quarter(self, quarter_name, expected) -> None:
            assert Quarter.get_quarter(quarter_name) == expected

        @allure.title("测试获取季度枚举类中文名称")
        @pytest.mark.parametrize(
            "quarter, expected",
            [
                (Quarter.Q1, "第一季度"),
                (Quarter.Q2, "第二季度"),
                (Quarter.Q3, "第三季度"),
                (Quarter.Q4, "第四季度"),
            ],
        )
        def test_get_chinese_format(
            self,
            quarter,
            expected,
        ) -> None:
            assert quarter.get_chinese_format() == expected

        @allure.title("测试获取季度枚举类名称")
        @pytest.mark.parametrize(
            "quarter, expected",
            [
                (Quarter.Q1, "Q1"),
                (Quarter.Q2, "Q2"),
                (Quarter.Q3, "Q3"),
                (Quarter.Q4, "Q4"),
            ],
        )
        def test_get_name(self, quarter, expected) -> None:
            assert quarter.get_name() == expected

        @allure.title("测试获取季度枚举类值")
        @pytest.mark.parametrize(
            "quarter, expected",
            [
                (Quarter.Q1, 1),
                (Quarter.Q2, 2),
                (Quarter.Q3, 3),
                (Quarter.Q4, 4),
            ],
        )
        def test_get_value(self, quarter, expected) -> None:
            assert quarter.get_value() == expected

        @allure.title("测试获取季度枚举类最大、最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Quarter.get_max_value() == 4
            assert Quarter.get_min_value() == 1

        @allure.title("测试判断季度枚举类是否为第一个季度或者最后一个季度")
        @pytest.mark.parametrize(
            "quarter, expected",
            [
                (Quarter.Q1, True),
                (Quarter.Q2, False),
                (Quarter.Q3, False),
                (Quarter.Q4, False),
            ],
        )
        def test_is_first_quarter(self, quarter, expected) -> None:
            assert quarter.is_first_quarter() == expected

        @allure.title("测试判断季度枚举类是否为最后一个季度")
        @pytest.mark.parametrize(
            "quarter, expected",
            [
                (Quarter.Q1, False),
                (Quarter.Q2, False),
                (Quarter.Q3, False),
                (Quarter.Q4, True),
            ],
        )
        def test_is_last_quarter(self, quarter, expected) -> None:
            assert quarter.is_last_quarter() == expected

        @allure.title("测试判断给定季度值是否合法")
        @pytest.mark.parametrize(
            "quarter_value, expected",
            [
                (1, True),
                (2, True),
                (3, True),
                (4, True),
                (5, False),
                (6, False),
                (7, False),
                (8, False),
                (9, False),
                (10, False),
                (11, False),
                (12, False),
                (13, False),
            ],
        )
        def test_is_valid_quarter(self, quarter_value, expected) -> None:
            assert Quarter.is_valid_quarter(quarter_value) == expected

    @allure.story("月常量类")
    @allure.description("月常量枚举类, 用于获取月份的中文名称、名称、值")
    @allure.tag("constant")
    class TestMonth:
        @allure.title("测试获取月份枚举类")
        @pytest.mark.parametrize(
            "month_num, expected",
            [
                (1, Month.JANUARY),
                (2, Month.FEBRUARY),
                (3, Month.MARCH),
                (4, Month.APRIL),
                (5, Month.MAY),
                (6, Month.JUNE),
                (7, Month.JULY),
                (8, Month.AUGUST),
                (9, Month.SEPTEMBER),
                (10, Month.OCTOBER),
                (11, Month.NOVEMBER),
                (12, Month.DECEMBER),
                (13, None),
            ],
        )
        def test_get_month_by_number(self, month_num, expected) -> None:
            assert Month._get_month_by_number(month_num) == expected

        @allure.title("测试根据英文名称获取月份枚举类")
        @pytest.mark.parametrize(
            "month_name, expected",
            [
                ("JANUARY", Month.JANUARY),
                ("FEBRUARY", Month.FEBRUARY),
                ("MARCH", Month.MARCH),
                ("APRIL", Month.APRIL),
                ("MAY", Month.MAY),
                ("JUNE", Month.JUNE),
                ("JULY", Month.JULY),
                ("AUGUST", Month.AUGUST),
                ("SEPTEMBER", Month.SEPTEMBER),
                ("OCTOBER", Month.OCTOBER),
                ("NOVEMBER", Month.NOVEMBER),
                ("DECEMBER", Month.DECEMBER),
                ("INVALID", None),
            ],
        )
        def test_get_month_by_name(
            self,
            month_name,
            expected,
        ) -> None:
            assert Month.get_month(month_name) == expected

        @allure.title("测试根据中文名称获取月份枚举类")
        @pytest.mark.parametrize(
            "month_name, expected",
            [
                ("一月", Month.JANUARY),
                ("二月", Month.FEBRUARY),
                ("三月", Month.MARCH),
                ("四月", Month.APRIL),
                ("五月", Month.MAY),
                ("六月", Month.JUNE),
                ("七月", Month.JULY),
                ("八月", Month.AUGUST),
                ("九月", Month.SEPTEMBER),
                ("十月", Month.OCTOBER),
                ("十一月", Month.NOVEMBER),
                ("十二月", Month.DECEMBER),
                ("1月", Month.JANUARY),
                ("2月", Month.FEBRUARY),
                ("3月", Month.MARCH),
                ("4月", Month.APRIL),
                ("5月", Month.MAY),
                ("6月", Month.JUNE),
                ("7月", Month.JULY),
                ("8月", Month.AUGUST),
                ("9月", Month.SEPTEMBER),
                ("10月", Month.OCTOBER),
                ("11月", Month.NOVEMBER),
                ("12月", Month.DECEMBER),
                ("INVALID", None),
                pytest.param([], None, marks=pytest.mark.xfail(raises=TypeError)),
            ],
        )
        def test_get_month_by_chinese_name(
            self,
            month_name,
            expected,
        ) -> None:
            assert Month.get_month(month_name) == expected

        @allure.title("测试根据月份简称获取月份枚举类")
        @pytest.mark.parametrize(
            "month_name, expected",
            [
                ("JAN", Month.JANUARY),
                ("FEB", Month.FEBRUARY),
                ("MAR", Month.MARCH),
                ("APR", Month.APRIL),
                ("MAY", Month.MAY),
                ("JUN", Month.JUNE),
                ("JUL", Month.JULY),
                ("AUG", Month.AUGUST),
                ("SEP", Month.SEPTEMBER),
                ("OCT", Month.OCTOBER),
                ("NOV", Month.NOVEMBER),
                ("DEC", Month.DECEMBER),
                ("INVALID", None),
            ],
        )
        def test_get_month_by_alias(
            self,
            month_name,
            expected,
        ) -> None:
            assert Month.get_month(month_name) == expected

        @allure.title("测试根据dt对象获取月份枚举实例")
        @pytest.mark.parametrize(
            "dt, expected",
            [
                (datetime(2021, 1, 1), Month.JANUARY),
                (datetime(2021, 2, 1), Month.FEBRUARY),
                (datetime(2021, 3, 1), Month.MARCH),
                (datetime(2021, 4, 1), Month.APRIL),
                (datetime(2021, 5, 1), Month.MAY),
                (datetime(2021, 6, 1), Month.JUNE),
                (datetime(2021, 7, 1), Month.JULY),
                (datetime(2021, 8, 1), Month.AUGUST),
                (datetime(2021, 9, 1), Month.SEPTEMBER),
                (datetime(2021, 10, 1), Month.OCTOBER),
                (datetime(2021, 11, 1), Month.NOVEMBER),
                (datetime(2021, 12, 1), Month.DECEMBER),
            ],
        )
        def test_get_month_by_datetime(self, dt, expected) -> None:
            assert Month.get_month(dt) == expected

        @allure.title("测试获取月份枚举实例的天数")
        @pytest.mark.parametrize(
            "month, year, expected",
            [
                (Month.JANUARY, 2021, 31),
                (Month.FEBRUARY, 2021, 28),
                (Month.FEBRUARY, 2020, 29),
                (Month.MARCH, 2021, 31),
                (Month.APRIL, 2021, 30),
                (Month.MAY, 2021, 31),
                (Month.JUNE, 2021, 30),
                (Month.JULY, 2021, 31),
                (Month.AUGUST, 2021, 31),
                (Month.SEPTEMBER, 2021, 30),
                (Month.OCTOBER, 2021, 31),
                (Month.NOVEMBER, 2021, 30),
                (Month.DECEMBER, 2021, 31),
            ],
        )
        def test_month_get_last_day(
            self,
            month,
            year,
            expected,
        ) -> None:
            assert month.get_last_day(year) == expected

        @allure.title("测试获取月份枚举实例的名称")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, "JANUARY"),
                (Month.FEBRUARY, "FEBRUARY"),
                (Month.MARCH, "MARCH"),
                (Month.APRIL, "APRIL"),
                (Month.MAY, "MAY"),
                (Month.JUNE, "JUNE"),
                (Month.JULY, "JULY"),
                (Month.AUGUST, "AUGUST"),
                (Month.SEPTEMBER, "SEPTEMBER"),
                (Month.OCTOBER, "OCTOBER"),
                (Month.NOVEMBER, "NOVEMBER"),
                (Month.DECEMBER, "DECEMBER"),
            ],
        )
        def test_get_name(self, month, expected) -> None:
            assert month.get_name() == expected

        @allure.title("测试获取月份枚举实例的中文名称")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, "一月"),
                (Month.FEBRUARY, "二月"),
                (Month.MARCH, "三月"),
                (Month.APRIL, "四月"),
                (Month.MAY, "五月"),
                (Month.JUNE, "六月"),
                (Month.JULY, "七月"),
                (Month.AUGUST, "八月"),
                (Month.SEPTEMBER, "九月"),
                (Month.OCTOBER, "十月"),
                (Month.NOVEMBER, "十一月"),
                (Month.DECEMBER, "十二月"),
            ],
        )
        def test_get_chinese_format(self, month, expected) -> None:
            assert month.get_chinese_format() == expected

        @allure.title("测试获取月份枚举实例的简称")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, "JAN"),
                (Month.FEBRUARY, "FEB"),
                (Month.MARCH, "MAR"),
                (Month.APRIL, "APR"),
                (Month.MAY, "MAY"),
                (Month.JUNE, "JUN"),
                (Month.JULY, "JUL"),
                (Month.AUGUST, "AUG"),
                (Month.SEPTEMBER, "SEP"),
                (Month.OCTOBER, "OCT"),
                (Month.NOVEMBER, "NOV"),
                (Month.DECEMBER, "DEC"),
            ],
        )
        def test_get_alias(self, month, expected) -> None:
            month.get_alias() == expected.lower()

        @allure.title("测试获取月份枚举实例数字表示")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, 1),
                (Month.FEBRUARY, 2),
                (Month.MARCH, 3),
                (Month.APRIL, 4),
                (Month.MAY, 5),
                (Month.JUNE, 6),
                (Month.JULY, 7),
                (Month.AUGUST, 8),
                (Month.SEPTEMBER, 9),
                (Month.OCTOBER, 10),
                (Month.NOVEMBER, 11),
                (Month.DECEMBER, 12),
            ],
        )
        def test_get_value(self, month, expected) -> None:
            assert month.get_value() == expected

        @allure.title("测试获取月份枚举类最大、最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Month.get_max_value() == 12
            assert Month.get_min_value() == 1

        @allure.title("测试判断月份枚举类是否为第一个月或者最后一个月")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, True),
                (Month.FEBRUARY, False),
                (Month.MARCH, False),
                (Month.APRIL, False),
                (Month.MAY, False),
                (Month.JUNE, False),
                (Month.JULY, False),
                (Month.AUGUST, False),
                (Month.SEPTEMBER, False),
                (Month.OCTOBER, False),
                (Month.NOVEMBER, False),
                (Month.DECEMBER, False),
            ],
        )
        def test_is_first_month(self, month, expected) -> None:
            assert month.is_first_month() == expected

        @allure.title("测试判断月份枚举类是否为最后一个月")
        @pytest.mark.parametrize(
            "month, expected",
            [
                (Month.JANUARY, False),
                (Month.FEBRUARY, False),
                (Month.MARCH, False),
                (Month.APRIL, False),
                (Month.MAY, False),
                (Month.JUNE, False),
                (Month.JULY, False),
                (Month.AUGUST, False),
                (Month.SEPTEMBER, False),
                (Month.OCTOBER, False),
                (Month.NOVEMBER, False),
                (Month.DECEMBER, True),
            ],
        )
        def test_is_last_month(self, month, expected) -> None:
            assert month.is_last_month() == expected

        @allure.title("测试判断给定月份值是否合法")
        @pytest.mark.parametrize(
            "month_value, expected",
            [
                (1, True),
                (2, True),
                (3, True),
                (4, True),
                (5, True),
                (6, True),
                (7, True),
                (8, True),
                (9, True),
                (10, True),
                (11, True),
                (12, True),
                (13, False),
                (0, False),
            ],
        )
        def test_is_valid_month(
            self,
            month_value,
            expected,
        ) -> None:
            assert Month.is_valid_month(month_value) == expected

    @allure.story("周单位枚举")
    @allure.description("周单位枚举, 表示周一到周日的枚举")
    class TestWeek:
        @allure.title("测试根据整数获取周枚举实例")
        @pytest.mark.parametrize(
            "week_num, expected",
            [
                (1, Week.MONDAY),
                (2, Week.TUESDAY),
                (3, Week.WEDNESDAY),
                (4, Week.THURSDAY),
                (5, Week.FRIDAY),
                (6, Week.SATURDAY),
                (7, Week.SUNDAY),
                (8, None),
            ],
        )
        def test_get_week_by_int(self, week_num, expected) -> None:
            assert Week.get_week(week_num) == expected

        @allure.title("测试根据中文名称获取周枚举实例")
        @pytest.mark.parametrize(
            "week_name, expected",
            [
                ("星期一", Week.MONDAY),
                ("星期二", Week.TUESDAY),
                ("星期三", Week.WEDNESDAY),
                ("星期四", Week.THURSDAY),
                ("星期五", Week.FRIDAY),
                ("星期六", Week.SATURDAY),
                ("星期日", Week.SUNDAY),
                ("星期1", Week.MONDAY),
                ("星期2", Week.TUESDAY),
                ("星期3", Week.WEDNESDAY),
                ("星期4", Week.THURSDAY),
                ("星期5", Week.FRIDAY),
                ("星期6", Week.SATURDAY),
                ("星期7", Week.SUNDAY),
                ("周一", Week.MONDAY),
                ("周二", Week.TUESDAY),
                ("周三", Week.WEDNESDAY),
                ("周四", Week.THURSDAY),
                ("周五", Week.FRIDAY),
                ("周六", Week.SATURDAY),
                ("周日", Week.SUNDAY),
                ("周1", Week.MONDAY),
                ("周2", Week.TUESDAY),
                ("周3", Week.WEDNESDAY),
                ("周4", Week.THURSDAY),
                ("周5", Week.FRIDAY),
                ("周6", Week.SATURDAY),
                ("周7", Week.SUNDAY),
                ("星期八", None),
                ("星期9", None),
                ("INVALID", None),
                pytest.param([], None, marks=pytest.mark.xfail(raises=TypeError)),
            ],
        )
        def test_get_week_by_chinese_name(self, week_name, expected) -> None:
            assert Week.get_week(week_name) == expected

        @allure.title("测试根据英文获取周枚举实例")
        @pytest.mark.parametrize(
            "week_name, expected",
            [
                ("MONDAY", Week.MONDAY),
                ("TUESDAY", Week.TUESDAY),
                ("WEDNESDAY", Week.WEDNESDAY),
                ("THURSDAY", Week.THURSDAY),
                ("FRIDAY", Week.FRIDAY),
                ("SATURDAY", Week.SATURDAY),
                ("SUNDAY", Week.SUNDAY),
            ],
        )
        def test_get_week_by_english_name(self, week_name, expected) -> None:
            assert Week.get_week(week_name) == expected

        @allure.title("测试根据dt对象获取周枚举实例")
        @pytest.mark.parametrize(
            "dt, expected",
            [
                (datetime(2024, 8, 26), Week.MONDAY),
                (datetime(2024, 8, 27), Week.TUESDAY),
                (datetime(2024, 8, 28), Week.WEDNESDAY),
                (datetime(2024, 8, 29), Week.THURSDAY),
                (datetime(2024, 8, 30), Week.FRIDAY),
                (datetime(2024, 8, 31), Week.SATURDAY),
                (datetime(2024, 9, 1), Week.SUNDAY),
            ],
        )
        def test_get_week_by_datetime(
            self,
            dt,
            expected,
        ) -> None:
            assert Week.get_week(dt) == expected

        @allure.title("测试根据英文简称获取周枚举实例")
        @pytest.mark.parametrize(
            "week_name, expected",
            [
                ("MON", Week.MONDAY),
                ("TUE", Week.TUESDAY),
                ("WED", Week.WEDNESDAY),
                ("THU", Week.THURSDAY),
                ("FRI", Week.FRIDAY),
                ("SAT", Week.SATURDAY),
                ("SUN", Week.SUNDAY),
            ],
        )
        def test_get_week_by_alias(
            self,
            week_name,
            expected,
        ) -> None:
            assert Week.get_week(week_name) == expected

        @allure.title("测试获取周枚举实例的名称")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, "MONDAY"),
                (Week.TUESDAY, "TUESDAY"),
                (Week.WEDNESDAY, "WEDNESDAY"),
                (Week.THURSDAY, "THURSDAY"),
                (Week.FRIDAY, "FRIDAY"),
                (Week.SATURDAY, "SATURDAY"),
                (Week.SUNDAY, "SUNDAY"),
            ],
        )
        def test_get_name(
            self,
            week,
            expected,
        ) -> None:
            assert week.get_name() == expected

        @allure.title("测试获取周枚举实例的中文名称")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, "星期一"),
                (Week.TUESDAY, "星期二"),
                (Week.WEDNESDAY, "星期三"),
                (Week.THURSDAY, "星期四"),
                (Week.FRIDAY, "星期五"),
                (Week.SATURDAY, "星期六"),
                (Week.SUNDAY, "星期日"),
            ],
        )
        def test_get_chinese_format_with_default_prefix(
            self,
            week,
            expected,
        ) -> None:
            assert week.get_chinese_format() == expected

        @allure.title("测试获取周枚举实例的中文名称, 使用自定义前缀")
        @pytest.mark.parametrize(
            "week, prefix, expected",
            [
                (Week.MONDAY, "周", "周一"),
                (Week.TUESDAY, "周", "周二"),
                (Week.WEDNESDAY, "周", "周三"),
                (Week.THURSDAY, "周", "周四"),
                (Week.FRIDAY, "周", "周五"),
                (Week.SATURDAY, "周", "周六"),
                (Week.SUNDAY, "周", "周日"),
            ],
        )
        def test_get_chinese_format_with_custom_prefix(
            self,
            week,
            prefix,
            expected,
        ) -> None:
            assert week.get_chinese_format(prefix=prefix) == expected

        @allure.title("测试获取周枚举实例的简称")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, "MON"),
                (Week.TUESDAY, "TUE"),
                (Week.WEDNESDAY, "WED"),
                (Week.THURSDAY, "THU"),
                (Week.FRIDAY, "FRI"),
                (Week.SATURDAY, "SAT"),
                (Week.SUNDAY, "SUN"),
            ],
        )
        def test_get_alias(
            self,
            week,
            expected,
        ) -> None:
            assert week.get_alias() == expected.lower()

        @allure.title("测试获取周枚举实例对应的calendar值")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, 0),
                (Week.TUESDAY, 1),
                (Week.WEDNESDAY, 2),
                (Week.THURSDAY, 3),
                (Week.FRIDAY, 4),
                (Week.SATURDAY, 5),
                (Week.SUNDAY, 6),
            ],
        )
        def test_get_value(
            self,
            week,
            expected,
        ) -> None:
            assert week.get_value() == expected

        @allure.title("测试获取周枚举实例的ISO8601值")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, 1),
                (Week.TUESDAY, 2),
                (Week.WEDNESDAY, 3),
                (Week.THURSDAY, 4),
                (Week.FRIDAY, 5),
                (Week.SATURDAY, 6),
                (Week.SUNDAY, 7),
            ],
        )
        def test_get_iso8601_value(
            self,
            week,
            expected,
        ) -> None:
            assert week.get_iso8601_value() == expected

        @allure.title("测试周最大值和最小值")
        def test_get_max_and_min_value(self) -> None:
            assert Week.get_max_value() == 7
            assert Week.get_min_value() == 1

        @allure.title("测试判断周枚举实例是否为一周的开始")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, True),
                (Week.TUESDAY, False),
                (Week.WEDNESDAY, False),
                (Week.THURSDAY, False),
                (Week.FRIDAY, False),
                (Week.SATURDAY, False),
                (Week.SUNDAY, False),
            ],
        )
        def test_is_first_day_of_week(self, week, expected) -> None:
            assert week.is_first_day_of_week() == expected

        @allure.title("测试判断周枚举实例是否为一周的结尾")
        @pytest.mark.parametrize(
            "week, expected",
            [
                (Week.MONDAY, False),
                (Week.TUESDAY, False),
                (Week.WEDNESDAY, False),
                (Week.THURSDAY, False),
                (Week.FRIDAY, False),
                (Week.SATURDAY, False),
                (Week.SUNDAY, True),
            ],
        )
        def test_is_last_day_of_week(self, week, expected) -> None:
            assert week.is_last_day_of_week() == expected

        @allure.title("测试判断给定周值是否合法")
        @pytest.mark.parametrize(
            "week_value, expected",
            [
                (1, True),
                (2, True),
                (3, True),
                (4, True),
                (5, True),
                (6, True),
                (7, True),
                (8, False),
                (0, False),
            ],
        )
        def test_is_valid_week(self, week_value, expected) -> None:
            assert Week.is_valid_weekday(week_value) == expected

    @allure.story("时间单位枚举")
    @allure.description("时间单位枚举, 表示时间单位的枚举, 纳秒,微秒,毫秒,秒,分钟,小时,天")
    class TestTimeUnit:
        @allure.title("测试纳秒的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.NANOSECONDS, 1, 1),
                (TimeUnit.MICROSECONDS, 1, 1000),
                (TimeUnit.MILLISECONDS, 1, 1000000),
                (TimeUnit.SECONDS, 1, 1000000000),
                (TimeUnit.MINUTES, 1, 60000000000),
                (TimeUnit.HOURS, 1, 3600000000000),
                (TimeUnit.DAYS, 1, 86400000000000),
                (TimeUnit.WEEK, 1, 604800000000000),
            ],
        )
        def test_to_nanos(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_nanos(val) == expected

        @allure.title("测试微秒的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.MICROSECONDS, 1, 1),
                (TimeUnit.MILLISECONDS, 1, 1000),
                (TimeUnit.SECONDS, 1, 1000000),
                (TimeUnit.MINUTES, 1, 60000000),
                (TimeUnit.HOURS, 1, 3600000000),
                (TimeUnit.DAYS, 1, 86400000000),
                (TimeUnit.WEEK, 1, 604800000000),
            ],
        )
        def test_to_micros(self, time_unit, val, expected) -> None:
            assert time_unit.to_micros(val) == expected

        @allure.title("测试毫秒的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.MILLISECONDS, 1, 1),
                (TimeUnit.SECONDS, 1, 1000),
                (TimeUnit.MINUTES, 1, 60000),
                (TimeUnit.HOURS, 1, 3600000),
                (TimeUnit.DAYS, 1, 86400000),
                (TimeUnit.WEEK, 1, 604800000),
            ],
        )
        def test_to_millis(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_millis(val) == expected

        @allure.title("测试秒的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.SECONDS, 1, 1),
                (TimeUnit.MINUTES, 1, 60),
                (TimeUnit.HOURS, 1, 3600),
                (TimeUnit.DAYS, 1, 86400),
                (TimeUnit.WEEK, 1, 604800),
            ],
        )
        def test_to_seconds(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_seconds(val) == expected

        @allure.title("测试分钟的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.MINUTES, 1, 1),
                (TimeUnit.HOURS, 1, 60),
                (TimeUnit.DAYS, 1, 1440),
                (TimeUnit.WEEK, 1, 10080),
            ],
        )
        def test_to_minutes(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_minutes(val) == expected

        @allure.title("测试小时的的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.HOURS, 1, 1),
                (TimeUnit.DAYS, 1, 24),
                (TimeUnit.WEEK, 1, 168),
            ],
        )
        def test_to_hours(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_hours(val) == expected

        @allure.title("测试天的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.DAYS, 1, 1),
                (TimeUnit.WEEK, 1, 7),
            ],
        )
        def test_to_days(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_days(val) == expected

        @allure.title("测试周的时间转换")
        @pytest.mark.parametrize(
            "time_unit, val, expected",
            [
                (TimeUnit.WEEK, 1, 1),
            ],
        )
        def test_to_weeks(
            self,
            time_unit,
            val,
            expected,
        ) -> None:
            assert time_unit.to_weeks(val) == expected

    @allure.story("性别枚举")
    @allure.description("性别枚举, 表示性别的枚举, 男,女")
    class TestGender:
        @allure.title("测试获取性别枚举实例")
        @pytest.mark.parametrize(
            "gender_name, expected_gender",
            [
                ("MALE", Gender.MALE),
                ("男", Gender.MALE),
                ("男的", Gender.MALE),
                ("男性", Gender.MALE),
                ("FEMALE", Gender.FEMALE),
                ("女性", Gender.FEMALE),
                ("女的", Gender.FEMALE),
                ("女", Gender.FEMALE),
                pytest.param("unknown", None, marks=pytest.mark.xfail),
            ],
        )
        def test_get_gender_by_name(self, gender_name, expected_gender) -> None:
            assert Gender.get_gender_by_name(gender_name) == expected_gender

        @allure.title("测试根据性别代码获取性别枚举实例")
        @pytest.mark.parametrize(
            "gender_code, expected_gender",
            [
                (0, Gender.FEMALE),
                (1, Gender.MALE),
                (2, Gender.FEMALE),
                (3, Gender.MALE),
            ],
        )
        def test_get_gender_by_code(self, gender_code, expected_gender) -> None:
            assert Gender.get_gender_by_code(gender_code) == expected_gender

    @allure.story("脱敏类型枚举")
    @allure.description(
        "脱敏类型枚举, 表示脱敏类型, 包括用户id,地址,身份证号,银行卡,手机号,\
            电子邮件,IPv4地址,IPv6地址,全部不显示,车牌号"
    )
    class TestDesensitizedType:
        @allure.title("测试获取枚举值描述信息")
        @pytest.mark.parametrize(
            "desensitized_type, expected_description",
            [
                (DesensitizedType.USER_ID, "用户id"),
                (DesensitizedType.ADDRESS, "地址"),
                (DesensitizedType.ID_CARD, "身份证号"),
                (DesensitizedType.BANK_CARD, "银行卡"),
                (DesensitizedType.MOBILE_PHONE, "手机号"),
                (DesensitizedType.EMAIL, "电子邮件"),
                (DesensitizedType.IPV4, "IPv4地址"),
                (DesensitizedType.IPV6, "IPv6地址"),
                (DesensitizedType.ALL_MASK, "全部不显示"),
                (DesensitizedType.CAR_LICENSE, "车牌号"),
            ],
        )
        def test_get_DesensitizedType_description(
            self,
            desensitized_type,
            expected_description,
        ) -> None:
            assert desensitized_type.get_description() == expected_description
