#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# https://stackoverflow.com/questions/75549599/how-to-efficiently-read-pq-files-python
# $ python -m cProfile -s tottime geo/ski/bench_parquet.py
from collections.abc import Generator
from pathlib import Path
from time import time

from tqdm import tqdm
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

K = 24
PQ_DIR = Path("/tmp/parquet.d")


def gen_dfs(
    k: int = K,
    dst_dir: Path = PQ_DIR,
    shape: tuple[int, int] = (667_858, 48),
) -> None:
    dst_dir.mkdir(exist_ok=True)
    rng = np.random.default_rng()
    for i in range(k):
        df = pd.DataFrame(
            rng.integers(66_000, size=shape) / 1_000,
            columns=[f"col_{j}" for j in range(shape[1])],
        )
        print(i)
        df.to_parquet(dst_dir / f"{i}.parquet", compression=None)


def read_dfs(src_dir: Path = PQ_DIR) -> Generator[pd.DataFrame]:
    for file in src_dir.glob("*.parquet"):
        yield pd.read_parquet(file)


def main() -> None:
    gen_dfs()
    t0 = time()

    for df in tqdm(read_dfs()):
        assert len(df) > 0

    files = list(PQ_DIR.glob("2*.parquet"))
    dataset = pq.ParquetDataset(files)
    assert dataset
    # df = dataset.read(use_threads=True).to_pandas()

    elapsed = time() - t0
    print(f"{elapsed:.3f} seconds elapsed, {elapsed / K:.3f} per file")


if __name__ == "__main__":
    main()
