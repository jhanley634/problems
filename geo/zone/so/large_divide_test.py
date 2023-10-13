# Copyright 2023 John Hanley. MIT licensed.
#
# from https://stackoverflow.com/questions/77270197/python-division-doesnt-work-as-expected-for-large-numbers


import unittest


class LargeDivideTest(unittest.TestCase):
    def test_divide(self) -> None:
        a = 5.195497498518083
        b = int(1.0813434626413702e16)
        c = int(5.614533816817397e16)
        self.assertGreater(a * b, c)
        self.assertEqual(56_181_172_551_921_216, int(a * b))
        self.assertEqual(56_145_338_168_173_968, c)

        unit_price, units, budget = a, b, c
        units = int(budget // unit_price)
        self.assertEqual(10_806_537_426_721_572, units)
        self.assertEqual(10_813_434_626_413_702, b)

        self.assertEqual(-35_834_383_747_248, c - int(a * b))
        c -= int(unit_price * units)
        self.assertEqual(-8, c)
