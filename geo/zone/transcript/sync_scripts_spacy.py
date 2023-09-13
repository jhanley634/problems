# Copyright 2023 John Hanley. MIT licensed.
from typing import Generator
import re

from spacy import Language
from spacy.cli import download
from spacy.tokens import Span
import spacy

from geo.zone.transcript.sync_scripts import get_story_text


def clean_text_for_spacy(text: str) -> str:
    """Remove non-breaking spaces, etc."""
    non_breaking_space_xlate = str.maketrans(
        "\xa0", " "
    )  # Turn non-breaking spaces into spaces.
    text = text.translate(non_breaking_space_xlate)
    text = re.sub(r"\. \. \. *", "...", text)
    # Extra space helps with sentence segmentation of dialog.
    return text.replace("\n", " \n")


def load_language_model(name: str = "en_core_web_sm") -> Language:
    try:
        return _downlod_then_load_model(name, do_download=False)
    except OSError:  # Can't find model.... It doesn't seem to be a Python package
        return _downlod_then_load_model(name, do_download=True)


def _downlod_then_load_model(name, do_download: bool):
    if do_download:
        download(name)
    return spacy.load(name)


def get_story_tokens(url: str) -> Generator[str, None, None]:
    """Generates both words and paragraph breaks."""
    nlp = load_language_model()
    doc = nlp(clean_text_for_spacy(get_story_text(url)))

    # No non-breaking spaces, please.
    whitespace_xlate = str.maketrans("", "", "\t \xa0")

    for token in doc:
        if token.is_space:
            text = token.text.translate(whitespace_xlate)[:2]
            # Alternative to newlines at this point would be the empty string.
            if text in ("\n", "\n\n"):
                yield text
        else:
            yield token.text


def get_story_sentences(url: str) -> Generator[Span, None, None]:
    nlp = load_language_model()
    doc = nlp(clean_text_for_spacy(get_story_text(url)))

    yield from doc.sents
