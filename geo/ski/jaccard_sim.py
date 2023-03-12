# Copyright 2023 John Hanley. MIT licensed.
# https://stackoverflow.com/questions/75714434/computing-jaccard-similarity-between-dataframe-columns
import unittest

import pandas as pd


class JaccardTest(unittest.TestCase):
    def test_jaccard(self):
        df = _get_example_data()
        self.assertAlmostEqual(2 / 3, jaccard_similarity(df.cancer, df.thyroid))
        self.assertAlmostEqual(3 / 7, jaccard_similarity(df.cancer, df.allergy))


def jaccard_similarity(
    a: pd.Series,
    b: pd.Series,
):
    assert len(a) == len(b)  # must be a pair of columns from same dataframe
    total_size = len(a) + len(b)
    intersection = (a == b).sum()
    return intersection / (total_size - intersection)


def _get_example_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "patient": ["P1", "P2", "P3", "P4", "P5"],
            "cancer": [1, 1, 0, 0, 0],
            "thyroid": [1, 0, 0, 0, 0],
            "allergy": [0, 0, 0, 0, 0],
        }
    )
