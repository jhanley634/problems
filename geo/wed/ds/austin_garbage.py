#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/128430/univariate-time-series-forecasting-with-bimodal-distribution
from pathlib import Path

from pycaret.regression import RegressionExperiment
import pandas as pd

KAGGLE_DATASET = "https://www.kaggle.com/datasets/ivantha/daily-solid-waste-dataset"
ARCHIVE = Path("~/Desktop/archive").expanduser()
CSV = ARCHIVE / "open_source_austin_daily_waste_2003_jan_2021_jul.csv"


def main():
    df = pd.read_csv(CSV)
    df["ticket_date"] = pd.to_datetime(df.ticket_date)
    df = df[df.ticket_date > "2003-01-13"]  # filter an isolated outlier date
    df["elapsed"] = (df.ticket_date - df.ticket_date.min()).dt.days
    df["weekday"] = df.ticket_date.dt.weekday
    df["month"] = df.ticket_date.dt.month
    print(df)
    print(df.describe())
    s = RegressionExperiment()
    s.setup(df, target="net_weight_kg", session_id=42)
    print(s)

    best = s.compare_models()
    print(best)

    print(s.evaluate_model(best))

    s.plot_model(best, plot="residuals")


if __name__ == "__main__":
    main()
