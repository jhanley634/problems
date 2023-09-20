import unittest


def log(s: str, verbose: bool = False) -> None:
    if verbose:
        print(s)


class MyType:
    def __init__(self, s: str) -> None:
        self._mystring = s

    def __add__(self, other) -> str:
        log(f"\nMyType add {self._mystring} + {other}")
        return self._mystring + other

    def __radd__(self, other) -> str:
        log(f"\nMyType radd {other} + {self._mystring}")
        return other + self._mystring


class Ty:
    def __init__(self, n) -> None:
        self._n = n

    def __add__(self, other) -> int:
        log(f"\nTy add {self._n} + {other}")
        return self._n + len(other)

    def __radd__(self, other) -> int:
        log(f"\nTy radd {self._n} + {other}")
        return self._n + len(other)

    def __repr__(self) -> str:
        return f"Ty({self._n})"


class MyTypeTest(unittest.TestCase):
    def test_my_type(self) -> None:
        log("\n\ntest_my_type")
        self.assertEqual("wx", MyType("w") + "x")
        self.assertEqual("yz", "y" + MyType("z"))

    def test_ty(self) -> None:
        log("\n\ntest_ty")
        self.assertEqual(8, "a" + Ty(7))
        self.assertEqual(8, Ty(7) + "b")

    def test_both(self) -> None:
        log("\n\ntest_both")
        self.assertEqual(8, MyType("c") + Ty(7))
