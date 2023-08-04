# Copyright 2023 John Hanley. MIT licensed.

import unittest

import numpy as np

from geo.zone.so.string_to_array import string_to_array


class StringToArrayTest(unittest.TestCase):
    def test_string_to_array(self):
        self.assertEqual(np.uint8, string_to_array("hello world").dtype)
