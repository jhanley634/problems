#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/126359/does-a-random-classifier-have-a-diagonal-roc

from contextlib import contextmanager
from pathlib import Path
from typing import Any
import re
import warnings

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import pandas as pd
import requests
import seaborn.objects as so

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
    assert 3 == df.species.nunique()
    assert 344 == len(df)

    df = df.sample(frac=1).reset_index(drop=True)  # shuffle the rows
    # Adelie & Chinstrap are indistinguishably mixed at this point.

    df["is_gentoo"] = df.species == "Gentoo"
    df = df.drop(columns="species")

    return df


@contextmanager
def _filter_warnings():
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="use_inf_as_na option is deprecated and will be removed ",
    )
    yield


def _get_fp_tp_rates() -> tuple[Any, Any, Any, Any]:
    # from https://www.sharpsightlabs.com/blog/plot-roc-curve-in-python-seaborn

    # Generate a binary classification problem.
    X, y = make_classification(n_samples=10_000, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=43
    )

    noskill_probabilities: list[int] = [0] * len(y_test)

    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)

    probabilities_lr = lr_model.predict_proba(X_test)

    # Filter, retaining just the positive case.
    probabilities_logistic_posclass = probabilities_lr[:, 1]

    falseposrate_noskill, trueposrate_noskill, _ = roc_curve(
        y_test, noskill_probabilities
    )
    falseposrate_logistic, trueposrate_logistic, _ = roc_curve(
        y_test, probabilities_logistic_posclass
    )
    return (
        falseposrate_noskill,
        trueposrate_noskill,
        falseposrate_logistic,
        trueposrate_logistic,
    )


def main():
    # df = get_penguin_df()

    (
        falseposrate_noskill,
        trueposrate_noskill,
        falseposrate_logistic,
        trueposrate_logistic,
    ) = _get_fp_tp_rates()

    # sns.pairplot(df, hue="species")
    with _filter_warnings():
        (
            so.Plot()
            .add(so.Line(color="red"), x=falseposrate_logistic, y=trueposrate_logistic)
            .add(
                so.Line(color="blue", linestyle="dashed"),
                x=falseposrate_noskill,
                y=trueposrate_noskill,
            )
            .layout(size=(7, 7))
            .show()
        )


if __name__ == "__main__":
    main()
