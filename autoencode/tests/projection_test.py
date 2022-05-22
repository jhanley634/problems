
# Copyright 2022 John Hanley. MIT licensed.
from random import seed
import unittest

import pandas as pd

from autoencode.util.projection import _hash_col, feature_subset


class TestProjection(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(('d1651215', 'name'), _hash_col('name'))

    def test_feature_subset(self):
        rows = [
            dict(a=1, b=2, c=3, d=4, e=5),
            dict(a=6, b=7, c=8, d=9, e=10),
        ]
        df = pd.DataFrame(rows)
        self.assertEqual('a b c d e', ' '.join(df.columns))

        seed(44)
        df = feature_subset(df, num_features=3)
        self.assertEqual('a d e', ' '.join(df.columns))
