import unittest

from gen.news_summary import Summarizer


class SummarizerTest(unittest.TestCase):
    def test_summarize(self):
        s = Summarizer()
        s.add_doc("hello world")

    def test_summarize_newsweek(self):
        url ='https://www.newsweek.com/americas-most-responsible-companies-2022'
