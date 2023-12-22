#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from random import randrange
from time import time
import unittest

from tqdm import tqdm
import numpy as np


class SortedMedianTest(unittest.TestCase):
    def setUp(self, n: int = 10_000) -> None:
        self.rand = [randrange(n) for _ in range(10 * n)]

    # typical array speedup is 3x: 21.764 s / 6.993 s
    def test_sort_speed_list(self) -> None:
        t0 = time()
        for _ in tqdm(range(len(self.rand))):
            a = self.rand.copy()
            a.sort()
            a.sort(reverse=True)
            a.sort()
        print(f"\nlist sort: {time() - t0:.3f} sec")

    def test_sort_speed_array(self) -> None:
        xs = np.array(self.rand)
        t0 = time()
        for _ in tqdm(range(len(self.rand))):
            a = np.array(xs)
            a.sort()
            a = np.flip(a)
            a.sort()
            a.sort()
        print(f"\narray sort: {time() - t0:.3f} sec")
