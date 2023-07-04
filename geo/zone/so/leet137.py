# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285911/leetcode-137-single-number-ii-python-bit-operations
import unittest


def single_number(nums: list[int]) -> int:
    INT_BASE = 33  # because of INT32_MIN
    # give python what it likes
    counts_nz = [0 for _ in range(INT_BASE)]
    vals_bit = ["0" for _ in range(INT_BASE)]

    for num in nums:
        # 33 because of INT32_MIN takes 33 bits to represent.
        for idx, bin_val in enumerate(f"{num:033b}"):
            if bin_val != "0":  # can be "1" or "-"
                counts_nz[idx] += 1
                vals_bit[idx] = bin_val

        # make the bits binary string -- set to value for M3 + 1 and 0 otherwise
        bin_res = "".join(
            [
                vals_bit[idx] if count % 3 == 1 else "0"
                for idx, count in enumerate(counts_nz)
            ]
        )

    return int(bin_res, 2)


class TestLeet137(unittest.TestCase):
    def test_leet137(self):
        self.assertEqual(3, single_number([2, 2, 3, 2]))
        self.assertEqual(99, single_number([0, 1, 0, 1, 0, 1, 99]))

    def test_negative_binary(self):
        num = -6
        self.assertEqual("-00000000000000000000000000000110", f"{num:033b}")
