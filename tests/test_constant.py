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

import pytest

from .context import DesensitizedType, Gender, Month, Quarter, TimeUnit, Week


class TestQuarterObject:
    def __init__(self, month: int) -> None:
        self.month = month


class TestQuarter:
    @classmethod
    def test_get_quarter_with_incorrect_arguments(cls) -> None:
        incorrect_obj = TestQuarterObject(13)
        with pytest.raises(KeyError):
            Quarter.get_quarter(incorrect_obj)

    @classmethod
    def test_get_chinese_format(cls) -> None:
        assert Quarter.Q1.get_chinese_format() == "第一季度"
        assert Quarter.Q2.get_chinese_format() == "第二季度"
        assert Quarter.Q3.get_chinese_format() == "第三季度"
        assert Quarter.Q4.get_chinese_format() == "第四季度"

    @classmethod
    def test_get_name(cls) -> None:
        assert Quarter.Q1.get_name() == "Q1"
        assert Quarter.Q2.get_name() == "Q2"
        assert Quarter.Q3.get_name() == "Q3"
        assert Quarter.Q4.get_name() == "Q4"


class TestConstant:
    @classmethod
    def test_get_DesensitizedType_description(cls) -> None:
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

    @classmethod
    def test_get_gender(cls) -> None:
        assert Gender.MALE == Gender.get_gender_by_code(1)
        assert Gender.FEMALE == Gender.get_gender_by_code(2)

        assert Gender.get_gender_by_name("MALE") == Gender.MALE
        assert Gender.get_gender_by_name("男") == Gender.MALE
        assert Gender.get_gender_by_name("男的") == Gender.MALE
        assert Gender.get_gender_by_name("男性") == Gender.MALE

        assert Gender.get_gender_by_name("FEMALE") == Gender.FEMALE
        assert Gender.get_gender_by_name("女性") == Gender.FEMALE
        assert Gender.get_gender_by_name("女的") == Gender.FEMALE
        assert Gender.get_gender_by_name("女") == Gender.FEMALE

        with pytest.raises(ValueError):
            Gender.get_gender_by_name("unknown")


class TestMonth:
    @classmethod
    def test_get_month_by_number(cls) -> None:
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
        assert Month.get_month(13) is None

    @classmethod
    def test_get_month_by_name(cls) -> None:
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
        assert Month.get_month("13月") is None

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
        assert Month.get_month("13月") is None

    @classmethod
    def test_get_month_incorrect(cls) -> None:
        with pytest.raises(TypeError):
            Month.get_month([])

    @classmethod
    def test_month_get_last_day(cls) -> None:
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

    @classmethod
    def test_get_value(cls) -> None:
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

    @classmethod
    def test_get_natest_get_chinese_format(cls) -> None:
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

    @classmethod
    def test_get_name(cls) -> None:
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

    @classmethod
    def test_get_alias(cls) -> None:
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


class TestTimeUnits:
    @classmethod
    def test_convert(cls) -> None:
        assert TimeUnit.NANOSECONDS.to_nanos(1) == 1

        assert TimeUnit.MICROSECONDS.to_micros(1) == 1
        assert TimeUnit.MICROSECONDS.to_nanos(1) == 1000

        assert TimeUnit.MILLISECONDS.to_millis(1) == 1
        assert TimeUnit.MILLISECONDS.to_micros(1) == 1000
        assert TimeUnit.MILLISECONDS.to_nanos(1) == 1000000

        assert TimeUnit.SECONDS.to_seconds(1) == 1
        assert TimeUnit.SECONDS.to_millis(1) == 1000
        assert TimeUnit.SECONDS.to_micros(1) == 1000000
        assert TimeUnit.SECONDS.to_nanos(1) == 1000000000

        assert TimeUnit.MINUTES.to_minutes(1) == 1
        assert TimeUnit.MINUTES.to_seconds(1) == 60
        assert TimeUnit.MINUTES.to_millis(1) == 60000
        assert TimeUnit.MINUTES.to_micros(1) == 60000000
        assert TimeUnit.MINUTES.to_nanos(1) == 60000000000

        assert TimeUnit.HOURS.to_hours(1) == 1
        assert TimeUnit.HOURS.to_minutes(1) == 60
        assert TimeUnit.HOURS.to_seconds(1) == 3600
        assert TimeUnit.HOURS.to_millis(1) == 3600000
        assert TimeUnit.HOURS.to_micros(1) == 3600000000
        assert TimeUnit.HOURS.to_nanos(1) == 3600000000000

        assert TimeUnit.DAYS.to_days(1) == 1
        assert TimeUnit.DAYS.to_hours(1) == 24
        assert TimeUnit.DAYS.to_minutes(1) == 1440
        assert TimeUnit.DAYS.to_seconds(1) == 86400
        assert TimeUnit.DAYS.to_millis(1) == 86400000
        assert TimeUnit.DAYS.to_micros(1) == 86400000000
        assert TimeUnit.DAYS.to_nanos(1) == 86400000000000


