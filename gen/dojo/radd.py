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
    """A type that cannot be added to itself."""

    def __init__(self, n: int) -> None:
        self._n = n

    def __add__(self, other) -> int:
        log(f"\nTy add {self._n} + {other}")
        return self._n + len(other)

    def __radd__(self, other) -> int:
        log(f"\nTy radd {self._n} + {other}")
        return len(other) + self._n

    def __repr__(self) -> str:
        return f"Ty({self._n})"


class MyTypeTest(unittest.TestCase):
    def test_my_type(self) -> None:
        log("\n\n test_my_type")
        self.assertEqual("wx", MyType("w") + "x")
        self.assertEqual("yz", "y" + MyType("z"))

    def test_ty(self) -> None:
        log("\n\n test_ty")
        self.assertEqual(7, "a" + Ty(6))
        self.assertEqual(8, Ty(7) + "b")
        with self.assertRaises(TypeError):
            sum([Ty(6), Ty(7), Ty(8)])

    def test_both(self) -> None:
        log("\n\n test_both")
        self.assertEqual(9, MyType("c") + Ty(8))
        with self.assertRaises(TypeError):
            Ty(9) + MyType("d")
