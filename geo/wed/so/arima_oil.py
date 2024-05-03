#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291850/forecast-volatility-of-monthly-crude-oil-prices-using-garch
from pathlib import Path
import datetime as dt

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
    print(get_oil_df())


if __name__ == "__main__":
    main()
