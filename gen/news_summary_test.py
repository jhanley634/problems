from pathlib import Path
import unittest

from gen.news_summary import Summarizer


class SummarizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Summarizer()

    def test_summarize_newsweek(self):
        # self.s.add_doc("hello world")

        # url = "https://www.newsweek.com/americas-most-responsible-companies-2022"
        # self.s.add_doc_url(url)

        txt_file = Path("/tmp/cache/americas-most-responsible-companies-2022.txt")
        self.s.add_doc_file(txt_file)
