#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


from beartype import beartype


@beartype
def median_of_k_sorted_vectors(vecs: list[list[int]], verify: bool = False) -> int:
    """Given K sorted vectors containing a total of N numbers, returns the
    index of the median, as (vec_idx, idx), with vec_idx in range(k).

    There shall be N // 2 numbers less than or equal to the median,
    and N // 2 numbers greater than or equal to the median.
    We require that N shall be odd, so the median is present in the input.
    That is, we do not perform any averaging.
    """
    n = sum(map(len, vecs))
    if n % 2 == 0:
        raise ValueError(
            f"N must be odd, but it was {n}. Number of vectors was {len(vecs)}."
        )
