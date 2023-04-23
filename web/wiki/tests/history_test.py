# Copyright 2022 John Hanley. MIT licensed.
import unittest

from web.wiki.history import HistoryScraper


class HistoryTest(unittest.TestCase):
    def setUp(self) -> None:
        SHORT_ARTICLE = "Nathan_Safir"  # Page was created 2022-02-02.
        self.scraper = HistoryScraper(SHORT_ARTICLE)

    def test_ids(self) -> None:
        expected = [
            1072659079,
            1072642893,
            1072600131,
            1072576425,
            1072576090,
            1072563499,
            1072563485,
            1072505271,
            1072487282,
            1072487096,
            1072486832,
            1072486158,
            1072485842,
            1072485492,
            1072485313,
            1071324002,
            1070524139,
            1069619860,
            1069390842,
            1069387713,
            1069387625,
            1069387522,
            1069387483,
        ]
        self.assertEqual(23, len(expected))
        self.assertEqual(
            expected,
            [
                id_
                for id_, *_ in self.scraper._get_reverse_history_ids()
                if id_ <= 1072659079
            ],
        )

    def test_short_lines(self) -> None:
        """Verifies vowels will force a newline, improving the diffs."""
        txt = "groceries:\ncherry banana apple date eggplant fennel"
        self.assertEqual(
            self.scraper._short_lines(txt),
            """groceries:

======
cherry banana
apple date
eggplant fennel""",
        )
