#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

import unittest

from pycaret.classification import (
    compare_models,
    evaluate_model,
    predict_model,
    save_model,
    setup,
)
from pycaret.datasets import get_data
import pandas as pd
import polars as pl

from geo.gpx.so.fetch_penguins import fetch_df

# 'https://raw.githubusercontent.com/simak-Olga/sem11/main/titanic.csv'
titanic_url = "https://raw.githubusercontent.com/Geoyi/Cleaning-Titanic-Data/master/titanic_original.csv"


class TestTitanic(unittest.TestCase):
    def test_verify_dst_behavior(self):
        df = fetch_df(titanic_url)
        self.assertEqual(1310, len(df))
        self.assertEqual(14, len(df.columns))


def describe_titanic_dataset() -> None:
    df = pd.read_csv(titanic_url)
    print(df.describe())
    print(df.info())

    df1 = pl.DataFrame(pd.read_csv(titanic_url))
    print(df1)
    print(df1.describe())


def main() -> None:
    data = get_data("juice")

    s = setup(data, target="Purchase", session_id=123)

    # model training and selection
    best = compare_models()

    # evaluate trained model
    evaluate_model(best)

    # predict on hold-out/test set
    pred_holdout = predict_model(best)

    # predict on new data
    new_data = data.copy().drop("Purchase", axis=1)
    predictions = predict_model(best, data=new_data)

    # save model
    save_model(best, "/tmp/best_pipeline")


if __name__ == "__main__":
    main()
