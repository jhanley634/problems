#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from beartype import beartype
from numpy.typing import NDArray
from scipy.interpolate import BSpline, splrep
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


@beartype
def get_df() -> pd.DataFrame:
    df = pd.DataFrame(
        columns=["stamp", "close"],
        # commodity closing prices
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


@beartype
def get_x(ser: pd.Series) -> NDArray[np.int_]:
    NANOSEC_PER_SEC = int(1e9)
    return np.array(ser.astype("int64") // NANOSEC_PER_SEC)


@beartype
def get_spline_fit(df: pd.DataFrame) -> pd.Series:
    x = get_x(df.stamp)
    tck = splrep(x, df.close, s=len(df))
    ser = pd.Series(BSpline(*tck)(x))
    # Deal with: Returning Any from function declared to return "Series[Any]"  [no-any-return]
    assert isinstance(ser, pd.Series)
    return ser


@beartype
def get_polynomial_fit(df: pd.DataFrame, order: int = 3) -> pd.Series:
    """Use e.g. order=3 for a cubic fit."""
    x = get_x(df.stamp)
    model = np.poly1d(np.polyfit(x, df.close, order))
    return pd.Series(model(x))


def main() -> None:
    df = get_df()
    df["spline"] = get_spline_fit(df)
    df["cubic"] = get_polynomial_fit(df)
    sns.lineplot(marker="o", data=df, x="stamp", y="close")
    sns.lineplot(marker="x", data=df, x="stamp", y="spline")
    sns.lineplot(marker="+", data=df, x="stamp", y="cubic")
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    main()
