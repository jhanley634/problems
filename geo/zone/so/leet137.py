# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285911/leetcode-137-single-number-ii-python-bit-operations
import unittest


def single_number(nums: list[int]) -> int:
    BIAS = 2**31
    nums = [num + BIAS for num in nums]

    res = 0

    for bit in range(32):
        counts = 0
        mask = 1 << bit
        for num in nums:
            if num & mask:
                counts += 1
        if counts % 3 == 1:
            res |= mask

    return res - BIAS


class TestLeet137(unittest.TestCase):
    def test_leet137(self):
        self.assertEqual(3, single_number([2, 2, 3, 2]))
        self.assertEqual(-99, single_number([0, 1, 0, 1, 0, 1, -99]))

    def test_negative_binary(self):
        num = -6
        self.assertEqual("-00000000000000000000000000000110", f"{num:033b}")
