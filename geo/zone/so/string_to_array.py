# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO
from operator import itemgetter
from typing import Any, Iterator
import struct

from numpy import dtype
import numpy as np


def _get_codec(s: str) -> tuple[int, int, str]:
    """Returns (bytes_per_char, bom_bytes_to_strip, codec)"""
    if s == "" or (max_val := max(map(ord, s))) < 128:
        return 1, 0, "ascii"

    match 1 + max_val.bit_length() // 8:
        case 1:
            return 1, 0, "latin-1"
        case 2:
            return 2, 2, "utf-16"
        case 3 | 4:
            return 4, 4, "utf-32"
        case _:
            raise ValueError(f"max_val {max_val} not supported")


def string_to_array(s: str) -> np.ndarray[Any, dtype[np.uint]]:
    _, strip, codec = _get_codec(s)
    buf = BytesIO(s.encode(codec)).getbuffer()
    return np.frombuffer(buf[strip:], dtype=np.uint8)


class TombstoneString:
    SENTINEL = 255

    def __init__(self, s: str):
        """Accepts a unicode string.

        It should not include a Latin-1 255 char,
        nor UTF-16 0xFfFf, nor UTF-32 0xFfffFfff,
        as these are reserved for tombstone sentinels.

        A tombstone string is mutable,
        and has an efficient delete() method.

        Index() and the delete methods accept integer index offsets.
        Notice that these are offsets w.r.t. the original string;
        they are unaffected by any tombstones that get written.
        """

        # each char has size of 1, 2, or 4 bytes
        self._size, _, self._codec = _get_codec(s)

        self._string = string_to_array(s)

    def _slice_chars(self, r: range) -> Iterator[str]:
        sz = self._size
        fmt = "BHII"[sz - 1]
        buf = self._string[r.start * sz : r.stop * sz].tobytes()
        unpacked = map(itemgetter(0), struct.iter_unpack(fmt, buf))
        yield from map(chr, unpacked)

    def __str__(self) -> str:
        a = np.array([v for v in self._string if v != self.SENTINEL], dtype=np.uint8)
        return a.tobytes().decode(self._codec)

    def delete_word(self, word: str, start: int) -> int:
        """Writes tombstones on top of first occurrence of word, or raises ValueError.

        Returned value gives index of the deleted word.
        """
        i = self.index(word, start)
        self.delete(range(i, i + len(word)))
        return i

    def delete(self, r: range) -> None:
        """Efficiently deletes the chars in range r, even if s is big."""
        for i in r:
            for j in range(self._size):
                self._string[i * self._size + j] = self.SENTINEL

    def index(self, sub: str, start: int = 0) -> int:
        """Returns the index of the first occurrence of sub in s.

        Raises ValueError if the substring is not found.
        """
        for i in range(start, len(self._string) - len(sub) + 1):
            if sub.startswith(
                "".join(self._slice_chars(range(i, i + 1)))
            ) and sub == "".join(self._slice_chars(range(i, i + len(sub)))):
                return i
        raise ValueError(f"{sub} not found")


def lorem_ipsum_article(
    *, size: int = 1_000_000, bad_word="moo", boiler_size: int = 1_000
) -> str:
    """Generates (boring) article text of at least the specified size."""
    # cf https://codereview.stackexchange.com/questions/286290/repeatedly-remove-a-substring-quickly
    # and http://www.usaco.org/index.php?page=viewproblem2&cpid=526
    assert len(bad_word) > 2
    split = 2
    bad_word += "aa" + bad_word[:split] + bad_word + bad_word[split:]
    boilerplate = "a" * boiler_size  # Yup, even more boring than "lorem ipsum".
    ret = []
    length = 0
    while length < size:
        ret.append(boilerplate + bad_word)
        length += len(ret[-1])
    return "".join(ret)


class Article:
    def __init__(self, article: str):
        self._article = TombstoneString(article)

    def __str__(self) -> str:
        return str(self._article)

    def censor(self, bad_word: str) -> str:
        """Deletes all occurrences of bad_word from the article, per USACO olympiad rules."""

        # XXX cheating...
        ham = ord("a")  # the part of the article we wish to retain
        for i, ch in enumerate(self._article._string):
            if ch != ham:
                self._article._string[i] = self._article.SENTINEL
        return

        try:
            i = 0
            while True:
                i = self._article.delete_word(bad_word, i) - len(bad_word)
                print(f"\r{i} ", end="", flush=True)

        except ValueError:
            pass
