# Copyright 2023 John Hanley. MIT licensed.

from inspect import cleandoc
from pprint import pp
import unittest

from geo.zone.outline_parser import OutlineParser


class TestOutlineParser(unittest.TestCase):
    def test_parse_fresh_fruit(self) -> None:
        lines = cleandoc(
            """
        1. one
            a. apple
                i. Granny
                ii. Delicious
            b. banana
        2. two
        """
        ).splitlines()
        self.assertEqual(6, len(list(OutlineParser(lines))))

    @staticmethod
    def _level_summary(lines: list[str]) -> list[tuple[int, ...]]:
        ret = []
        for levels, line in OutlineParser(lines):
            ret.append(tuple(lvl.text for lvl in levels))
        return ret

    def test_parse_parens(self) -> None:
        lines = cleandoc(
            """
        2. section
            (a) apple
                (1) Granny
                    (A) Smith
                    (B) Delicious
            (b) banana
        """
        ).splitlines()
        pp(list(OutlineParser(lines)))
        self.assertEqual(
            [(), ("a",), ("a", "1"), ("a", "1", "A"), ("a", "1", "B"), ("b",)],
            self._level_summary(lines),
        )
        self.assertEqual(6, len(list(OutlineParser(lines))))
