# Copyright 2023 John Hanley. MIT licensed.

from collections import deque
from typing import Any, Iterable
import re


class Level:
    """Outline level, e.g. 2. (a) (1) (A) (ii)"""

    _level_re = [
        re.compile(r"^\d+$"),
        re.compile(r"^[a-z]+$"),
        re.compile(r"^\d+$"),
        re.compile(r"^[A-Z]+$"),
        re.compile(r"^[ivx]+$"),
    ]

    def __init__(self, text: str):
        self.text = text
        self.level = None
        for i, pattern in enumerate(self._level_re):
            if pattern.match(text):
                self.level = i
        assert self.level is not None, text

    def __repr__(self) -> str:
        return self.text


class OutlineParser:
    def __init__(self, lines: Iterable[str]):
        self.lines = deque(lines)
        self.level: list[Level] = []

    def __iter__(self) -> "OutlineParser":
        return self

    def __next__(self) -> tuple[Any, str]:
        if len(self.lines) == 0:
            raise StopIteration
        line = self.lines.popleft()
        self._parse_level(line)
        return tuple(self.level), line

    _level_re = re.compile(r"^\((\w+)\)")

    def _parse_level(self, line: str) -> None:
        if m := self._level_re.match(line.lstrip()):
            new_level = Level(m[1])
            self.level.append(Level(m[1]))
