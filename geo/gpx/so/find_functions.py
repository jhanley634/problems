#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78067735/statically-inspect-a-python-test-suite

from pathlib import Path
from types import FunctionType, ModuleType
from typing import Callable, Generator, NamedTuple
from unittest import TestCase
from unittest.main import TestProgram
import re
import sys


def find_callable_functions(module: ModuleType | type) -> list[Callable]:
    """Finds all callable functions in a module."""
    return [
        obj
        for obj in module.__dict__.values()
        if callable(obj) and isinstance(obj, (FunctionType, type))
    ]


class Source(NamedTuple):
    """coordinates of a source code location"""

    file: Path
    line: int
    src: list[str]


def find_functions_in(source_file: Path) -> Generator[Source, None, None]:
    decorator = re.compile(r"^\s*@")
    record_delimiter = re.compile(r"^(\s*def |if __name__ == .__main__.)")
    record = Source(Path("/dev/null"), -1, [])  # sentinel
    with open(source_file) as fin:
        for i, line in enumerate(fin):
            if record_delimiter.match(line):
                if record.line > 0:
                    yield record
                record = Source(file=source_file, line=i + 1, src=[])
            if not decorator.match(line):
                record.src.append(line)
        if record.line > 0:
            yield record


class FirstClass:
    def __init__(self):
        self.x = 1

    def get_x(self):
        return self.x

    def generate_scenario(self, a, b, c):
        self.x += a + b + c

    def run_scenario(self):
        print(self.x)


class SecondClass:
    def __init__(self):
        self.y = 2

    def get_y(self):
        return self.y

    def generate_scenario(self, a, b, c):
        self.y += a * b * c

    def run_scenario(self):
        print(self.y)


class TestFindFunctions(TestCase):
    def test_find_callable_functions(self) -> None:
        self.assertEqual(
            [TestProgram],
            find_callable_functions(sys.modules["__main__"]),
        )
        self.assertEqual(
            [
                FirstClass.__init__,
                FirstClass.get_x,
                FirstClass.generate_scenario,
                FirstClass.run_scenario,
            ],
            find_callable_functions(FirstClass),
        )

    def test_find_functions(self) -> None:
        source_records = list(find_functions_in(Path(__file__)))
        self.assertEqual(12, len(source_records))
