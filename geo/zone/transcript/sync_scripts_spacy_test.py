import re

from geo.zone.transcript.sync_scripts_spacy import get_story_sentences, get_story_tokens
from geo.zone.transcript.sync_scripts_test import SyncScriptsTest


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

    def test_sentences(self, verbose: bool = False) -> None:
        for sent in get_story_sentences(self.fuego_url):
            if verbose:
                print(sent, end="")
