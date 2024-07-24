#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from math import isclose

from hypothesis import given
import hypothesis.strategies as st


def sqrt_float(n: float, rel_tol=1e-9) -> float:
    """Compute the positive root x = √n for n > 0, i.e. to solve x² = n.

    We do this with the Newton-Raphson method.
    Relative error between result squared and n shall be less than rel_tol.
    """
    assert n>=0, n
    x = 1  # initial guess
    while not isclose(x * x, n, rel_tol=rel_tol):
        x = (x + n / x) / 2
    return x


@given(st.floats(min_value=1e-6, max_value=1e12))
def test_sqrt_float(n: float) -> None:
    assert isclose(sqrt_float(n) ** 2, n, rel_tol=1e-9)


if __name__ == "__main__":
    assert 1.1113793747425387e-162 == sqrt_float(0)
    assert 1.0000000000043957e-07==sqrt_float(1e-14)
    assert 1 == sqrt_float(1)
    assert 1.4142135623746899 == sqrt_float(2)
    assert 3.000000001396984 == sqrt_float(9)
    assert 4.000000000000051 == sqrt_float(16)
    assert 5.000000000053722 == sqrt_float(25)
    assert 6 == sqrt_float(36), sqrt_float(36)
    assert 7.000000000000002 == sqrt_float(49)

    test_sqrt_float()
