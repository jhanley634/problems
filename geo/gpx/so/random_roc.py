#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/126359/does-a-random-classifier-have-a-diagonal-roc
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any
import warnings

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import seaborn.objects as so


@contextmanager
def _filter_warnings() -> Generator[None]:
    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        message="use_inf_as_na option is deprecated and will be removed ",
    )
    yield


def _get_fp_tp_rates() -> tuple[Any, Any, Any, Any]:
    # from https://www.sharpsightlabs.com/blog/plot-roc-curve-in-python-seaborn

    # Generate a binary classification problem.
    x, y = make_classification(
        n_samples=10_000,
        class_sep=0.9,
        n_classes=2,
        n_clusters_per_class=2,
        n_features=2,
        n_redundant=0,
        n_repeated=0,
        random_state=42,
    )
    df_x = pd.DataFrame(x)
    print(df_x.describe())
    sns.scatterplot(data=df_x, x=0, y=1, hue=y)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=43
    )

    noskill_probabilities: list[int] = [0] * len(y_test)

    lr_model = LogisticRegression()
    lr_model.fit(x_train, y_train)

    probabilities_lr = lr_model.predict_proba(x_test)

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


def main() -> None:
    # df = fetch_penguin_df()
    # sns.pairplot(df, hue="species")

    (
        falseposrate_noskill,
        trueposrate_noskill,
        falseposrate_logistic,
        trueposrate_logistic,
    ) = _get_fp_tp_rates()

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
