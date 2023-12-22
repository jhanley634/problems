#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from random import randrange
from time import time
import unittest

import numpy as np


class SortedMedianTest(unittest.TestCase):
    def setUp(self, n: int = 10_000) -> None:
        self.xs = [randrange(n) for _ in range(n)]

    # typical array speedup is 3x: 12.906 s / 4.376 s == 2.95
    def test_sort_speed_list(self) -> None:
        t0 = time()
        for _ in range(len(self.xs)):
            self.xs.copy().sort()
        print(f"\nlist sort: {time() - t0:.3f} sec")

    def test_sort_speed_array(self) -> None:
        xs = np.array(self.xs)
        t0 = time()
        for _ in range(len(self.xs)):
            np.array(xs).sort()
        print(f"\narray sort: {time() - t0:.3f} sec")
