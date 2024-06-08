#!/usr/bin/env python3
# Copyright 2024 John Hanley. MIT licensed.

# from https://docs.python.org/3/library/itertools.html#itertools.accumulate

from doctest import run_docstring_examples
from doctest import testmod as run_doctests
import operator
import unittest

from beartype import beartype
from beartype.typing import Callable, Generator, Iterable


@beartype
def accumulate1(
    iterable: Iterable[int],
    func: Callable[[int, int], int] = operator.add,
    *,
    initial: int | None = None
) -> Generator[int, None, None]:
    """Return running totals -- from the python documentation.

    >>> list(accumulate1([1,2,3,4,5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate1([1,2,3,4,5], initial=100))
    [100, 101, 103, 106, 110, 115]
    >>> list(accumulate1([1,2,3,4,5], operator.mul))
    [1, 2, 6, 24, 120]
    >>>
    >>> list(accumulate1([7]))
    [7]
    >>> list(accumulate1([]))
    []
    >>> list(accumulate1([], initial=7))
    [7]
    >>> list(accumulate1([8], initial=7))
    [7, 15]
    """
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    assert total is not None
    yield total
    for element in it:
        total = func(total, element)
        yield total


class AccumulateTest(unittest.TestCase):
    def test_accumulate(self) -> None:
        self.assertEqual(
            [7, 15],
            list(accumulate1([8], initial=7)),
        )
        self.assertEqual(
            [8, 17],
            list(accumulate1([8, 9], initial=None)),
        )
        self.assertEqual(
            [],
            list(accumulate1([], initial=None)),
        )


if __name__ == "__main__":
    # this amounts to running with `python -m doctest`
    run_docstring_examples(accumulate1, globals())

    run_doctests()  # same thing
