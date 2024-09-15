#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


import unittest

from beartype import beartype

from geo.zone.so.sorted_medians import median_of_k_sorted_vectors


@beartype
class SortedMediansTest(unittest.TestCase):
    def test_odd_n(self) -> None:
        with self.assertRaises(ValueError):
            median_of_k_sorted_vectors([1, 2], [3, 4, 5, 6])

        # median_of_k_sorted_vectors([1, 2], [3, 4, 5], verify=True)
