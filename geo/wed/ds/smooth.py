#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=["stamp", "close"],
        data=[
            ["2023-11-01 16:00", 110],
            ["2023-12-01 16:00", 110],
            ["2024-01-02 16:00", 110],
            ["2024-01-03 16:00", 110],
            ["2024-01-04 16:00", 110],
            ["2024-01-05 16:00", 120],
            ["2024-01-08 16:00", 120],
            ["2024-01-09 16:00", 120],
            ["2024-02-01 16:00", 120],
            ["2024-03-01 16:00", 120],
            ["2024-04-01 16:00", 120],
        ],
    )
    df["stamp"] = pd.to_datetime(df["stamp"])
    return df


def get_polynomial_fit(df: pd.DataFrame, order=3) -> pd.Series:
    """Use e.g. order=3 for a cubic fit."""
    NANOSEC_PER_SEC = 1e9
    x = df.stamp.astype("int64") // NANOSEC_PER_SEC
    model = np.poly1d(np.polyfit(x, df.close, order))
    return pd.Series(model(x))


def main():
    df = get_df()
    df["fit"] = get_polynomial_fit(df)
    sns.lineplot(marker="o", data=df, x="stamp", y="close")
    sns.lineplot(marker="x", data=df, x="stamp", y="fit")
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()
