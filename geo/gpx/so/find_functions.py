#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78067735/statically-inspect-a-python-test-suite

from pathlib import Path
from types import FunctionType, MethodType, ModuleType
from typing import Callable, Generator, Iterable, NamedTuple
from unittest import TestCase
from unittest.main import TestProgram
import re
import sys


def find_callable_functions(module: ModuleType | type) -> list[Callable]:
    """Finds callables within a module, including functions and classes."""
    return [
        obj
        for obj in module.__dict__.values()
        if callable(obj) and isinstance(obj, (FunctionType, MethodType, type))
    ]


# cf inspect.{isfunction, ismethod, isclass}


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
                record = Source(file=source_file.resolve(), line=i + 1, src=[])
            if not decorator.match(line):
                record.src.append(line)
        if record.line > 0:
            yield record


def find_functions_under(
    paths: Iterable[Path], needle
) -> Generator[Source, None, None]:
    for path in paths:
        if path.is_file() and path.suffix == ".py":
            for record in find_functions_in(path):
                if needle in "".join(record.src):
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
        self.assertEqual(14, len(source_records))

    def test_find_functions_under(self, verbose: bool = False) -> None:
        source_folder = Path(__file__).parent
        glob = source_folder.glob("**/*.py")

        records = list(find_functions_under(glob, "generate_scenario"))
        self.assertEqual(4, len(records))

        if verbose:
            for record in records:
                print(record[:2])
                print("".join(record.src))
