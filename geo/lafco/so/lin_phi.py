#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stats.stackexchange.com/questions/647982/how-to-fix-errors-in-lins-1989-approximation-to-the-gaussian-cdf
from typing import Generator
import math

from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np
import pandas as pd
import seaborn as sns


def lin_phi(x: float, mu: float = 0, sigma: float = 1) -> float:
    z = (x - mu) / sigma
    if z >= 0:
        return 1 - 0.5 * math.exp(-0.72 * z - 0.42 * z**2)
    else:
        return 0.5 * math.exp(0.72 * z - 0.42 * z**2)


def gen_df(n: int = 1_000) -> Generator[dict[str, float | str], None, None]:
    for x in np.linspace(-3.0, 3.0, num=n):
        yield {"x": x, "value": lin_phi(x), "type": "cdf"}
        yield {"x": x, "value": lin_phi(x) - norm.cdf(x), "type": "error"}


if __name__ == "__main__":
    df = pd.DataFrame(gen_df())
    sns.scatterplot(data=df, x="x", y="value", hue="type")
    plt.show()

    df1 = pd.DataFrame()
    df1["x"] = np.unique(df.x)
    df1["cdf"] = df1.x.apply(lin_phi)
    df1["error"] = df1.cdf - norm.cdf(df1.x)
    # display the max error
    print(df1.describe())
