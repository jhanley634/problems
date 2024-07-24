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
    assert n >= 0, n
    x = 1  # initial guess
    while not isclose(x * x, n, rel_tol=rel_tol):
        x = (x + n / x) / 2
    return x


@given(st.floats(min_value=1e-6, max_value=1e12))
def test_sqrt_float(n: float) -> None:
    assert isclose(sqrt_float(n) ** 2, n, rel_tol=1e-9)


if __name__ == "__main__":
    assert sqrt_float(0) == 1.1113793747425387e-162
    assert sqrt_float(1e-14) == 1.0000000000043957e-07
    assert sqrt_float(1) == 1
    assert sqrt_float(2) == 1.4142135623746899
    assert sqrt_float(9) == 3.000000001396984
    assert sqrt_float(16) == 4.000000000000051
    assert sqrt_float(25) == 5.000000000053722
    assert sqrt_float(36) == 6, sqrt_float(36)
    assert sqrt_float(49) == 7.000000000000002

    test_sqrt_float()
