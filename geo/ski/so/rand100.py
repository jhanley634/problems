# Copyright 2023 John Hanley. MIT licensed.
from collections import Counter
import unittest

from numpy.random import default_rng


def rand100(size: int = 100_000) -> list[float]:
    """Generate random numbers between 0 and 100 inclusive (range is 101)."""
    g = RandomIntGenerator()
    return [g.rand_0_n(100 + 1) for _ in range(size)]


class RandomIntGenerator:
    def __init__(self, bits: list[bool] | None = None, size: int = 750_000) -> None:
        self._bits = bits or self._get_random_bits(size)

    @staticmethod
    def _get_random_bits(size: int) -> list[bool]:
        rng = default_rng()
        return list(map(bool, rng.integers(0, 2, size=size)))

    def _next_random_bit(self) -> bool:
        assert len(self._bits) > 0
        return self._bits.pop()

    def rand_0_n(self, n: int) -> float:
        """Generate random numbers in the half-open interval [0, n)."""
        # https://crypto.stackexchange.com/questions/104252/how-to-generate-random-numbers-within-a-range
        # Optimal Discrete Uniform Generation from Coin Flips, and Applications
        # https://arxiv.org/pdf/1304.1916.pdf
        v: int = 1
        c: int = 0
        while True:
            v *= 2
            c = 2 * c + self._next_random_bit()
            if v >= n:
                if c < n:
                    return c
                v -= n
                c -= n


# ruff: noqa: SLF001


class TestRand100(unittest.TestCase):
    def test_next_random_bit(self) -> None:
        g = RandomIntGenerator()
        for _ in range(len(g._bits)):
            self.assertIsInstance(g._next_random_bit(), bool)
        self.assertEqual(0, len(g._bits))

    def test_rand100(self, verbose: bool = False) -> None:
        xs = rand100()
        counts = Counter(xs)
        delta: float = max(counts.values()) - min(counts.values())
        if verbose:
            print("  ", delta)
        self.assertLess(delta, 0.2 * len(xs))
        self.assertEqual(len(xs), sum(counts.values()))
        self.assertEqual(0, sorted(counts.keys())[0])
        self.assertEqual(100, sorted(counts.keys())[-1])
        self.assertEqual(101, len(counts.keys()))
