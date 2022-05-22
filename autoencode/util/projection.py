
# Copyright 2022 John Hanley. MIT licensed.
from hashlib import blake2b

import pandas as pd


def _hash_col(col_name: str, seed='51') -> tuple:
    """Gives a 32-bit hash of input name."""
    digest = blake2b((seed + col_name).encode()).hexdigest()  # 128 nybbles
    return digest[:8], col_name


def _random_permutation(pairs: list[tuple]) -> list[str]:
    """Gives an arbitrary (repeatable!) re-ordering of column names."""
    return [col_name
            for _, col_name in sorted(pairs)]


def feature_subset(df: pd.DataFrame, *, num_features=None, fraction=1.0, keep=1):
    assert len(df.shape) == 2, df.shape

    nc = df.shape[1]  # num columns
    if num_features is None:
        num_features = int(fraction * nc)
    nc = min(nc, num_features)

    cols = _random_permutation(list(map(_hash_col, df.columns[keep:])))
    for col in cols:
        if df.shape[1] <= nc:
            break
        df.drop(columns=[col], inplace=True)

    return df
