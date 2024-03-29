# Copyright 2023 John Hanley. MIT licensed.

import pandas as pd


def bbox(df: pd.DataFrame) -> tuple[tuple[float, float], tuple[float, float]]:
    ul = df.lat.max(), df.lon.min()
    lr = df.lat.min(), df.lon.max()
    return ul, lr
