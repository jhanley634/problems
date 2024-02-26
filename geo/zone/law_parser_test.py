# Copyright 2023 John Hanley. MIT licensed.
from difflib import unified_diff
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

from geo.gpx.so.word_publisher import get_document
from geo.zone.law_parser import LawParser


class TestLawParser(unittest.TestCase):
    def test_parse(self) -> None:
        desktop = Path("~/Desktop").expanduser()
        in_file = list(desktop.glob("**/GOV_65852.2.html"))[0]
        paragraphs = list(LawParser(in_file).parse().get_paragraphs())
        self.assertEqual(222, len(paragraphs))

    def test_diff(self) -> None:
        ca_code_base = "https://law.justia.com/codes/california/"
        adu_2021_url = f"{ca_code_base}/2021/code-gov/title-7/division-1/chapter-4/article-2/section-65852-2-d-1/"
        adu_2022_url = f"{ca_code_base}/2022/code-gov/title-7/division-1/chapter-4/article-2/section-65852-2/"
        adu_2021 = BeautifulSoup(get_document(adu_2021_url), "html.parser")
        adu_2022 = BeautifulSoup(get_document(adu_2022_url), "html.parser")

        temp = Path("/tmp/k")
        (temp / "adu_2021.html").write_text(adu_2021.prettify())
        (temp / "adu_2022.html").write_text(adu_2022.prettify())

        diffs = unified_diff(
            adu_2021.prettify().splitlines(),
            adu_2022.prettify().splitlines(),
            n=1,
        )
        # print("\n".join(map(str.rstrip, diffs)))

        self.assertEqual(7, len(list(diffs)))
