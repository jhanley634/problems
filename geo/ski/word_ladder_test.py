import unittest

from .word_ladder import WordLadder


class TestWordLadder(unittest.TestCase):
    def test_init(self):
        for length, num_words in [
            (17, 1813),
            (10, 30_824),
            (4, 4994),
            (3, 1294),
        ]:
            wl = WordLadder(length=length)
            self.assertEqual(num_words, len(wl.words))

        self.assertEqual(3882, len(wl.nodes))
