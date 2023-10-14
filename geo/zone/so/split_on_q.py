#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
#
# from https://stackoverflow.com/questions/77294679/pandas-column-split-a-row-with-conditional-and-create-a-separate-column

import pandas as pd


def get_input() -> pd.DataFrame:
    csv_text = """
           a      1     198q24
           a      2     128q6
           a      6     1456
           b      7     67q22
           b      1     56
           c      3     451q2
           d      11    1q789
           """.strip()
    return pd.DataFrame(map(str.split, csv_text.splitlines()), columns=["a", "b", "c"])


def split_on_q(df_in: pd.DataFrame) -> pd.DataFrame:
    df = df_in.c.str.split("q", expand=True)
    df_out = df_in.copy()
    df_out["c"] = df[0]
    df_out["d"] = prepend_q(df[1])
    return df_out


def prepend_q(series: pd.Series) -> pd.Series:
    return series.apply(lambda s: None if s is None else f"q{s}")


if __name__ == "__main__":
    print(split_on_q(get_input()))
