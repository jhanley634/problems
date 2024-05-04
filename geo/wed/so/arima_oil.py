#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291850/forecast-volatility-of-monthly-crude-oil-prices-using-garch
from pathlib import Path
import datetime as dt

from numpy import log
from pmdarima.arima.utils import ndiffs
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def get_oil_df(id_: str = "DCOILWTICO", since_year: int = 2010) -> pd.DataFrame:
    today = dt.datetime.today()
    temp = Path("/tmp/k")
    csv = temp / f"{id_}.csv"
    if not csv.exists():
        base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        url = base_url + f"?id={id_}&cosd=1987-01-01&coed={today}"
        resp = requests.get(url)
        resp.raise_for_status()
        csv.write_text(resp.text)
    df = pd.read_csv(csv, parse_dates=["DATE"], index_col="DATE")
    df = df.rename(columns={id_: "price"})
    df = df[df.price != "."]
    df = df[df.index.year >= since_year]
    return pd.DataFrame(
        {"price": df.price.astype(float)},
        pd.to_datetime(df.reset_index().DATE.rename("date")),
    )


def main() -> None:
    df = get_oil_df().asfreq("D")
    print(df)
    model = ARIMA(df, order=(1, 0, 0))
    fit = model.fit()
    print(model)
    print(fit.summary())

    result = adfuller(df.price.dropna())
    print("ADF Statistic: %f" % result[0])
    p_value = result[1]
    assert 0.05 < 0.17 < p_value, p_value

    y = df.price.dropna()
    assert 1 == ndiffs(y, test="adf") == ndiffs(y, test="kpss") == ndiffs(y, test="pp")

    plot(df)


def plot(df):
    df["value"] = df.price
    plt.rcParams.update({"figure.figsize": (9, 7), "figure.dpi": 120})

    # Import data
    df1 = pd.read_csv(
        "https://raw.githubusercontent.com/selva86/datasets/master/wwwusage.csv",
        names=["value"],
        header=0,
    )

    # Original Series
    fig, axes = plt.subplots(3, 2, sharex=True)
    axes[0, 0].plot(df.value)
    axes[0, 0].set_title("Original Series")
    plot_acf(df.value, ax=axes[0, 1])

    # 1st Differencing
    axes[1, 0].plot(df.value.diff())
    axes[1, 0].set_title("1st Order Differencing")
    plot_acf(df.value.diff().dropna(), ax=axes[1, 1])

    # 2nd Differencing
    axes[2, 0].plot(df.value.diff().diff())
    axes[2, 0].set_title("2nd Order Differencing")
    plot_acf(df.value.diff().diff().dropna(), ax=axes[2, 1])

    plt.show()


if __name__ == "__main__":
    main()
