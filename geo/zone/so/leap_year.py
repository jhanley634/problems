#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
#
# from https://codereview.stackexchange.com/questions/287764/leap-year-calculator-using-if-elif-and-else-only

from calendar import isleap
import unittest


def is_leap_year_instructor(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def is_leap_year_student(year: int) -> bool:
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True


class LeapYearTest(unittest.TestCase):
    def test_leap_year(self) -> None:
        for year in range(1, 2525):
            self.assertEqual(isleap(year), is_leap_year_instructor(year))
            self.assertEqual(
                is_leap_year_student(year),
                is_leap_year_instructor(year),
            )
