from io import StringIO
import dis
import inspect
import unittest


class MyManager:
    def __enter__(self):
        print("enter")

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit")


def app():
    with MyManager() as m:
        report_on_ctx_mgr()


def report_on_ctx_mgr():
    stack = inspect.stack()
    assert "test_app" == stack[2].function
    assert "app" == stack[1].function
    fn = globals()[stack[1].function]
    src = inspect.getsource(fn)
    print(list(filter(_contains_with, src.splitlines())))

    out = StringIO()
    dis.dis(fn, file=out)
    disasm = out.getvalue()
    if "MyManager" in disasm:
        print(disasm)


def _contains_with(s: str):
    return "with " in s


class TestApp(unittest.TestCase):
    def test_app(self):
        app()
