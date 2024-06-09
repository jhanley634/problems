# Copyright 2024 John Hanley. MIT licensed.
from collections import Counter
from pathlib import Path
import unittest

from geo.gpx.so.tokenizer_simple import get_simple_words, main
from geo.gpx.so.word_publisher import _get_ranks, get_document, get_words


class TokenizerSimpleTest(unittest.TestCase):
    def test_main(self) -> None:
        main(Path("/etc/hosts"))

    def test_get_simple_words(self) -> None:
        self.assertEqual(
            ["Bob", "Burger"],
            list(get_simple_words("Bob's Burger'.")),
        )

    def test_get_words(self) -> None:
        cr = get_document("https://codereview.stackexchange.com/")
        assert cr.startswith("\n<!DOCTYPE html>\n\n\n    <html ")

        w = list(get_words("https://codereview.stackexchange.com/"))[:7]
        self.assertEqual(
            ["doctype", "html", "responsive", "en", "review", "stack", "shortcut"],
            w,
        )

        self.assertEqual([0, 0, 1, 1, 1], list(_get_ranks(Counter("abbba"))))
