# Copyright 2024 John Hanley. MIT licensed.
from collections.abc import Callable
from operator import __ge__, __gt__, __le__, __lt__

from typing_extensions import NamedTuple
import numpy as np

from geo.zone.so.sorted_median import _monotonic


class Elt(NamedTuple):
    val: int
    idx: int
    src: int


class Merged:

    def __init__(self, a: list[int], b: list[int]):
        assert _monotonic(np.array(a)), "sorted elements, please"
        assert _monotonic(np.array(b)), "sorted elements, please"

        assert len(a) == len(set(a)), "unique elements, please"
        assert len(b) == len(set(b)), "unique elements, please"
        assert len(a + b) == len(set(a + b)), "unique elements, please"

        assert len(a + b) % 2, "odd number of elements, please"

        self.a = a
        self.b = b

        a_elts = [Elt(v, i, 0) for i, v in enumerate(a)]
        b_elts = [Elt(v, i, 1) for i, v in enumerate(b)]
        self.merged = sorted(a_elts + b_elts)

    def __len__(self) -> int:
        return len(self.merged)


def pick_one(a_elt: Elt, b_elt: Elt, op: Callable) -> Elt:
    if op(a_elt.val, b_elt.val):
        return a_elt
    return b_elt


def s_m_merged_median_index(a: list[int], b: list[int], verify: bool = True) -> Elt:

    assert len(a) > 0
    assert len(b) > 0
    assert len(a) < len(b)  # w.l.o.g.

    gt = None  # ground truth
    if True or verify:
        gt = Merged(a, b)
        # return gt.merged[len(gt) // 2]

    assert gt.merged[0] == pick_one(
        Elt(a[0], 0, 0),
        Elt(b[0], 0, 1),
        __lt__,
    )
    assert gt.merged[-1] == pick_one(
        Elt(a[-1], len(a) - 1, 0),
        Elt(b[-1], len(b) - 1, 1),
        __gt__,
    )

    # target index is in the middle of the merged list
    tgt_idx = (len(a) + len(b)) // 2

    # key observation here is that a_idx + b_idx == merged_idx

    a_lo = 0
    b_lo = 0
    m_lo = a_lo + b_lo

    a_hi = len(a)
    b_hi = len(b)
    m_hi = a_hi + b_hi

    while m_lo < m_hi:
        m_delta = (m_hi - m_lo) // 2
        a_delta = (a_hi - a_lo) // 2
        b_delta = (b_hi - b_lo) // 2

        a_mid_elt = Elt(a[a_lo + a_delta], a_lo + a_delta, 0)
        b_mid_elt = Elt(b[b_lo + b_delta], b_lo + b_delta, 1)

        a_elt = Elt(a[a_idx], a_idx, 0)
        b_elt = Elt(b[b_idx], b_idx, 1)

        m_lo = a_lo + b_lo
        m_hi = a_hi + b_hi
