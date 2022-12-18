import unittest

from vision.collatz.collatz import collatz


class CollatzTest(unittest.TestCase):
    def test_collatz(self):
        self.assertEqual(collatz(1), 1)
        self.assertEqual(collatz(2), 2)
        self.assertEqual(collatz(3), 8)
        self.assertEqual(collatz(4), 3)
        self.assertEqual(collatz(5), 6)
        self.assertEqual(collatz(6), 9)
        self.assertEqual(collatz(7), 17)
        self.assertEqual(collatz(8), 4)
        self.assertEqual(collatz(9), 20)
        self.assertEqual(collatz(10), 7)
        self.assertEqual(collatz(11), 15)
        self.assertEqual(collatz(12), 10)
        self.assertEqual(collatz(13), 10)
        self.assertEqual(collatz(14), 18)
        self.assertEqual(collatz(15), 18)
        self.assertEqual(collatz(16), 5)
        self.assertEqual(collatz(17), 13)
        self.assertEqual(collatz(18), 21)
        self.assertEqual(collatz(19), 21)
        self.assertEqual(collatz(20), 8)
        self.assertEqual(collatz(1_000), 112)
        self.assertEqual(collatz(2_000), 113)
        self.assertEqual(collatz(10_000), 30)
        self.assertEqual(collatz(20_000), 31)
        self.assertEqual(collatz(100_000), 129)
        self.assertEqual(collatz(230_631), 443)
        self.assertEqual(collatz(410_011), 449)
        self.assertEqual(collatz(511_935), 470)
        self.assertEqual(collatz(1_000_000), 153)
        self.assertEqual(collatz(10_000_000), 146)
        self.assertEqual(collatz(100_000_000), 108)
        self.assertEqual(collatz(1_000_000_000), 101)

    def test_iterate(self):
        for i in range(1, 500_000):
            self.assertLess(collatz(i), 450, i)
