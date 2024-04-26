# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/291672/create-a-snail-matrix

import unittest

from geo.wed.so.snail import Matrix, square


def print_matrix(matrix: Matrix) -> None:
    padding = len(str(len(matrix) ** 2))
    for row in matrix:
        print(" ".join(f"{num:>{padding}}" for num in row))


class SnailTest(unittest.TestCase):
    def test_matrix(self) -> None:
        # print_matrix(square(10))

        assert square(1) == [[1]]
        self.assertEqual(
            square(2),
            [
                [1, 2],
                [4, 3],
            ],
        )
        assert square(2) == [
            [1, 2],
            [4, 3],
        ]
        assert square(3) == [
            [1, 2, 3],
            [8, 9, 4],
            [7, 6, 5],
        ]
        assert square(4) == [
            [1, 2, 3, 4],
            [12, 13, 14, 5],
            [11, 16, 15, 6],
            [10, 9, 8, 7],
        ]
        assert square(5) == [
            [1, 2, 3, 4, 5],
            [16, 17, 18, 19, 6],
            [15, 24, 25, 20, 7],
            [14, 23, 22, 21, 8],
            [13, 12, 11, 10, 9],
        ]
