# Copyright 2023 John Hanley. MIT licensed.
import io
import re
import sys

from geo.zone.transcript.sync_scripts_spacy import (
    get_story_sentences,
    get_story_tokens,
    load_language_model,
)
from geo.zone.transcript.sync_scripts_test import SyncScriptsTest

# ruff: noqa: RUF001


class SyncScriptsSpacyTest(SyncScriptsTest):
    def test_get_story_tokens(self) -> None:
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

    def test_model_not_found(self) -> None:
        # suppress spacy's "✘ No compatible package found" message.
        sys.stdout = io.StringIO()

        with self.assertRaises(SystemExit):
            load_language_model("en_nonexistent_model_name")

        sys.stdout = sys.__stdout__  # back to normal

    def test_sentences(self) -> None:
        sentences = list(get_story_sentences(self.fuego_url))
        self.assertEqual(775, len(sentences))  # We have hundreds of spacy Spans.
