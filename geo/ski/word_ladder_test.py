import unittest

from .word_ladder import WordLadder


class TestWordLadder(unittest.TestCase):
    def test_init(self):
        for length, num_words in [
            (3, 1294),
            (4, 4994),
            (10, 30_824),
            (17, 1813),
        ]:
            wl = WordLadder(length=length)
            self.assertEqual(num_words, len(wl.words))
