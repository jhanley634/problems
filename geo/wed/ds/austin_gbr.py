#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/128430/univariate-time-series-forecasting-with-bimodal-distrib
from pathlib import Path

from pandas.tseries.holiday import USFederalHolidayCalendar
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
    df["month"] = df.ticket_date.dt.month

    holidays = USFederalHolidayCalendar().holidays(
        start=df.ticket_date.min(),
        end=df.ticket_date.max(),
    )
    df["holiday"] = df.ticket_date.isin(holidays)
    df["weekday"] = df.ticket_date.dt.weekday
    # SATURDAY = 5
    # df["workday"] = (df.ticket_date.dt.weekday < SATURDAY) & ~df.holiday
    return df


def main() -> None:
    df = get_garbage_df()
    y = df.net_weight_kg
    df = df.drop(columns=["net_weight_kg", "ticket_date"])
    x = df
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(x_train, y_train)
    print(int(reg.predict(x_test[1:2])[0]))
    print(reg.score(x_test, y_test))


if __name__ == "__main__":
    main()
