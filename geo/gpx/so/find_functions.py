#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78067735/statically-inspect-a-python-test-suite
from collections.abc import Callable, Generator, Iterable
from importlib import import_module
from inspect import getsource, isfunction, isgenerator
from pathlib import Path
from types import FunctionType, MethodType, ModuleType
from unittest.main import TestProgram
import dis
import io
import os
import re
import sys
import unittest

from typing_extensions import Any, NamedTuple


def find_callable_functions(module: ModuleType | type) -> list[Callable[[Any], Any]]:
    """Finds callables within a module, including functions and classes."""
    return [
        obj
        for obj in module.__dict__.values()
        if callable(obj) and isinstance(obj, (FunctionType, MethodType, type))
    ]
    # cf inspect.{isfunction, ismethod, isclass}


def find_callable_matches(
    module: ModuleType | type, needle: str, verbose: bool = False
) -> Generator[Callable[[Any], Any], None, None]:
    for obj in module.__dict__.values():
        if callable(obj) and isinstance(obj, (FunctionType, MethodType, type)):
            if not isgenerator(obj) and isfunction(obj):
                buf = io.StringIO()
                dis.dis(obj, file=buf)
                names = obj.__code__.co_names
                if needle in buf.getvalue() and needle in names:
                    yield obj
                    if verbose:
                        print(getsource(obj))
                    # print(dis._disassemble_bytes(code, names=names))
                    # lines, start = findsource(obj)
                    # print("".join(lines[start : start + 5]), "\n")
                    # dis.disassemble(obj.__code__)


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
    paths: Iterable[Path], needle: str
) -> Generator[Source, None, None]:
    for path in paths:
        if path.is_file() and path.suffix == ".py":
            for record in find_functions_in(path):
                if needle in "".join(record.src):
                    yield record
            # file = f"{record.file.relative_to(os.getcwd())}"
            # m = import_module(file.replace("/", ".").removesuffix(".py"))


class FirstClass:
    def __init__(self, x: int) -> None:
        self.x = x

    def generate_scenario(self, a: int, b: int, c: int) -> None:
        self.x += a + b + c

    def run_scenario(self) -> None:
        self.generate_scenario(1, 2, 3)
        print(self.x)


class SecondClass:
    def __init__(self, y: int) -> None:
        self.y = y

    def generate_scenario(self, a: int, b: int, c: int) -> None:
        self.y += a * b * c

    def run_scenario(self) -> None:
        print(self.y)


class UnrelatedClass:
    def __init__(self) -> None:
        self.z = None


class TestFindFunctions(unittest.TestCase):
    def test_find_callable_functions(self) -> None:
        self.assertEqual(
            [TestProgram],
            find_callable_functions(sys.modules["__main__"]),
        )
        self.assertEqual(
            "<class '_frozen_importlib.FrozenImporter'>",
            str(find_callable_functions(os)[0]),
        )
        self.assertEqual(os, import_module("os"))
        self.assertEqual(
            [
                FirstClass.__init__,
                FirstClass.generate_scenario,
                FirstClass.run_scenario,
            ],
            find_callable_functions(FirstClass),
        )

    def test_find_callable_matches(self) -> None:
        self.assertEqual(
            [FirstClass.run_scenario],
            list(find_callable_matches(FirstClass, "generate_scenario")),
        )

    def test_find_functions(self) -> None:
        source_records = list(find_functions_in(Path(__file__)))
        self.assertEqual(15, len(source_records))

    def test_find_functions_under(self, verbose: bool = False) -> None:
        source_folder = Path(__file__).parent
        glob = source_folder.glob("**/*.py")

        records = list(find_functions_under(glob, "generate_scenario"))
        self.assertEqual(6, len(records))

        if verbose:
            for record in records:
                print(record[:2])
                print("".join(record.src))
