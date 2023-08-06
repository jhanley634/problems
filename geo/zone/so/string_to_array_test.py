# Copyright 2023 John Hanley. MIT licensed.


import unittest

from hypothesis import given
import hypothesis.strategies as st

from geo.zone.so.string_to_array import (
    Article,
    TombstoneString,
    _get_codec,
    lorem_ipsum_article,
    string_to_array,
)


class TombstoneStringTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ts = TombstoneString("hello world")

    def test_delete(self) -> None:
        ts = self.ts
        self.assertEqual("hello world", str(ts))

        ts.delete(range(4, 6))
        self.assertEqual("hellworld", str(ts))

    def test_delete_word(self) -> None:
        ts = TombstoneString("the big bear")
        ts.delete_word("big", 0)
        self.assertEqual("the  bear", str(ts))

    def test_slice(self) -> None:
        self.assertEqual("ello", "".join(self.ts._slice_chars(range(1, 5))))

    def test_index(self) -> None:
        self.assertEqual(6, self.ts.index("world"))

        ts = TombstoneString("hi χ 气")
        self.assertEqual((2, 2, "utf-16"), _get_codec(f"{ts}"))
        self.assertEqual(1, ts.index("i "))

        ts = TombstoneString("hi χ 气 🌱")
        self.assertEqual((4, 4, "utf-32"), _get_codec(f"{ts}"))
        self.assertEqual(1, ts.index("i "))

        with self.assertRaises(ValueError):
            ts.index("fourscore")


class ArticleTest(unittest.TestCase):
    def test_article(self) -> None:
        text = lorem_ipsum_article()
        self.assertTrue(text.startswith("aaa"))
        self.assertEqual(1_000_890, len(text))
        art = Article(text)
        self.assertEqual(text, str(art))

        n = art.censor("moo")
        self.assertEqual(1_980, n)
        self.assertEqual(994_950, len(str(art)))
        # self.assertEqual(994_950 * "a", str(art))


class StringToArrayTest(unittest.TestCase):
    def test_get_codec(self) -> None:
        self.assertEqual((1, 0, "ascii"), _get_codec(""))
        self.assertEqual((1, 0, "ascii"), _get_codec("hi"))
        self.assertEqual((2, 2, "utf-16"), _get_codec("Straße des Bücher"))
        self.assertEqual((2, 2, "utf-16"), _get_codec("hi χ"))
        self.assertEqual((4, 4, "utf-32"), _get_codec("hi 🌱" + chr(0x110000 - 1)))

    def test_string_to_array(self) -> None:
        s = "hi"
        self.assertEqual(
            [104, 105],
            string_to_array(s).tolist(),
        )
        s = "hi χ 气"
        self.assertEqual(
            [104, 0, 105, 0, 32, 0, 199, 3, 32, 0, 20, 108],
            string_to_array(s).tolist(),
        )
        s = "hi χ 🌱"
        self.assertEqual(
            [104, 0, 0, 0, 105, 0, 0, 0, 32, 0, 0, 0]
            + [199, 3, 0, 0, 32, 0, 0, 0, 49, 243, 1, 0],
            string_to_array(s).tolist(),
        )

    def test_one_roundtrip(self) -> None:
        s = "hi χ 气 🌱"
        self.assertEqual(s, roundtrip(s))


def roundtrip(s: str) -> str:
    """This is the identity function."""
    _, _, codec = _get_codec(s)
    return string_to_array(s).tobytes().decode(codec)


# pytest --capture=tee-sys
@given(st.text(min_size=20))
def test_roundtrip(s: str) -> None:
    assert s == roundtrip(s)
