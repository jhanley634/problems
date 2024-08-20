# Copyright 2024 John Hanley. MIT licensed.
# from https://stackoverflow.com/questions/78650421/get-variable-from-identifier-in-a-context
from collections.abc import Generator
from inspect import stack
from tokenize import tokenize
import io
import token
import unittest


def f() -> Generator[str, None, None]:
    # print("Doing something in function f.")
    yield from detect()


def detect() -> Generator[str, None, None]:
    name = stack()[1].function
    source_line = stack()[2].code_context[0]  # type: ignore [index]
    tokens = tokenize(io.BytesIO(source_line.encode()).read)
    for tok in tokens:
        if (
            tok.type == token.NAME
            and tok.string == name
            and all(ch == next(tokens).string for ch in "()")
        ):
            yield (
                f"Current invocation of function {name} was in line {tok.line[:-1]} at position {tok.start[1]}."
            )


class IntrospectionTest(unittest.TestCase):
    def test_detect(self) -> None:
        self.assertEqual(
            [
                "Current invocation of function f was in line             list(f()), at position 17."
            ],
            list(f()),
        )
        # self.assertEqual(expected, ([f() for f in []], list(f())))


expected: tuple[list[str], list[str]] = (
    [],
    [
        "Current invocation of function f was in line             ([f() for f in []], list(f())), at position 14.",
        "Current invocation of function f was in line             ([f() for f in []], list(f())), at position 37.",
    ],
)
