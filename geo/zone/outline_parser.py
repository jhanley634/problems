# Copyright 2023 John Hanley. MIT licensed.

from collections import deque
from typing import Any, Iterable
import re


def _int_val(s: str) -> int:
    return int(s)


def _lower_val(s: str) -> int:
    assert s.islower()
    return ord(s) - ord("a") + 1


def _upper_val(s: str) -> int:
    assert s.isupper()
    return ord(s) - ord("A") + 1


class Level:
    """Outline level, e.g. 2. (a) (1) (A) (ii)"""

    _level_re_ordinal = [
        (re.compile(r"^\d+$"), _int_val),
        (re.compile(r"^[a-z]+$"), _lower_val),
        (re.compile(r"^\d+$"), _int_val),
        (re.compile(r"^[A-Z]+$"), _upper_val),
        (re.compile(r"^[ivx]+$"), len),
    ]

    def __init__(self, text: str):
        self.text = text
        self.depth = 0
        self.ordinal = 0
        for i, (pattern, ord_fn) in enumerate(self._level_re_ordinal):
            if pattern.match(text):
                self.depth = i
                self.ordinal = ord_fn(text)
        assert self.depth > 0, text

    def __repr__(self) -> str:
        return self.text


class OutlineParser:
    def __init__(self, lines: Iterable[str]):
        self.lines = deque(lines)
        self.levels: list[Level] = []

    def __iter__(self) -> "OutlineParser":
        return self

    def __next__(self) -> tuple[Any, str]:
        if len(self.lines) == 0:
            raise StopIteration
        line = self.lines.popleft()
        self._parse_level(line)
        return tuple(self.levels), line

    _level_re = re.compile(r"^\((\w+)\)")

    def _parse_level(self, line: str) -> None:
        if m := self._level_re.match(line.lstrip()):
            new_lvl = Level(m[1])
            if len(self.levels) > 0 and self.levels[-1].depth == new_lvl.depth:
                # print(self.levels[-1].ordinal, new_lvl.ordinal)
                assert self.levels[-1].ordinal + 1 == new_lvl.ordinal
            while len(self.levels) > 0 and self.levels[-1].depth >= new_lvl.depth:
                self.levels.pop()
            self.levels.append(new_lvl)
