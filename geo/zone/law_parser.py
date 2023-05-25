#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from typing import Generator
import re

from bs4 import BeautifulSoup
import typer

from geo.zone.outline_parser import OutlineParser


class LawParser:
    """Scans leginfo.legislature.ca.gov zoning code
    to identify the proper indent level."""

    def __init__(self, path: Path):
        assert path.exists()
        assert path.suffix == ".html"
        self.markdown: Path = path.with_suffix(".md")
        self.soup = BeautifulSoup(path.read_text(), "html.parser")

    def parse(self) -> "LawParser":  # builder pattern
        tag = self.soup.find_all("html")[-1]  # There's six(!?!) of them.
        # We _do_ see indent hints, e.g. the .5 in:  <p style="...;margin-left: 2.5em;">
        with open("/tmp/out.html", "w") as fout:
            fout.write(tag.prettify())
        self.soup = BeautifulSoup(tag.prettify(), "html.parser")
        return self

    def get_paragraphs(self) -> Generator[str, None, None]:
        section_number_re = re.compile(r"^\(\w+\)")
        for line in self._get_paragraph_lines():
            # deal with stacked section numbers
            while m := section_number_re.search(line):
                yield m[0]
                line = line.removeprefix(m[0]).lstrip()

            yield line

    def _get_paragraph_lines(self) -> Generator[str, None, None]:
        xlate_table = str.maketrans("\xa0", " ")  # No non-breaking spaces, please.
        for p in self.soup.find_all("p"):
            yield p.text.translate(xlate_table).strip()

    def format(self) -> None:
        paragraphs = list(OutlineParser(self.get_paragraphs()))
        for level, text in paragraphs:
            print(f"{level.ordinal} {level.value} {text[:60]}")


def main(input_html_file: Path) -> None:
    LawParser(input_html_file).parse().format()


if __name__ == "__main__":
    typer.run(main)
