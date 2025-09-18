# Copyright 2023 John Hanley. MIT licensed.
import re
import unittest

from geo.zone.transcript.sync_scripts import (
    _TRIM_PREAMBLE_RE,
    _cache_file_for,
    get_html_text,
    get_markdown_text,
    get_markdown_words,
    get_story_text,
    get_web_text,
    squish,
)

# ruff: noqa: RUF001


class SyncScriptsTest(unittest.TestCase):
    fuego_url = "https://clarkesworldmagazine.com/buckell_07_09/"

    def test_sync_scripts(self) -> None:
        # Force a cache miss.
        fspec = _cache_file_for(self.fuego_url)
        fspec.unlink(missing_ok=True)

        self.assertGreater(len(get_html_text(self.fuego_url)), 91427)

        expected = (
            "Placa del Fuego by Tobias S. Buckell : Clarkesworld Magazine"
            " – Science Fiction & Fantasy Skip to content ClarkesworlD"
            " SCIENCE FICTION & FANTASY MAGAZINE ☰MENU About Us Subscribe"
            " Back Issues Cover Gallery Podcast Submissions Mailing List"
            " Support Us Advertising × ABOUT US SUBSCRIBE BACK ISSUES COVER"
            " GALLERY PODCAST SUBMISSIONS MAILING LIST SUPPORT US ADVERTISING"
            " BROWSE BY FICTION AUDIO FICTION ARTICLES INTERVIEWS AWARDS & RECOGNITION"
            " AUTHORS & ARTISTS EXPLORE RANDOM STORY RANDOM PODCAST SEARCH Search for:"
            " FOLLOW US ON Issue 34 – July 2009 8420 words, novelette Placa del Fuego"
            " by Tobias S. Buckell AUDIO VERSION Tiago would normally have"
            " taken his cut of the picked pockets and stopped right here"
            " at the Seaside Plaza. On the very edge, past the"
        )
        self.maxDiff = None
        prefix = 20 + get_html_text(self.fuego_url).index("very edge")
        self.assertEqual(
            expected, squish(get_web_text(get_html_text(self.fuego_url)[:prefix]))
        )

        expected = _TRIM_PREAMBLE_RE.sub("", expected)
        text = _TRIM_PREAMBLE_RE.sub("", get_story_text(self.fuego_url)).lstrip()
        self.assertEqual(f"{expected}", text[:133])
        self.assertTrue(text.startswith(expected))

    def test_regex_dotall(self) -> None:
        till_eof_re = re.compile(r"def.*", re.DOTALL)
        s = "abc\ndef\nghi\n"
        self.assertEqual("abc\nz", till_eof_re.sub("z", s))

        till_eof_re = re.compile(r"^def.*", re.DOTALL)
        self.assertIsNone(till_eof_re.search(s))

        till_eof_re = re.compile(r"^def.*", re.DOTALL | re.MULTILINE)
        self.assertEqual("abc\nz", till_eof_re.sub("z", s))

    def test_get_markdown_text(self) -> None:
        md = get_markdown_text(self.fuego_url)
        self.assertTrue(md.startswith("Tiago would "))
        self.assertTrue(md.endswith(" a chance just like this."))

    def test_get_markdown_words(self) -> None:
        words = list(get_markdown_words(self.fuego_url))
        self.assertEqual(8_435, len(words))
        self.assertEqual("Tiago", words[0])
        self.assertEqual(["this.\n", "EOF"], words[-2:])

        for word in words:
            if "\n" in word:
                self.assertTrue(word.endswith("\n"))
                self.assertEqual(1, word.count("\n"))
