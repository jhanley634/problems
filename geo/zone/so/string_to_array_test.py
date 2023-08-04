# Copyright 2023 John Hanley. MIT licensed.

import unittest

import numpy as np

from geo.zone.so.string_to_array import _get_codec, string_to_array


class StringToArrayTest(unittest.TestCase):
    def test_get_codec(self):
        self.assertEqual("ascii", _get_codec(""))
        self.assertEqual("ascii", _get_codec("hi"))
        self.assertEqual("utf-16", _get_codec("hi χ"))
        self.assertEqual("utf-16", _get_codec("hi 气"))
        self.assertEqual("utf-32", _get_codec("hi 🌱"))

    def test_string_to_array(self):
        # s = "hi 气 ."  # 0x6c14; 🌱 0x1f331
        s = "hi χ ."  # 0x3c7
        s = "hi   ."
        self.assertEqual(105, max(map(ord, s)))

        self.assertEqual(np.uint8, string_to_array(s).dtype)
        self.assertEqual(6, len(string_to_array(s)))
        self.assertEqual(
            # "ÿþh\x00i\x00 \x00Ç\x03 \x00.\x00",
            "hi   .",
            "".join(map(chr, string_to_array(s))),
        )
        self.assertEqual(
            # [255, 254, 104, 0, 105, 0, 32, 0, 199, 3, 32, 0, 46, 0],
            [104, 105, 32, 32, 32, 46],
            string_to_array(s).tolist(),
        )
