# Copyright 2023 John Hanley. MIT licensed.

from inspect import cleandoc
import unittest

from geo.zone.outline_parser import Level, OutlineParser


class TestLevel(unittest.TestCase):
    def test_level(self) -> None:
        lvl = Level("E")
        self.assertEqual("E", f"{lvl}")
        self.assertEqual(3, lvl.depth)
        self.assertEqual(5, lvl.ordinal)


class TestOutlineParser(unittest.TestCase):
    @staticmethod
    def _levels_summary(lines: list[str]) -> list[tuple[int, ...]]:
        return [
            tuple(lvl.text for lvl in levels) for levels, line in OutlineParser(lines)
        ]

    def test_parse_parens(self) -> None:
        lines = cleandoc(
            """
        2. section
            (a) apple
                (1) Autumn
                    (A) Bough
                    (B) Glory
                (2) Golden
                    (A) Noble
                    (B) Sweet
            (b) banana
        """
        ).splitlines()
        self.assertEqual(
            [
                (),
                ("a",),
                ("a", "1"),
                ("a", "1", "A"),
                ("a", "1", "B"),
                ("a", "2"),
                ("a", "2", "A"),
                ("a", "2", "B"),
                ("b",),
            ],
            self._levels_summary(lines),
        )
        self.assertEqual(9, len(list(OutlineParser(lines))))
