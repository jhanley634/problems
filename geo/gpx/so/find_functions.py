#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78067735/statically-inspect-a-python-test-suite

from pathlib import Path
from types import FunctionType as function
from types import ModuleType
from typing import Callable
from unittest import TestCase
from unittest.main import TestProgram
import sys


def find_callable_functions(module: ModuleType | type) -> list[Callable]:
    """Finds all callable functions in a module."""
    return [
        obj
        for obj in module.__dict__.values()
        if callable(obj) and isinstance(obj, (function, type))
    ]


def find_functions(source_file: Path):
    0


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
    def test_find_functions(self) -> None:
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
