#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from random import randrange

from beartype import beartype
from sortedcontainers import SortedList
import numpy as np

from geo.zone.so.sorted_median import _monotonic


@beartype
def argmax(vec: list[int]) -> int:
    return vec.index(max(vec))


@beartype
def median_of_k_sorted_vectors(
    *vecs: list[int],
    verify: bool = False,
) -> tuple[int, int]:
    """Given K sorted vectors containing a total of N numbers, returns the
    index of the median, as (vec_idx, idx), with vec_idx in range(k).

    There shall be N // 2 numbers less than or equal to the median,
    and N // 2 numbers greater than or equal to the median.
    We require that N shall be odd, so the median is present in the input.
    That is, we do not perform any averaging.
    """
    if verify:
        for vec in vecs:
            assert _monotonic(np.array(vec))
            assert vec == sorted(vec)

    return _median_k([SortedList(vec) for vec in vecs])


def _median_k(vecs: list[SortedList]) -> tuple[int, int]:

    n = sum(map(len, vecs))
    if n % 2 == 0:
        raise ValueError(
            f"N must be odd, but it was {n}. Number of vectors was {len(vecs)}."
        )
    # There are now n candidate index positions.

    # target = n // 2 # We must eliminate this many lo, and this many hi values.

    # [lo, hi) indexes for each vector
    # The median definitely lies within one of those K ranges.
    rng = [[0, len(vec)] for vec in vecs]

    lo_hi = 0  # Start out working on the low part of each range.

    def feasible() -> bool:
        """For a (v, cut) proposal, will return True if we can discard enough values
        to make the median lie within the remaining ranges.
        """
        discarded_lo = discarded_hi = 0
        val = vecs[v][cut]
        if lo_hi == 0:
            discarded_hi = rng[v][1] - cut  # number of discarded values above the cut
            for i, vec in enumerate(vecs):
                if i != v:
                    j = vec.bisect_right(val)
                    discarded_lo += j - rng[i][0]
            return discarded_lo >= discarded_hi
        discarded_lo = cut - rng[v][0]  # number of discarded values below the cut
        for i, vec in enumerate(vecs):
            if i != v:
                j = vec.bisect_left(val)
                discarded_hi += rng[i][1] - j
        return discarded_hi >= discarded_lo

    def trim() -> None:
        """Actually trim the ranges, based on a known feasible proposal."""
        discarded_lo = discarded_hi = 0
        val = vecs[v][cut]
        if lo_hi == 0:
            discarded_hi = rng[v][1] - cut
            rng[v][1] = cut - 1
            for i, vec in enumerate(vecs):
                if i != v and discarded_lo < discarded_hi:
                    lo = rng[i][0]
                    j = vec.bisect_right(val)
                    excess = discarded_lo + (j - lo) - discarded_hi
                    if excess > 0:
                        j += excess
                    discarded_lo += j - lo
                    rng[i][0] = j
        else:
            discarded_lo = cut - rng[v][0]
            rng[v][0] = cut
            for i, vec in enumerate(vecs):
                if i != v and discarded_hi < discarded_lo:
                    hi = rng[i][1]
                    j = vec.bisect_left(val)
                    excess = discarded_hi + (hi - j) - discarded_lo
                    if excess > 0:
                        j -= excess
                    discarded_hi += hi - j
                    rng[i][1] = j

    while n > 1:
        sizes = [hi - lo for lo, hi in rng]
        n = sum(sizes)
        print(n, sizes)

        # Pick out the biggest vector, the one most likely to contain the median.
        v = argmax(sizes)
        # Propose to discard all values from vecs[v]
        # that are either above or below the value at the cut index.
        cut = randrange(rng[v][0], rng[v][1] + 1)

        if feasible():
            trim()

        lo_hi = 1 - lo_hi  # toggle

    sizes = [hi - lo for lo, hi in rng]
    assert sum(sizes) == 1
    answer: tuple[int, int] = 0, 0

    for i, (lo, hi) in enumerate(rng):
        if hi - lo == 1:
            assert isinstance(vecs[i], SortedList)
            val = vecs[i][lo]
            assert isinstance(val, int)
            answer = i, val
    return answer
