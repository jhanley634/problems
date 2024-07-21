# Copyright 2024 John Hanley. MIT licensed.
import unittest

import pandas as pd


class JoinTest(unittest.TestCase):
    def setUp(self) -> None:
        self.df_age = pd.DataFrame(
            [
                {"name": "Alice", "age": 21},
                {"name": "Bob", "age": 22},
                {"name": "Carol"},
                {"name": "David", "age": 24},
            ]
        )

    def test_one_to_one_join(self) -> None:
        """Demo of JOINing one relation against another."""
        df_email = pd.DataFrame(
            [
                {"name": "Alice", "email": "alice@y.com"},
                {"name": "Bob"},
                {"name": "Carol", "email": "carol@y.com"},
                {"name": "David", "email": "david@y.com"},
            ]
        )
        joined = self.df_age.merge(df_email, on="name", how="outer")
        self.assertEqual(
            """
| name   |   age | email       |
|:-------|------:|:------------|
| Alice  |    21 | alice@y.com |
| Bob    |    22 | nan         |
| Carol  |   nan | carol@y.com |
| David  |    24 | david@y.com |
""".strip(),
            joined.to_markdown(index=False),
        )

    def test_one_to_many_join(self) -> None:
        df_email = pd.DataFrame(
            [
                {"name": "Carol", "email": "carol@y.com"},
                {"name": "David", "email": "dave@w.com"},
                {"name": "David", "email": "david@x.com"},
                {"name": "David", "email": "davey@y.com"},
                {"name": "Eve", "email": "evelynn@x.com"},
                {"name": "Eve", "email": "eve@y.com"},
            ]
        )
        joined = self.df_age.merge(df_email, on="name", how="outer")
        self.assertEqual(
            """
| name   |   age | email         |
|:-------|------:|:--------------|
| Alice  |    21 | nan           |
| Bob    |    22 | nan           |
| Carol  |   nan | carol@y.com   |
| David  |    24 | dave@w.com    |
| David  |    24 | david@x.com   |
| David  |    24 | davey@y.com   |
| Eve    |   nan | evelynn@x.com |
| Eve    |   nan | eve@y.com     |
""".strip(),
            joined.to_markdown(index=False),
        )
