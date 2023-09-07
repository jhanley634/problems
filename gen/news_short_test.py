import unittest

from gen.news_summary import Summarizer
from gen.news_summary_test import get_article_text_file


class SummarizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Summarizer()

    def test_get_article_text(self) -> None:
        art = get_article_text_file().read_text()
        print(art)
        self.assertEqual(4517, len(art))
