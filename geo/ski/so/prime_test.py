# Copyright 2023 John Hanley. MIT licensed.

from math import sqrt
import unittest

from hypothesis import given
from numba import int_, jit
import hypothesis.strategies as st
import sympy

assert int_
assert jit


def is_prime(n: int) -> bool:
    return int(_find_divisor(n)) == 1


# @jit(int_(int_))  # type: ignore [misc]
def _find_divisor(n: int) -> int:
    assert n >= 2
    if n == 2:
        return 1
    if n & 1 == 0:
        return 2
    root = int(sqrt(n))

    for i in range(3, root + 1, 2):
        if n % i == 0:
            return i
    return 1


# @jit  # (int_(int_))
def _square(n: int) -> int:
    return n**2


LARGE = 1_000_000
assert _find_divisor(LARGE - 1) == 3  # force a compile


class PrimeTest(unittest.TestCase):
    def test_square(self) -> None:
        self.assertEqual(9, _square(3))

    def test_is_prime(self, verbose: bool = False) -> None:
        count = 0
        for n in range(2, LARGE):
            divisor = _find_divisor(n)
            if divisor > 1:
                count += 1
            else:
                self.assertTrue(sympy.isprime(n))  # type: ignore [no-untyped-call]
                if verbose:  # pragma: no cover
                    print(n, end="  ")

        self.assertEqual(921_500, count)  # 90_406, 8_769

        with self.assertRaises(AssertionError):
            _find_divisor(0)

    @given(st.integers(min_value=2, max_value=100 * LARGE))
    def test_is_prime_hypo(self, n: int) -> None:
        self.assertEqual(is_prime(n), sympy.isprime(n))  # type: ignore [no-untyped-call]

        divisor = _find_divisor(n)
        dividend = n / divisor
        self.assertEqual(n, divisor * dividend)
        self.assertEqual(0, n % divisor)
        self.assertEqual(0, n % dividend)
        self.assertEqual(dividend, int(dividend))
