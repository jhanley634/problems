#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# from https://stackoverflow.com/questions/77974490/convert-txt-with-tabular-separated-data-to-csv-with-comma

from pathlib import Path
from subprocess import check_call
import io

import pandas as pd


def main():
    s = """Time (s)\tLength (m)\tAcel (s)
2\t3\t0.3"""
    df = pd.read_csv(io.StringIO(s), sep="\t").set_index("Time (s)")
    print(df, "\n\n")

    df.to_csv("pap.csv")
    check_call("cat pap.csv", shell=True)
    Path("pap.csv").unlink()


if __name__ == "__main__":
    main()
