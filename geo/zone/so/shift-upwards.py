#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
#
# from https://stackoverflow.com/questions/77328023/how-to-shift-up-data-in-a-csv-file

from io import StringIO, TextIOWrapper

import pandas as pd

csv_input = """
Name,Points,Type
name1,,
name2,,
name3,,
,4.5,
,2.5,
,1.0,
,,type1
,,type1
,,type1
"""


def shift_upwards(in_file: TextIOWrapper) -> list:
    in_df = pd.read_csv(in_file)
    result = pd.DataFrame(
        {col: in_df[col].dropna().reset_index(drop=True) for col in in_df.columns}
    )
    return result


if __name__ == "__main__":
    print(shift_upwards(StringIO(csv_input)))
