# Copyright 2023 John Hanley. MIT licensed.
from enum import Enum


class Level(Enum):
    """Outline level, e.g. 1) a) ii)"""


class OutlineParser:
    def __init__(self, lines):
        self.lines = lines

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.lines.pop(0)
        except IndexError:
            raise StopIteration
