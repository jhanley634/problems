#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

import pandas as pd
import requests


def _get_csv_fspec(folder: Path = Path('/tmp')) -> Path:
    fspec = folder.expanduser() / 'ozone.csv'
    if not fspec.exists():
        url = 'https://www.sector6.net/shared/ozone.csv'
        r = requests.get(url)
        with open(fspec, 'w') as fout:
            fout.write(r.text)
    return fspec


def _get_df():
    # from https://rdrr.io/cran/mlbench/man/Ozone.html
    new_names = {
        'V1': 'month',
        'V2': 'day',
        'V3': 'dow',
        'V4': 'ozone',  # target variable
        'V5': 'pres_500mb',  # https://www.weather.gov/jetstream/500mb
        'V6': 'wind_mph',
        'V7': 'humidity',
        'V8': 'temp_f_sandberg',
        'V9': 'temp_f_el_monte',
        'V10': 'inversion_height_ft',
        'V11': 'gradient_mm_hg',
        'V12': 'inversion_temp_f',
        'V13': 'visibility_mi',
    }
    df = pd.read_csv(_get_csv_fspec())
    df = df.rename(columns=new_names)

    # Now shuffle target to the end.
    target = df.ozone
    df = df.drop(columns='ozone')
    df['ozone'] = target

    return df


def main():
    df = _get_df()
    print(df)


if __name__ == '__main__':
    main()
