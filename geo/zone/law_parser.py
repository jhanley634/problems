#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
import re

from bs4 import BeautifulSoup
import typer

from geo.zone.outline_parser import OutlineParser


class LawParser:
    """Scans leginfo.legislature.ca.gov zoning code
    to identify the proper indent level.
    """

    def __init__(self, path: Path) -> None:
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

    def get_paragraphs(self) -> Generator[str]:
        section_number_re = re.compile(r"^\(\w+\)")
        for line in self._get_paragraph_lines():
            if m := section_number_re.search(line):
                yield m[0]

            # Cleanup leading section numbers, which may be stacked.
            while m := section_number_re.search(line):
                line1 = line.removeprefix(m[0]).lstrip()
            assert not line1.startswith("(")
            yield line1

    def _get_paragraph_lines(self) -> Generator[str]:
        xlate_table = str.maketrans("\xa0", " ")  # No non-breaking spaces, please.
        for p in self.soup.find_all("p"):
            yield p.text.translate(xlate_table).strip()

    def _get_outline(self) -> list[tuple[str, str]]:
        return [
            (levels, text)
            for levels, text in OutlineParser(self.get_paragraphs())
            if not text.startswith("(")
        ]

    def format_md(self) -> str:
        for levels, text in self._get_outline():
            hashes = "#" * len(levels)
            dots = ". . " * len(levels)
            levels1 = str(levels).replace(",)", ")")
            return f"{hashes} {levels1}\n{dots} {text}\n"
        return None

    def format_html(self) -> None:
        style = "font-family: sans-serif; line-height: 1.4; max-width: 50em; text-align: justify;"
        html = [
            "<!DOCTYPE html><head><title>outline</title></head>"
            f"<body><div style='{style}'>"
        ]
        for levels, text in self._get_outline():
            heading = f"h{len(levels)}>"
            indent = 4 * len(levels)
            style = f"margin-left: {indent}em;"
            levels1 = str(levels).replace(",)", ")")
            html.append(
                f"<{heading} {levels1} </{heading}\n<p style='{style}'>{text}</p>\n"
            )

        soup = BeautifulSoup("\n".join(html), "html.parser")
        return soup.prettify()


def main(input_html_file: Path) -> None:
    print(LawParser(input_html_file).parse().format_html())


if __name__ == "__main__":
    typer.run(main)
