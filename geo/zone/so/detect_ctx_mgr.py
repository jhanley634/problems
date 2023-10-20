#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
#
# from https://stackoverflow.com/questions/77318785/how-do-i-detect-use-of-a-contextmanager

from io import StringIO
import dis
import inspect


class MyManager:
    def __enter__(self) -> None:
        print("enter")

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print("exit")


def app() -> None:
    with MyManager() as m:
        assert m
        report_on_ctx_mgr()


def report_on_ctx_mgr() -> None:
    stack = inspect.stack()
    assert "app" == stack[1].function
    fn = globals()[stack[1].function]
    src = inspect.getsource(fn)
    print(list(filter(_contains_with, src.splitlines())))

    out = StringIO()
    dis.dis(fn, file=out)
    disasm = out.getvalue()
    if "MyManager" in disasm:
        print(disasm)


def _contains_with(s: str) -> bool:
    return "with " in s


if __name__ == "__main__":
    app()
