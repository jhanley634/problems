#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from typing import Generator

from bs4 import BeautifulSoup
from bs4.element import Tag
import typer


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

    def get_paragraphs(self) -> Generator[Tag, None, None]:
        yield from self.soup.find_all("p")


def main(input_html_file: Path) -> None:
    LawParser(input_html_file).parse()


if __name__ == "__main__":
    typer.run(main)
