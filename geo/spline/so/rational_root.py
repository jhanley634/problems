#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from fractions import Fraction
from math import isclose

from hypothesis import given
import hypothesis.strategies as st


def sqrt_rational(n: Fraction, rel_tol=1e-9) -> Fraction:
    """Compute the positive root x = √n for n > 0, i.e. to solve x² = n.

    We do this with the Newton-Raphson method.
    A rational approximation is returned.
    Relative error between result squared and n shall be less than rel_tol.
    """
    assert n >= 0, n
    n = Fraction(n)
    x = Fraction(1)  # initial guess
    while not isclose(x * x, n, rel_tol=rel_tol):
        x = (x + n / x) / 2
    return x


def sqrt_float(n: float, rel_tol=1e-9) -> float:
    """Compute the positive root x = √n for n > 0, i.e. to solve x² = n.

    We do this with the Newton-Raphson method.
    Relative error between result squared and n shall be less than rel_tol.
    """
    assert n >= 0, n
    x = 1  # initial guess
    while not isclose(x * x, n, rel_tol=rel_tol):
        x = (x + n / x) / 2
    x = (x + n / x) / 2  # One more won't hurt, and it cleans up integer results.
    return x


@given(st.floats(min_value=1e-6, max_value=1e12))
def test_sqrt_float(n: float) -> None:
    assert isclose(sqrt_float(n) ** 2, n, rel_tol=1e-9)


@given(
    st.integers(min_value=1, max_value=2_000_000),
    st.integers(min_value=1, max_value=2_000_000),
)
def test_sqrt_rational(num: int, denom: int) -> None:
    n = Fraction(num, denom)
    assert isclose(sqrt_rational(n) ** 2, n, rel_tol=1e-9)


if __name__ == "__main__":
    assert sqrt_float(0) == 5.556896873712694e-163
    assert sqrt_float(1e-14) == 1e-7
    assert sqrt_float(1e-12) == 1e-6
    assert sqrt_float(1e-10) == 9.999999999999999e-06
    assert sqrt_float(1e-8) == 9.999999999999999e-05
    assert sqrt_float(1e-6) == 1e-3
    assert sqrt_float(1e-4) == 1e-2
    assert sqrt_float(1e-2) == 1e-1
    assert sqrt_float(2) == 1.414213562373095
    assert sqrt_rational(2) == Fraction(665857, 470832)

    for i in range(1, 101):
        assert sqrt_float(i**2) == i

    test_sqrt_float()
    test_sqrt_rational()
