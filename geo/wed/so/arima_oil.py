#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291850/forecast-volatility-of-monthly-crude-oil-prices-using-garch
# with material from https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python
from pathlib import Path
import datetime as dt

from pmdarima.arima.utils import ndiffs
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA, ARIMAResultsWrapper
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pmdarima as pm
import requests


def get_oil_df(id_: str = "DCOILWTICO", since_year: int = 2010) -> pd.DataFrame:
    today = dt.datetime.now(dt.UTC).date()
    temp = Path("/tmp")
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
        df.reset_index().DATE.rename("date"),
    )


def main() -> None:
    df = get_oil_df().asfreq("D")
    model = ARIMA(df, order=(1, 0, 0))
    fit = model.fit()
    assert isinstance(fit, ARIMAResultsWrapper), type(fit)
    print(model)
    print(fit.summary())

    result = adfuller(df.price.dropna())
    print(f"ADF Statistic: {result[0]:f}")
    p_value = result[1]
    assert 0.17 < p_value, p_value

    y = df.price.dropna()
    assert 1 == ndiffs(y, test="adf") == ndiffs(y, test="kpss") == ndiffs(y, test="pp")

    df["value"] = df.price
    # a barrel cost -$37 on 20th April 2020
    df["value"] = np.array([max(8, p) for p in df.price])
    # _plot_acf(df)
    # _plot_residuals(fit)


def _plot_differences(df: pd.DataFrame) -> None:
    plt.rcParams.update({"figure.figsize": (9, 7), "figure.dpi": 120})

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


def _plot_pacf(df: pd.DataFrame) -> None:
    # PACF plot of 1st differenced series
    plt.rcParams.update({"figure.figsize": (9, 3), "figure.dpi": 120})

    fig, axes = plt.subplots(1, 2, sharex=True)
    axes[0].plot(df.value.diff())
    axes[0].set_title("1st Differencing")
    axes[1].set(ylim=(0, 5))
    plot_pacf(df.value.diff().dropna(), ax=axes[1])

    plt.show()


def _plot_acf(df: pd.DataFrame) -> None:
    plt.rcParams.update({"figure.figsize": (9, 3), "figure.dpi": 120})
    fig, axes = plt.subplots(1, 2, sharex=True)
    axes[0].plot(df.value.diff())
    axes[0].set_title("1st Differencing")
    axes[1].set(ylim=(0, 1.2))
    plot_acf(df.value.diff().dropna(), ax=axes[1])

    plt.show()


def _plot_residuals(fit: ARIMAResultsWrapper) -> None:
    residuals = pd.DataFrame(fit.resid)
    fig, ax = plt.subplots(1, 2)
    residuals.plot(title="Residuals", ax=ax[0])
    residuals.plot(kind="kde", title="Density", ax=ax[1])
    plt.show()


def _auto_arima() -> None:
    df = get_oil_df()
    df["value"] = np.array([max(8, p) for p in df.price])

    model = pm.auto_arima(
        df.value,
        test="adf",  # to find optimal 'd'
        max_p=3,
        max_q=3,
        m=1,  # frequency of series
        d=None,  # let model determine 'd'
        seasonal=False,  # No Seasonality
        start_P=0,
        D=0,
        trace=True,
        error_action="ignore",
        suppress_warnings=True,
        stepwise=True,
    )

    print(model.summary())
    model.plot_diagnostics()
    plt.show()
    _plot_forecast(df, model)


def _plot_forecast(df: pd.DataFrame, model: ARIMA) -> None:
    n_periods = 24
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)
    index_of_fc = np.arange(len(df.value), len(df.value) + n_periods)

    fc_series = pd.Series(fc, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)

    plt.plot(df.value)
    plt.plot(fc_series, color="darkgreen")
    plt.fill_between(
        lower_series.index,
        lower_series,
        upper_series,
        color="k",
        alpha=0.15,
    )
    plt.show()


if __name__ == "__main__":
    _auto_arima()
    # main()
