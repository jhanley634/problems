#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/126359/does-a-random-classifier-have-a-diagonal-roc

from pathlib import Path
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import sklearn

PENGUIN_URL = (
    "https://raw.githubusercontent.com/allisonhorst"
    "/esm-206-2018/master/week_6/penguins.csv"
)


def fetch_df(url: str) -> pd.DataFrame:
    cache_dir = Path("/tmp")
    cache_dir.mkdir(exist_ok=True)
    file = cache_dir / Path(url).name
    if not file.exists():
        file.write_text(requests.get(url).text)
    return pd.read_csv(file)


def get_penguin_df() -> pd.DataFrame:
    df = fetch_df(PENGUIN_URL)

    # Drop index, a pair of categorical columns, and unused measurements.
    cols = "sample_number region study_name culmen_length flipper_length"
    df = df.drop(columns=cols.split())

    species_re = re.compile(r"^(\w+) penguin .*", re.IGNORECASE)
    df["species"] = df.species.apply(lambda s: species_re.sub(r"\1", s))
    assert df.species.nunique() == 3

    return df


def main():
    df = get_penguin_df()
    print(df)
    print(df.describe())

    with warnings.catch_warnings():
        # warnings.simplefilter("ignore")
        warnings.filterwarnings(
            "ignore",
            category=FutureWarning,
            message="use_inf_as_na option is deprecated and will be removed ",
        )
        sns.pairplot(df, hue="species")
    plt.show()


if __name__ == "__main__":
    main()
