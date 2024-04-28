#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291815/coding-challenge-for-mixing-a-string
from collections import Counter
import unittest


def lower(s: str) -> str:
    """
    Filters the input string down to just lowercase letters.

    >>> lower('A aaaa xyz xyz')
    'aaaaxyzxyz'
    """
    return "".join(filter(str.islower, s))


def which(letter: str, biggest: int, *counts: Counter[str]) -> str:
    """Reports which counter has the most of the given letter, typically '1' or '2'."""
    for i, count in enumerate(counts):
        if count.get(letter) == biggest:
            return str(i + 1)
    return "999"


def mix(*strings: str) -> str:
    counts = [Counter(lower(string)) for string in strings]
    ret = []
    for letter in sorted(set("".join(strings))):
        biggest = max((count.get(letter, 0) for count in counts))
        if biggest > 1:
            ret.append(which(letter, biggest, *counts) + ":" + letter * biggest)
    return "/".join(ret)


class LetterCountTest(unittest.TestCase):
    def test_letter_count(self) -> None:
        self.assertEqual("2:eee", mix("ee", "eee"))
        self.assertEqual("1:ee", mix("ee", "fe"))
        self.assertEqual(
            "1:aaaa/3:bbb/3:dd",
            mix("A aaaa bb c", "bb", "& daaa bbb c d"),
        )
