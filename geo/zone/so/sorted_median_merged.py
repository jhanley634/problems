# Copyright 2024 John Hanley. MIT licensed.
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


def s_m_merged_median_index(a: list[int], b: list[int], verify: bool = True) -> Elt:
    m = None
    if verify:
        m = Merged(a, b)
        return m.merged[len(m) // 2]
