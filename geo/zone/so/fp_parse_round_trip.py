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

    acc = abs(_to_int(num[:i])) + _to_int(num[i + 1 :]) / 10 ** (len(num) - i - 1)
    if num.startswith("-"):
        acc *= -1
    return acc

    #   We would suffer round-off errors if we did it the hard way, digit-by-digit:
    # acc = 0
    # exp = 10 ** (len(num) - i - 1)
    # for j in range(len(num) - 1, i, -1):
    #     acc += (ord(num[j]) - ord("0")) / exp
    #     exp /= 10
    # if num.startswith("-"):
    #     acc *= -1
    # return _to_int(num[:i]) + acc


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

    def test_round_off_issues(self):
        self.assertEqual(0.1, to_fp(".1"))
        self.assertEqual(0.2, to_fp(".2"))
        self.assertEqual(0.3, to_fp(".3"))
        self.assertEqual(0.3, 3 / 10)
        self.assertEqual(0.30000000000000004, 3 * 0.1)
        self.assertEqual(0.4, to_fp(".4"))
        self.assertEqual(0.5, to_fp(".5"))
        self.assertEqual(0.6, to_fp(".6"))
        self.assertEqual(0.7, 7 / 10)
        self.assertEqual(0.7000000000000001, 7 * 0.1)
        self.assertEqual(0.7000000000000001, 7 * 10**-1)
        self.assertEqual(0.7, to_fp(".7"))
        self.assertEqual(0.75, to_fp(".75"))
        self.assertEqual(0.7509765625, to_fp("0.7509765625"))
        self.assertEqual(0.8750000000582074, to_fp("0.8750000000582074"))
        self.assertEqual(0.8750000000582075, to_fp("0.8750000000582075"))
        self.assertEqual(0.8750000000582075, to_fp("0.8750000000582076"))
        self.assertEqual(0.8750000000582077, to_fp("0.8750000000582077"))
        self.assertEqual(0.8750000000582078, to_fp("0.8750000000582078"))
        self.assertEqual(0.8750000000582079, to_fp("0.8750000000582079"))
        self.assertEqual("0x1.c00000007ffffp-1", (0.8750000000582076).hex())
        self.assertEqual("0x1.c000000080000p-1", (0.8750000000582077).hex())

    def test_hex_representation(self):
        self.assertEqual("0x1.999999999999ap-4", (0.1).hex())
        self.assertEqual("0x1.999999999999ap-3", (0.2).hex())
        self.assertEqual("0x1.3333333333333p-2", (0.3).hex())
        self.assertEqual("0x1.999999999999ap-2", (0.4).hex())
        self.assertEqual("0x1.0000000000000p-1", (0.5).hex())  # Exact!
        self.assertEqual("0x1.3333333333333p-1", (0.6).hex())
        self.assertEqual("0x1.6666666666666p-1", (0.7).hex())
        self.assertEqual("0x1.999999999999ap-1", (0.8).hex())
        self.assertEqual("0x1.ccccccccccccdp-1", (0.9).hex())
        self.assertEqual("0x1.0000000000000p+0", (1.0).hex())

        self.assertEqual("0x1.0000000000000p-2", (0.25).hex())

    @given(st.floats(allow_infinity=False, allow_nan=False))
    def test_torture(self, f: float):
        num = str(f)
        with contextlib.suppress(ValueError):
            if "+" in num or num.rindex("-") > 0:
                return  # We don't support parsing e.g. "1e+16" or "1e-05"

        assert float(num) == to_fp(num)
