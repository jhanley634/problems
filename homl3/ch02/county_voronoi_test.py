# Copyright 2023 John Hanley. MIT licensed.

import unittest

import pandas as pd


class CountyVoronoiTest(unittest.TestCase):
    def test_serialize_df_as_list(self, verbose: bool = False) -> None:
        df = pd.DataFrame()
        df["county"] = ["L.A."] * 3 + ["San_Joaquin"] * 2
        if verbose:
            print(df.to_dict(orient="list"))

    def unused_test_find_internal(self) -> None:
        df = pd.DataFrame(
            {
                "county": ["L.A.", "L.A.", "L.A.", "San_Joaquin", "San_Joaquin"],
                "pop": [10, 20, 30, 40, 50],
                "internal": [False, True, False, False, False],
            }
        )
        df = pd.DataFrame(df[not df.internal])
        self.assertEqual(4, len(df))
