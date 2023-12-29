#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# from https://codereview.stackexchange.com/questions/288620/calculate-the-base-10-log-with-loops-in-java

from functools import partial
import math
import os
import unittest

from beartype import beartype
from hypothesis import given
from hypothesis import strategies as st

BASE = 10


def division_based_log10(x):
    assert x > 0
    return math.log(x) / math.log(BASE)


@beartype
def _places_and_remainder(base: int, x: int) -> tuple[int, int]:
    """Finds number of decimal places in x.

    Returns (places, remainder), where remainder is x % 10**places."""
    assert x > 0
    places = 0
    while x // base > 0:
        x //= base
        places += 1
    return places, x


@beartype
def log_newton(base: int, x: float, epsilon: float = 1e-14) -> float:
    """Calculates the root r = log_{base} x, to within epsilon."""
    # https://en.wikipedia.org/wiki/Natural_logarithm#High_precision
    assert x > 0
    pow_ = partial(math.pow, base)
    r = 1.0  # initial guess
    velocity = 1.0

    while abs(relative_error(pow_(r), x)) > epsilon:
        r += 2 * velocity * (x - pow_(r)) / (x + pow_(r))
        velocity *= 0.9999  # avoids stable oscillation around the true root
    return r


def relative_error(x: float, y: float) -> float:
    assert y != 0
    return abs(x - y) / y


# from https://stackoverflow.com/questions/739532/logarithm-of-a-bigdecimal
@beartype
def log_meow(base: int, x: float) -> float:
    assert x >= 1  # This is a pretty significant restriction.
    input_ = x
    result = 0.0

    while input_ > base:
        input_ /= base
        result += 1
    assert 0 < input_ <= base

    fraction = 0.5
    input_ *= input_

    # 1st conjunct is verifying that fraction is still above machine FP precision.
    while fraction + result > result and input_ > 1:
        if input_ > base:
            input_ /= base
            result += fraction
        input_ *= input_
        fraction /= 2.0

    return result


if os.getenv("HOME"):
    log2 = partial(log_newton, 2)
    log10 = partial(log_newton, 10)
else:
    log2 = partial(log_meow, 2)
    log10 = partial(log_meow, 10)


class LogTest(unittest.TestCase):
    def test_log2(self) -> None:
        self.assertAlmostEqual(0.0, log2(1.0))
        self.assertAlmostEqual(1.0, log2(2.0))
        self.assertAlmostEqual(2.0, log2(4.0))
        self.assertAlmostEqual(3.0, log2(8.0))
        self.assertAlmostEqual(3.0, math.log2(8.0))
        self.assertAlmostEqual(3.16992500, math.log2(9.0))
        self.assertAlmostEqual(3.16992500, log2(9.0))
        self.assertAlmostEqual(3.32192809, math.log2(10.0))
        self.assertAlmostEqual(3.32192809, log2(10.0))
        self.assertAlmostEqual(3.45943161, math.log2(11.0))
        self.assertAlmostEqual(3.45943161, log2(11.0))

        self.assertAlmostEqual(-1.0, math.log2(0.5))
        self.assertAlmostEqual(-1.0, log2(0.5))
        self.assertAlmostEqual(-2.0, math.log2(0.25))
        self.assertAlmostEqual(-2.0, log2(0.25))
        self.assertAlmostEqual(-2.32192809, math.log2(0.2))
        self.assertAlmostEqual(-2.32192809, log2(0.2))

    def test_log10(self) -> None:
        self.assertAlmostEqual(0.0, log10(1.0))
        self.assertAlmostEqual(1.0, log10(10.0))
        self.assertAlmostEqual(2.0, log10(100.0))
        self.assertAlmostEqual(3.0, math.log10(1000.0))
        self.assertAlmostEqual(3.0, log10(1000.0))
        self.assertAlmostEqual(0.47712125, log10(3.0))
        self.assertAlmostEqual(1.11394335, log10(13.0))
        self.assertAlmostEqual(1.47712125, log10(30.0))
        self.assertAlmostEqual(2.47712125, log10(300.0))
        self.assertAlmostEqual(3.30102999, log10(2000.0))
        self.assertAlmostEqual(3.47712125, log10(3000.0))
        self.assertAlmostEqual(3.60205999, log10(4000.0))
        self.assertAlmostEqual(3.5385737, log10(3456.0))

    def test_both(self, limit: int = 200) -> None:
        for actual, log in [
            (math.log2, log2),
            (math.log10, log10),
        ]:
            j = 1.0
            for i in map(float, range(1, limit)):
                # sequential args
                self.assertAlmostEqual(actual(i), log(i))
                self.assertAlmostEqual(actual(1 / i), log(1 / i))

                # power-of-two args
                self.assertAlmostEqual(actual(j), log(j))
                self.assertAlmostEqual(actual(1 / j), log(1 / j))
                j *= 2

    @given(st.floats(min_value=1 + 1e-15, max_value=3.4e38))
    def test_log_hypothesis(self, x):
        self.assertAlmostEqual(math.log2(x), log2(x))
        self.assertAlmostEqual(math.log10(x), log10(x))
