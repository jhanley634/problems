#! /usr/bin/env python
# from https://stackoverflow.com/questions/79195892/most-efficient-way-to-get-unique-elements-from-sorted-list
from pathlib import Path
from random import choices

import numpy as np
import numpy.typing as npt
import pyarrow as pa
import pyarrow.parquet as pq


def generate_sorted_values(
    n: int = 1_000_000,
    distinct_values: int = 12,
) -> list[int]:
    """Returns a sorted list of random non-negative integers."""
    population = range(distinct_values)
    xs = choices(population, k=n)
    return sorted(xs)


def generate_sorted_numpy_array(
    n: int = 1_000_000,
    distinct_values: int = 12,
) -> npt.NDArray[np.int16]:
    """Returns a sorted array of random non-negative integers."""
    assert distinct_values < 2**16
    population = np.array(range(distinct_values), dtype=np.int16)
    rng = np.random.default_rng()
    xs = rng.choice(population, n)
    return np.sort(xs)


def roundtrip_to_disk(temp_file: Path = Path("/tmp/sorted_xs.parquet")) -> None:
    xs = generate_sorted_numpy_array()

    table = pa.table({"x": pa.array(xs)})
    pq.write_table(table, temp_file)

    # Now read it back in.
    table2 = pq.read_table(temp_file)
    xs2 = np.array(table2["x"])
    assert xs2.dtype == np.int16
    assert xs.shape == xs2.shape
    assert (xs == xs2).all()
    assert 627 == temp_file.stat().st_size  # It compresses quite nicely.
    # temp_file.unlink()


if __name__ == "__main__":
    print(generate_sorted_numpy_array(24))
    roundtrip_to_disk()
