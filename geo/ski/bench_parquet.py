#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75549599/how-to-efficiently-read-pq-files-python
# $ python -m cProfile -s tottime geo/ski/bench_parquet.py
from math import prod
from pathlib import Path
from time import time

from tqdm import tqdm
import numpy as np
import pandas as pd

K = 24
PQ_DIR = Path("/tmp/parquet.d")


def gen_dfs(k=K, dst_dir=PQ_DIR, shape=(667_858, 48)):
    dst_dir.mkdir(exist_ok=True)
    rng = np.random.default_rng()
    for i in range(k):
        n = prod(shape)
        df = pd.DataFrame(
            rng.integers(84_000, dtype=np.int32, size=shape),
            columns=[f"col_{j}" for j in range(shape[1])],
        )
        print(i)
        df.to_parquet(dst_dir / f"{i}.parquet")


def read_dfs(src_dir=PQ_DIR):
    for path in src_dir.glob("*.parquet"):
        yield pd.read_parquet(path)


def main():
    gen_dfs()
    t0 = time()
    for df in tqdm(read_dfs()):
        assert len(df) > 0

    elapsed = time() - t0
    print(f"{elapsed:.3f} seconds elapsed, {elapsed / K:.3f} per file")


if __name__ == "__main__":
    main()
