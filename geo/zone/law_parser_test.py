# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
import unittest

from geo.zone.law_parser import LawParser


class TestLawParser(unittest.TestCase):
    def test_parse(self) -> None:
        desktop = Path("~/Desktop").expanduser()
        in_file = desktop / "GOV_65852.2.html"
        paragraphs = list(LawParser(in_file).parse().get_paragraphs())
        self.assertEqual(222, len(paragraphs))
