# Copyright 2023 John Hanley. MIT licensed.

from inspect import cleandoc
import unittest

from roman import InvalidRomanNumeralError
from roman import fromRoman as from_roman

from geo.zone.outline_parser import Level, OutlineParser, _reverse_enumerate


class TestRoman(unittest.TestCase):
    def test_roman(self) -> None:
        self.assertEqual(4, from_roman("IV"))
        self.assertEqual(9, from_roman("IX"))
        self.assertEqual(90, from_roman("XC"))
        self.assertEqual(1900, from_roman("MCM"))

        with self.assertRaises(InvalidRomanNumeralError):
            from_roman("iv")


class TestReverseEnumerate(unittest.TestCase):
    def test_reverse_enumerate(self) -> None:
        self.assertEqual([(0, "a"), (1, "b"), (2, "c")], list(enumerate("abc")))
        self.assertEqual(
            [(2, "c"), (1, "b"), (0, "a")], list(_reverse_enumerate("abc"))
        )


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
                        (i) one
                        (ii) two
                        (iii) three
                        (iv) four
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
                ("a", "1", "A", "i"),
                ("a", "1", "A", "ii"),
                ("a", "1", "A", "iii"),
                ("a", "1", "A", "iv"),
                ("a", "1", "B"),
                ("a", "2"),
                ("a", "2", "A"),
                ("a", "2", "B"),
                ("b",),
            ],
            self._levels_summary(lines),
        )
        self.assertEqual(13, len(list(OutlineParser(lines))))

    def test_non_sequential(self) -> None:
        lines = cleandoc(
            """
        2. section
            (a) apple
            (b) banana
            (d) cherry
        """
        ).splitlines()
        with self.assertRaises(ValueError):
            self._levels_summary(lines)
