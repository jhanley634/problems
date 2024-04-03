# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285911/leetcode-137-single-number-ii-python-bit-operations


import random
import unittest

from hypothesis import given
import hypothesis.strategies as st


def single_number(nums: list[int]) -> int:
    bias = 2**31
    nums = [num + bias for num in nums]
    assert all(num >= 0 for num in nums)

    res = 0

    for bit in range(32):
        counts = sum(num < 0 for num in nums)
        mask = 1 << bit
        for num in nums:
            if abs(num) & mask:
                counts += 1
        if counts % 3 == 1:
            res |= mask

    return res - bias


class TestLeet137(unittest.TestCase):
    def test_leet137(self) -> None:
        self.assertEqual(3, single_number([2, 2, 3, 2]))
        self.assertEqual(0, single_number([2, 1, 2, 1, 2, 1, 0]))
        self.assertEqual(-99, single_number([0, 1, 0, 1, 0, 1, -99]))

    def test_negative_binary(self) -> None:
        num = -6
        self.assertEqual("-00000000000000000000000000000110", f"{num:033b}")


# These constants are specified by https://leetcode.com/problems/single-number-ii
LO = -(2**31)
HI = 2**31 - 1


@given(st.lists(st.integers(min_value=LO, max_value=HI), min_size=1))
def test_leet(randoms: list[int]) -> None:
    target, *distractors = randoms
    arg = [target] + distractors * 3
    assert single_number(arg) == target

    arg.sort()
    assert single_number(arg) == target

    random.shuffle(arg)
    assert single_number(arg) == target
