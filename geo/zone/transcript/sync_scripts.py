# Copyright 2023 John Hanley. MIT licensed.
from collections.abc import Generator
from pathlib import Path
import re

from bs4 import BeautifulSoup
from markdownify import markdownify
import requests

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
    return get_web_text(trim_preamble(trim_postamble(get_html_text(url))))


def trim_preamble(html: str) -> str:
    assert "AUDIO " in html, html
    return _TRIM_PREAMBLE_RE.sub("", html)


def trim_postamble(html: str) -> str:
    # marker = '<div class="molongui-clearfix">'
    marker = '<h3 class="about"> </h3>'
    assert marker in html, html
    strip_till_eof_re = re.compile(f"{marker}.*", re.DOTALL)
    return strip_till_eof_re.sub("", html)


def get_markdown_text(url: str) -> str:
    html = trim_preamble(trim_postamble(get_html_text(url)))
    return str(markdownify(html)).strip()


def get_markdown_words(url: str) -> Generator[str, None, None]:
    text = get_markdown_text(url) + "\nEOF"
    text = re.sub(r"(\n)+", r"\1 ", text)
    for word in text.split(" "):
        yield word.lstrip()


def squish(s: str) -> str:
    """Remove dup whitespace from a string."""
    return " ".join(s.split())


class HapaxLegomenon:
    """"""
