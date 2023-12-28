#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/288620/calculate-the-base-10-log-with-loops-in-java

import math
import unittest

from hypothesis import given
from hypothesis import strategies as st


def relative_error(x, y):
    if x == 0:
        x += 1e-15
    return abs(x - y) / x


def division_based_log10(x):
    assert x > 0
    return math.log(x) / math.log(10)


def log10(x: int) -> float:
    assert x > 0
    # original_x = x
    a = 0
    while x // 10 > 0:
        x //= 10
        a += 1

    r = float(a)
    frac = 0.5
    x1 = float(x)
    for i in range(55):
        x1 *= x1
        if x1 > 10:
            x1 /= 10.0
            r += frac
        frac /= 2
        # print(i, x1, "\t", r)
    return r


class Log10Test(unittest.TestCase):
    def test_log10(self):
        self.assertEqual(0, log10(1))
        self.assertEqual(1, log10(10))
        self.assertEqual(2, log10(100))
        self.assertEqual(3, math.log10(1000))
        self.assertAlmostEqual(3.0, log10(1000))
        self.assertAlmostEqual(0.47712125, log10(3))
        self.assertAlmostEqual(1.11394335, log10(13))
        self.assertAlmostEqual(1.47712125, log10(30))
        self.assertAlmostEqual(2.47712125, log10(300))
        self.assertAlmostEqual(3.30102999, log10(2000))
        self.assertAlmostEqual(3.47712125, log10(3000))
        self.assertAlmostEqual(3.60205999, log10(4000))
        self.assertAlmostEqual(3.5385737, log10(3456))

    @given(st.floats(min_value=1e-15, max_value=1e100))
    def ztest_log10_hypothesis(self, x):
        print()
        assert x > 0
        print(
            x,
            "\t",
            relative_error(math.log10(x), log10(x)),
            "\t",
            math.log10(x),
            "\t",
            division_based_log10(x),
        )
        self.assertAlmostEqual(math.log10(x), log10(x))
