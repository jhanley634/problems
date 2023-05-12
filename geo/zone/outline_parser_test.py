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

    def test_parse_parens(self) -> None:
        lines = cleandoc(
            """
        2. section
            (a) apple
                (1) Granny
                    (A) Smith
                    (B) Delicious
            (b) banana
        3. three
        """
        ).splitlines()
        pp(list(OutlineParser(lines)))
        self.assertEqual(7, len(list(OutlineParser(lines))))
