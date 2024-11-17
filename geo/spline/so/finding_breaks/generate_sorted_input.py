#! /usr/bin/env python
# from https://stackoverflow.com/questions/79195892/most-efficient-way-to-get-unique-elements-from-sorted-list

from random import choices

import numpy as np
import numpy.typing as npt


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
) -> npt.NDArray[np.int_]:
    """Returns a sorted array of random non-negative integers."""
    population = range(distinct_values)
    rng = np.random.default_rng()
    xs = rng.choice(population, n)
    assert isinstance(xs, np.ndarray)
    return np.sort(xs)


if __name__ == "__main__":
    print(generate_sorted_numpy_array(24))
