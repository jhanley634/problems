from collections import deque
# Copyright 2023 John Hanley. MIT licensed.
import re
import unittest

from geo.zone.transcript.sync_scripts import (
    _TRIM_PREAMBLE_RE,
    get_html_text,
    get_story_text,
    get_story_tokens,
    get_web_text,
    squish,
)


class SyncScriptsTest(unittest.TestCase):
    fuego_url = "https://clarkesworldmagazine.com/buckell_07_09/"

    def test_sync_scripts(self):
        self.assertEqual(91743, len(get_html_text(self.fuego_url)))

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
        self.assertEqual(
            expected, squish(get_web_text(get_html_text(self.fuego_url)[:18_602]))
        )

        expected = _TRIM_PREAMBLE_RE.sub("", expected)
        text = _TRIM_PREAMBLE_RE.sub("", get_story_text(self.fuego_url)).lstrip()
        self.assertEqual(f"{expected}", text[:133])
        self.assertTrue(text.startswith(expected))

    def test_get_story_tokens(self):
        expected = (
            "Tiago would normally have taken his cut of the picked pockets"
            " and stopped right here at the Seaside Plaza . On the very edge , past"
        )
        self.assertEqual(
            expected,
            (" ".join(list(get_story_tokens(self.fuego_url))[:27])).lstrip(),
        )
        token_re = re.compile(r"^[\w;,.·!?&©/'’‘\"“”:-]+$")
        for token in get_story_tokens(self.fuego_url):
            if token not in ("", "\n", "\n\n"):
                assert token_re.search(token), f">{token}<  {ord(token[0])}"

    def test_sentences(self):
        tokens = deque(get_story_tokens(self.fuego_url))
        while True:
            try:
                i = tokens.index(".") + 1
            except ValueError:
                break
            sentence = [tokens.popleft() for _ in range(i)]
            # print(i, " ".join(sentence).lstrip())