class TestWeek:
    @classmethod
    def test_get_week_by_int(cls) -> None:
        assert Week.get_week(1) == Week.MONDAY
        assert Week.get_week(2) == Week.TUESDAY
        assert Week.get_week(3) == Week.WEDNESDAY
        assert Week.get_week(4) == Week.THURSDAY
        assert Week.get_week(5) == Week.FRIDAY
        assert Week.get_week(6) == Week.SATURDAY
        assert Week.get_week(7) == Week.SUNDAY
        assert Week.get_week(8) is None

    @classmethod
    def test_get_week_by_name(cls) -> None:
        assert Week.get_week("星期一") == Week.MONDAY
        assert Week.get_week("星期二") == Week.TUESDAY
        assert Week.get_week("星期三") == Week.WEDNESDAY
        assert Week.get_week("星期四") == Week.THURSDAY
        assert Week.get_week("星期五") == Week.FRIDAY
        assert Week.get_week("星期六") == Week.SATURDAY
        assert Week.get_week("星期日") == Week.SUNDAY
        assert Week.get_week("8") is None

        assert Week.get_week("周一") == Week.MONDAY
        assert Week.get_week("周二") == Week.TUESDAY
        assert Week.get_week("周三") == Week.WEDNESDAY
        assert Week.get_week("周四") == Week.THURSDAY
        assert Week.get_week("周五") == Week.FRIDAY
        assert Week.get_week("周六") == Week.SATURDAY
        assert Week.get_week("周日") == Week.SUNDAY
        assert Week.get_week("8") is None

        assert Week.get_week("星期1") == Week.MONDAY
        assert Week.get_week("星期2") == Week.TUESDAY
        assert Week.get_week("星期3") == Week.WEDNESDAY
        assert Week.get_week("星期4") == Week.THURSDAY
        assert Week.get_week("星期5") == Week.FRIDAY
        assert Week.get_week("星期6") == Week.SATURDAY
        assert Week.get_week("星期7") == Week.SUNDAY
        assert Week.get_week("8") is None

        assert Week.get_week("周1") == Week.MONDAY
        assert Week.get_week("周2") == Week.TUESDAY
        assert Week.get_week("周3") == Week.WEDNESDAY
        assert Week.get_week("周4") == Week.THURSDAY
        assert Week.get_week("周5") == Week.FRIDAY
        assert Week.get_week("周6") == Week.SATURDAY
        assert Week.get_week("周7") == Week.SUNDAY
        assert Week.get_week("周8") is None

    @classmethod
    def test_get_week_incorrect(cls) -> None:
        with pytest.raises(TypeError):
            Week.get_week([321312])

    @classmethod
    def test_get_value(cls) -> None:
        assert Week.MONDAY.get_value() == calendar.MONDAY
        assert Week.TUESDAY.get_value() == calendar.TUESDAY
        assert Week.WEDNESDAY.get_value() == calendar.WEDNESDAY
        assert Week.THURSDAY.get_value() == calendar.THURSDAY
        assert Week.FRIDAY.get_value() == calendar.FRIDAY
        assert Week.SATURDAY.get_value() == calendar.SATURDAY
        assert Week.SUNDAY.get_value() == calendar.SUNDAY

    @classmethod
    def test_get_chinese_format(cls) -> None:
        assert Week.MONDAY.get_chinese_format() == "星期一"
        assert Week.TUESDAY.get_chinese_format() == "星期二"
        assert Week.WEDNESDAY.get_chinese_format() == "星期三"
        assert Week.THURSDAY.get_chinese_format() == "星期四"
        assert Week.FRIDAY.get_chinese_format() == "星期五"
        assert Week.SATURDAY.get_chinese_format() == "星期六"
        assert Week.SUNDAY.get_chinese_format() == "星期日"

    @classmethod
    def test_get_name(cls) -> None:
        assert Week.MONDAY.get_name() == "MONDAY"
        assert Week.TUESDAY.get_name() == "TUESDAY"
        assert Week.WEDNESDAY.get_name() == "WEDNESDAY"
        assert Week.THURSDAY.get_name() == "THURSDAY"
        assert Week.FRIDAY.get_name() == "FRIDAY"
        assert Week.SATURDAY.get_name() == "SATURDAY"
        assert Week.SUNDAY.get_name() == "SUNDAY"

    @classmethod
    def test_get_alias(cls) -> None:
        assert Week.MONDAY.get_alias() == "MON".lower()
        assert Week.TUESDAY.get_alias() == "TUE".lower()
        assert Week.WEDNESDAY.get_alias() == "WED".lower()
        assert Week.THURSDAY.get_alias() == "THU".lower()
        assert Week.FRIDAY.get_alias() == "FRI".lower()
        assert Week.SATURDAY.get_alias() == "SAT".lower()
        assert Week.SUNDAY.get_alias() == "SUN".lower()

    @classmethod
    def test_get_iso8601_value(cls) -> None:
        assert Week.MONDAY.get_iso8601_value() == 1
        assert Week.TUESDAY.get_iso8601_value() == 2
        assert Week.WEDNESDAY.get_iso8601_value() == 3
        assert Week.THURSDAY.get_iso8601_value() == 4
        assert Week.FRIDAY.get_iso8601_value() == 5
        assert Week.SATURDAY.get_iso8601_value() == 6
        assert Week.SUNDAY.get_iso8601_value() == 7
