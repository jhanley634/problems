#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/288620/calculate-the-base-10-log-with-loops-in-java

from functools import partial
import math
import unittest

from hypothesis import given
from hypothesis import strategies as st


def relative_error(x, y):
    assert x > 0
    assert y != 0
    return abs(x - y) / y


BASE = 10


def division_based_log10(x):
    assert x > 0
    return math.log(x) / math.log(BASE)


def _places_and_remainder(base: int, x: int) -> tuple[int, int]:
    """Finds number of decimal places in x.

    Returns (places, remainder), where remainder is x % 10**places."""
    assert x > 0
    places = 0
    while x // base > 0:
        x //= base
        places += 1
    return places, x


def log(base: int, x: int, epsilon: float = 1e-14) -> float:
    """Calculates the root r = log_{base} x, to within epsilon."""
    # https://en.wikipedia.org/wiki/Natural_logarithm#High_precision
    assert x > 0
    pow = partial(math.pow, base)
    r = 1.0  # initial guess
    velocity = 1.0

    while abs(relative_error(pow(r), x)) > epsilon:
        r += 2 * velocity * (x - pow(r)) / (x + pow(r))
        velocity *= 0.9999  # avoids stable oscillation around the true root
    return r


log2 = partial(log, 2)
log10 = partial(log, 10)


class Log10Test(unittest.TestCase):
    def test_log2(self):
        # self.assertEqual(0, log2(1))
        self.assertAlmostEqual(1.0, log2(2))
        self.assertAlmostEqual(2.0, log2(4))
        self.assertAlmostEqual(3.0, log2(8))
        self.assertAlmostEqual(3.0, math.log2(8))
        self.assertAlmostEqual(3.16992500, math.log2(9))
        self.assertAlmostEqual(3.16992500, log2(9))
        self.assertAlmostEqual(3.32192809, math.log2(10))
        self.assertAlmostEqual(3.32192809, log2(10))
        self.assertAlmostEqual(3.45943161, math.log2(11))
        self.assertAlmostEqual(3.45943161, log2(11))

        self.assertAlmostEqual(-1.0, math.log2(0.5))
        self.assertAlmostEqual(-1.0, log2(0.5))
        self.assertAlmostEqual(-2.0, math.log2(0.25))
        self.assertAlmostEqual(-2.0, log2(0.25))
        self.assertAlmostEqual(-2.32192809, math.log2(0.2))
        self.assertAlmostEqual(-2.32192809, log2(0.2))

    def test_log10(self):
        self.assertAlmostEqual(0.0, log10(1))
        self.assertAlmostEqual(1.0, log10(10))
        self.assertAlmostEqual(2.0, log10(100))
        self.assertAlmostEqual(3.0, math.log10(1000))
        self.assertAlmostEqual(3.0, log10(1000))
        self.assertAlmostEqual(0.47712125, log10(3))
        self.assertAlmostEqual(1.11394335, log10(13))
        self.assertAlmostEqual(1.47712125, log10(30))
        self.assertAlmostEqual(2.47712125, log10(300))
        self.assertAlmostEqual(3.30102999, log10(2000))
        self.assertAlmostEqual(3.47712125, log10(3000))
        self.assertAlmostEqual(3.60205999, log10(4000))
        self.assertAlmostEqual(3.5385737, log10(3456))

    @given(st.floats(min_value=1e-15, max_value=3.4e38))
    def test_log10_hypothesis(self, x):
        self.assertAlmostEqual(math.log2(x), log2(x))
        self.assertAlmostEqual(math.log10(x), log10(x))
