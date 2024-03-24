#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/128430/univariate-time-series-forecasting-with-bimodal-distribution
from pathlib import Path

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

KAGGLE_DATASET = "https://www.kaggle.com/datasets/ivantha/daily-solid-waste-dataset"
ARCHIVE = Path("~/Desktop/archive").expanduser()
CSV = ARCHIVE / "open_source_austin_daily_waste_2003_jan_2021_jul.csv"


def get_garbage_df() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df["ticket_date"] = pd.to_datetime(df.ticket_date)
    df = df[df.ticket_date > "2003-01-13"]  # filter an isolated outlier date
    df["elapsed"] = (df.ticket_date - df.ticket_date.min()).dt.days
    df["weekday"] = df.ticket_date.dt.weekday
    df["month"] = df.ticket_date.dt.month
    return df


def main():
    df = get_garbage_df().drop(columns=["ticket_date"])
    y = df.net_weight_kg
    df = df.drop(columns=["net_weight_kg"])
    X = df
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(X_train, y_train)
    print(int(reg.predict(X_test[1:2])[0]))
    print(reg.score(X_test, y_test))


if __name__ == "__main__":
    main()
