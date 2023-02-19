# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
import unittest

from geo.ski.iso_filenames import iso


class IsoFilenamesTest(unittest.TestCase):
    def test_iso_filenames(self):
        path = Path("01-Aug-2022-2043-milk.gpx")
        self.assertEqual(Path("2022-08-01-2043-milk.gpx"), iso(path))
