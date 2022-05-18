
from random import shuffle

# Copyright 2022 John Hanley. MIT licensed.
import pandas as pd


def feature_subset(df: pd.DataFrame, *, num_features=None, frac=1.0, keep=1):
    assert len(df.shape) == 2, df.shape

    nc = df.shape[1]  # num columns
    if num_features is None:
        num_features = int(frac * nc)
    nc = min(nc, num_features)

    cols = list(df.columns[keep:])
    shuffle(cols)
    for col in cols:
        if df.shape[1] <= nc:
            break
        df.drop(columns=[col], inplace=True)

    return df
