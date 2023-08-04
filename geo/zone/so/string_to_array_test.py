# Copyright 2023 John Hanley. MIT licensed.


import unittest

from hypothesis import given
import hypothesis.strategies as st

from geo.zone.so.string_to_array import TombstoneString, _get_codec, string_to_array


class TombstoneStringTestCase(unittest.TestCase):
    def test_delete(self):
        ts = TombstoneString("hello world")
        self.assertEqual("hello world", str(ts))
        ts.delete(range(2, 6))


class StringToArrayTest(unittest.TestCase):
    def test_get_codec(self):
        self.assertEqual((1, 0, "ascii"), _get_codec(""))
        self.assertEqual((1, 0, "ascii"), _get_codec("hi"))
        self.assertEqual((2, 2, "utf-16"), _get_codec("hi χ"))
        self.assertEqual((2, 2, "utf-16"), _get_codec("hi 气"))
        self.assertEqual((4, 4, "utf-32"), _get_codec("hi 🌱"))

    def test_string_to_array(self):
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
        s = "hi 气 🌱"
        self.assertEqual(
            [104, 0, 0, 0, 105, 0, 0, 0, 32, 0, 0, 0]
            + [20, 108, 0, 0, 32, 0, 0, 0, 49, 243, 1, 0],
            string_to_array(s).tolist(),
        )

    def test_one_roundtrip(self):
        s = "hi χ 气 🌱"
        _, _, codec = _get_codec(s)
        self.assertEqual(s, string_to_array(s).tobytes().decode(codec))


# pytest --capture=tee-sys
@given(st.text(min_size=20))
def test_roundtrip(s: str):
    _, _, codec = _get_codec(s)
    assert s == string_to_array(s).tobytes().decode(codec)
