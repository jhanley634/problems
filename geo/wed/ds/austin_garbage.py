#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://datascience.stackexchange.com/questions/128430/univariate-time-series-forecasting-with-bimodal-distribution
from pathlib import Path

from pycaret.regression import RegressionExperiment
from ydata_profiling import ProfileReport

from geo.wed.ds.austin_gbr import get_garbage_df


def main() -> None:
    df = get_garbage_df()
    print(df)
    print(df.describe())

    html = Path("/tmp/k/austin_garbage.html")
    if not html.exists():
        ProfileReport(df).to_file(html)

    s = RegressionExperiment()
    s.setup(df, target="net_weight_kg", session_id=42)
    print(s)

    best = s.compare_models()
    print(best)

    print(s.evaluate_model(best))

    s.plot_model(best, plot="residuals")


if __name__ == "__main__":
    main()
