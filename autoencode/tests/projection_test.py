
# Copyright 2022 John Hanley. MIT licensed.
import unittest

import pandas as pd

from autoencode.util.projection import feature_subset


class TestProjection(unittest.TestCase):

    def test_feature_subset(self):
        rows = [
            dict(a=1, b=2, c=3, d=4, e=5),
            dict(a=6, b=7, c=8, d=9, e=10),
        ]
        df = pd.DataFrame(rows)
        self.assertEqual('a b c d e', ' '.join(df.columns))

        df = feature_subset(df, num_features=3)
        self.assertEqual('a b c', ' '.join(df.columns))
