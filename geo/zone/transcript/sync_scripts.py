# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
from typing import Generator
import re

from bs4 import BeautifulSoup
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


def load_language_model(name: str = "en_core_web_sm") -> spacy.Language:
    try:
        spacy.load(name)
    except OSError:
        download(name)
    return spacy.load(name)


def get_story_tokens(url: str) -> Generator[str, None, None]:
    """Generates both words and paragraph breaks."""
    nlp = load_language_model()
    doc = nlp(get_story_text(url))
    for token in doc:
        if token.is_space:
            if ord(token.text[0]) != 160:  # We suppress NBSP tokens.
                if token.text.startswith('\n\xa0\n'):
                    text = '\n\n'
                else:
                    text = token.text.strip(" ")[:2]
                if text in ("\n", "\n\n"):
                    yield text
        else:
            yield token.text


def squish(s: str) -> str:
    """Remove dup whitespace from a string."""
    return " ".join(s.split())


class HapaxLegomenon:
    """"""
