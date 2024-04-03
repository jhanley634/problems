#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

# based on https://datascience.stackexchange.com/questions/74125/how-to-add-a-calculated-column

from ydata_profiling import ProfileReport
import pandas as pd


def main(in_file: str = "/tmp/k/san_jose_pm25.csv") -> None:
    # data from:
    # https://www.epa.gov/outdoor-air-quality-data/download-daily-data
    df = pd.read_csv(in_file)
    assert 1661 == len(df)

    df["date"] = pd.to_datetime(df["Date"])
    df["aqi"] = df["DAILY_AQI_VALUE"]
    df["pm25_conc"] = df["Daily Mean PM2.5 Concentration"]
    df["site_id"] = df["Site ID"]
    df["hazy"] = df["AQS_PARAMETER_CODE"] == 88502
    df = df[["date", "aqi", "pm25_conc"]][df.site_id == 60850005]
    df = df.drop_duplicates().sort_values("date")
    assert 482 == len(df)

    ProfileReport(df).to_file("/tmp/k/san_jose_pm25.html")

    df["shift_conc"] = df["pm25_conc"].shift(1)
    df["delta"] = df["pm25_conc"] - df["shift_conc"]
    df = df[:10]
    print(df)


if __name__ == "__main__":
    main()
