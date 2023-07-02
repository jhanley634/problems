#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/76592758/any-faster-way-to-concatenate-arrays

from time import time

from numba import njit
import numpy as np


@njit(fastmath=True)
def eqn1(a):
    """Two memory ops."""
    return np.concatenate((2 * a[1:-1], 4 * a[0:2]))


@njit(fastmath=True)
def eqn2(a):
    """One memory op."""
    sys = np.empty_like(a)
    j = 0
    for i in range(1, len(a) - 1):
        eq1 = 2 * a[i]
        sys[j] = eq1
        j += 1

    for i in range(2):
        eq2 = 4 * a[i]
        sys[j] = eq2
        j += 1

    return sys


@njit(fastmath=True)
def eqn3(a):
    """One memory op."""
    sys = 2 * a
    sys[-2:] = 4 * a[0:2]
    return sys


@njit(fastmath=True)
def eqn4(a):
    """Two memory ops."""
    sys = np.empty_like(a)
    sys[:-2] = 2 * a[1:-1]
    sys[-2:] = 4 * a[0:2]
    return sys


def main(reps=10_000, size=100_000):
    arr = np.ones(size)
    # warmup
    assert arr.shape == eqn1(arr).shape
    assert arr[0] != eqn1(arr)[0]
    assert np.array_equal(eqn1(arr), eqn2(arr))
    assert np.array_equal(eqn1(arr), eqn3(arr))
    assert np.array_equal(eqn1(arr), eqn4(arr))

    for fn in [eqn1, eqn2, eqn3, eqn4]:
        elapsed = 0.0
        for _ in range(reps):
            arr = np.ones(size)
            t0 = time()
            fn(arr)
            elapsed += time() - t0

        print(f"{fn.__name__:<5} {elapsed:.3f} sec")

    t0 = time()
    for _ in range(reps):
        np.ones(size)
    print(f"init {time() - t0:.3f} sec")


if __name__ == "__main__":
    main()
