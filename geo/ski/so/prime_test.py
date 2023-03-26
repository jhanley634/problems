from math import sqrt
import unittest

from numba import jit
import sympy


def is_prime(n: int) -> bool:
    return _find_divisor(n) == 1


@jit
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


_find_divisor(999_999)  # force a compile


class PrimeTest(unittest.TestCase):
    def test_is_prime(self, verbose=False):
        count = 0
        for n in range(2, 1_000_000):
            divisor = _find_divisor(n)
            if divisor > 1:
                count += 1
                if verbose:
                    dividend = n / divisor
                    self.assertEqual(n, divisor * dividend)
                    self.assertEqual(0, n % divisor)
                    self.assertEqual(0, n % dividend)
                    self.assertEqual(dividend, int(dividend))
            else:
                self.assertTrue(sympy.isprime(n))
                if verbose:
                    print(n, end="  ")

        self.assertEqual(921_500, count)  # 90_406, 8_769

        with self.assertRaises(AssertionError):
            _find_divisor(0)
