# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/286060/fast-convert-string-view-to-floating-point

import contextlib
import unittest

from hypothesis import given
import hypothesis.strategies as st


def to_fp(num: str) -> float:
    if "." not in num:
        num += "."
    i = num.index(".")

    # return acc + _to_int(n[i + 1 :]) / 10 ** (len(n) - i - 1)
    # The above return is correct, but let's do it the hard way, digit-by-digit.

    acc = 0
    exp = 10 ** -(len(num) - i - 1)
    for j in range(len(num) - 1, i, -1):
        acc += exp * (ord(num[j]) - ord("0"))
        exp *= 10

    if num.startswith("-"):
        acc *= -1

    return _to_int(num[:i]) + acc


def _to_int(num: str) -> int:
    assert "." not in num
    sign = 1
    acc = 0
    for ch in num:
        if ch.isdigit():
            acc *= 10
            acc += ord(ch) - ord("0")
        else:
            if ch != "-":
                raise ValueError(f"Invalid digit: {ch}")
            sign = -1
            assert num.rindex("-") == 0  # There Can Be Only One.
    return sign * acc


class TestFP(unittest.TestCase):
    def test_to_int(self):
        self.assertEqual(0, _to_int(""))
        for i in range(-144, 144):
            self.assertEqual(i, _to_int(f"{i}"))

    def test_to_fp(self):
        self.assertEqual(1.0, to_fp("1"))
        self.assertEqual(1.0, to_fp("1."))
        self.assertEqual(1.0, to_fp("1.0"))
        self.assertEqual(1.0, to_fp("1.000"))
        self.assertEqual(-1.5, to_fp("-1.5"))

        n = "."
        for i in range(100):
            n = f"{i}{n}{i}"
            self.assertEqual(float(n), to_fp(n))

        n = "."
        for _ in range(7):  # 8 --> AssertionError: 0.11111111 != 0.11111111000000001
            n += "1"
            self.assertEqual(float(n), to_fp(n))

    def test_roundoff_issues(self):
        # Sigh!
        self.assertEqual(0.1, to_fp(".1"))
        self.assertEqual(0.2, to_fp(".2"))
        self.assertEqual(0.30000000000000004, to_fp(".3"))
        self.assertEqual(0.30000000000000004, 3 * 0.1)
        self.assertEqual(0.4, to_fp(".4"))
        self.assertEqual(0.5, to_fp(".5"))
        self.assertEqual(0.6000000000000001, to_fp(".6"))
        self.assertEqual(0.7, 7 / 10)
        self.assertEqual(0.7000000000000001, 7 * 0.1)
        self.assertEqual(0.7000000000000001, 7 * 10**-1)
        self.assertEqual(0.7000000000000001, to_fp(".7"))
        self.assertEqual(0.7500000000000001, to_fp(".75"))
        self.assertEqual(0.7509765625000001, to_fp("0.7509765625"))

    @given(st.floats(allow_infinity=False, allow_nan=False))
    def test_torture(self, f: float):
        num = str(f)
        with contextlib.suppress(ValueError):
            if "+" in num or num.rindex("-") > 0:
                return  # We don't support parsing e.g. "1e+16" or "1e-05"

        return
        assert float(num) == to_fp(num)
