# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path
import re

from bs4 import BeautifulSoup
import requests

CACHE_DIR = Path("/tmp/web_cache")
CACHE_DIR.mkdir(exist_ok=True)
_FNAME_RE = re.compile(r"^[\w.-]+$")  # no crazy characters like [?&%=]
_TRIM_PREAMBLE_RE = re.compile(r"^.*AUDIO VERSION *", re.DOTALL)


def _cache_file_for(url: str) -> Path:
    ret = CACHE_DIR / Path(url).name
    assert _FNAME_RE.search(ret.name)
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


def squish(s: str) -> str:
    """Remove dup whitespace from a string."""
    return " ".join(s.split())
