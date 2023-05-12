#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from subprocess import check_output
from typing import Generator


class AgendaParser:
    def __init__(self, in_folder: str):
        self.folder = Path(in_folder).expanduser()

    def parse_all_agenda_pdfs(self) -> None:
        for in_file in self.folder.glob("*.pdf"):
            self.parse_agenda_pdf(in_file)

    def parse_agenda_pdf(self, in_file: Path) -> Generator[str, None, None]:
        cmd = f"pdftotext -layout {in_file} -"
        for line in check_output(cmd, shell=True).decode().splitlines():
            yield line
