# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
from subprocess import check_output


class AgendaParser:
    def __init__(self, in_folder: str) -> None:
        self.folder = Path(in_folder).expanduser()

    def parse_all_agenda_pdfs(self) -> None:
        for in_file in self.folder.glob("*.pdf"):
            self.parse_agenda_pdf(in_file)

    def parse_agenda_pdf(self, in_file: Path) -> Generator[str]:
        cmd = f"pdftotext -layout {in_file} -"
        yield from check_output(cmd, shell=True).decode().splitlines()
