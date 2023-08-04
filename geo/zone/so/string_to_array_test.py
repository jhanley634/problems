# Copyright 2023 John Hanley. MIT licensed.

import unittest

import numpy as np

from geo.zone.so.string_to_array import string_to_array


class StringToArrayTest(unittest.TestCase):
    def test_string_to_array(self):
        # s = "hi 气 ."
        s = "hi χ ."
        self.assertEqual(np.uint8, string_to_array(s).dtype)
        self.assertEqual(14, len(string_to_array(s)))
        self.assertEqual(
            "ÿþh\x00i\x00 \x00Ç\x03 \x00.\x00",
            "".join(map(chr, string_to_array(s))),
        )
        self.assertEqual(
            [255, 254, 104, 0, 105, 0, 32, 0, 199, 3, 32, 0, 46, 0],
            string_to_array(s).tolist(),
        )
