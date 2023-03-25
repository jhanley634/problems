# Copyright 2023 John Hanley. MIT licensed.

from functools import partialmethod
from pathlib import Path
import unittest

from tqdm import tqdm

from geo.ski.iso_filenames import GPX_DIR, copy_all, iso

tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)  # type: ignore [assignment]


class IsoFilenamesTest(unittest.TestCase):
    def test_iso_filenames(self):
        path = Path("01-Aug-2022-2043-milk.gpx")
        self.assertEqual(Path("2022-08-01-2043-milk.gpx"), iso(path))

        path = Path("2022-08-01-2043-spam.gpx")
        self.assertEqual(Path("2022-08-01-2043-spam.gpx"), iso(path))

        temp_dir = Path("/tmp")
        temp = temp_dir / path.name
        temp.write_text("Hello.\n")
        copy_all(temp_dir)

        temp.unlink()
        (GPX_DIR / temp.name).unlink()
