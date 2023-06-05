# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from typing import Generator
import re

from bs4 import BeautifulSoup
from spacy import Language
from spacy.cli import download
import requests
import spacy

CACHE_DIR = Path("/tmp/web_cache")
CACHE_DIR.mkdir(exist_ok=True)
_FILENAME_RE = re.compile(r"^[\w.-]+$")  # no crazy characters like [?&%=]
_TRIM_PREAMBLE_RE = re.compile(r"^.*AUDIO VERSION *", re.DOTALL)


def _cache_file_for(url: str) -> Path:
    ret = CACHE_DIR / Path(url).name
    assert _FILENAME_RE.search(ret.name)
    return ret


def get_html_text(url: str) -> str:
    """Return the (possibly cached) HTML text of a web page."""
    fspec = _cache_file_for(url)
    if not fspec.exists():
        fspec.write_text(requests.get(url).text)

    return fspec.read_text()


def get_web_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()


def get_story_text(url: str) -> str:
    html = get_html_text(url)
    assert "AUDIO " in html, html
    html = _TRIM_PREAMBLE_RE.sub("", html)
    return get_web_text(html)


def load_language_model(name: str = "en_core_web_sm") -> Language:
    try:
        return spacy.load(name)
    except OSError:  # Can't find model.... It doesn't seem to be a Python package
        download(name)
        return spacy.load(name)


def clean_text(text: str) -> str:
    """Remove non-breaking spaces, etc."""
    non_breaking_space_xlate = str.maketrans(
        "\xa0", " "
    )  # Turn non-breaking spaces into spaces.
    text = text.translate(non_breaking_space_xlate)
    text = re.sub(r"\. \. \. *", "...", text)
    # Extra space helps with sentence segmentation of dialog.
    return text.replace("\n", " \n")


def get_story_tokens(url: str) -> Generator[str, None, None]:
    """Generates both words and paragraph breaks."""
    nlp = load_language_model()
    doc = nlp(clean_text(get_story_text(url)))

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


def get_story_sentences(url: str) -> Generator[str, None, None]:
    nlp = load_language_model()
    doc = nlp(clean_text(get_story_text(url)))

    yield from doc.sents


def squish(s: str) -> str:
    """Remove dup whitespace from a string."""
    return " ".join(s.split())


class HapaxLegomenon:
    """"""
