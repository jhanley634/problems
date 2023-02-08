# Copyright 2023 John Hanley. MIT licensed.
import unittest

import numpy as np
import pandas as pd

from .central_tendency import ct_mean, ct_median


class CentralTendencyTest(unittest.TestCase):
    def test_measures(self):
        nums = [1, 2, 6]
        self.assertEqual(3, ct_mean(nums))
        self.assertEqual(2, ct_median(nums))

        x = np.array(nums)
        self.assertEqual(3, ct_mean(x))
        self.assertEqual(2, ct_median(x))

        df = pd.DataFrame({"x": nums})
        self.assertEqual(3, ct_mean(df.x))
        self.assertEqual(2, ct_median(df.x))
