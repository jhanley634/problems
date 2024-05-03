# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO
from typing import Any
import struct

from beartype import beartype
from beartype.typing import Iterator
from numpy import dtype
from numpy.typing import NDArray
import numpy as np


@beartype
def _get_codec(s: str) -> tuple[int, int, str]:
    """Returns (bytes_per_char, bom_bytes_to_strip, codec)"""
    if s == "" or (max_val := max(map(ord, s))) < 128:
        return 1, 0, "ascii"

    n = 1 + max_val.bit_length() // 8
    assert 2 <= n <= 4, n
    if n == 2:
        return 2, 2, "utf-16"
    else:
        return 4, 4, "utf-32"


@beartype
def string_to_array(s: str) -> NDArray[np.uint8]:
    _, strip, codec = _get_codec(s)
    buf = BytesIO(s.encode(codec)).getbuffer()
    return np.frombuffer(buf[strip:], dtype=np.uint8)


@beartype
class TombstoneString:
    SENTINEL: int = 255

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
        self._size, self._strip, self._codec = _get_codec(s)

        self._string = string_to_array(s)

    def _slice_chars(self, r: range) -> Iterator[str]:
        """Yields chars in range r, skipping tombstones."""
        sz = self._size
        fmt = "BHII"[sz - 1]
        i = r.start
        n = len(r)
        while n > 0 and i * sz < len(self._string):
            if self._string[i * sz] != self.SENTINEL:
                buf = self._string[i * sz : (i + 1) * sz].tobytes()
                val = struct.unpack(fmt, buf)[0]
                yield chr(val)
                n -= 1
            i += 1

    def __str__(self) -> str:
        a = np.array(self._string, dtype=np.uint8)
        a = a[a != self.SENTINEL]
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
        assert r.stop * self._size <= len(self._string)
        n = len(r)  # We must blank out this many non-tombstone chars.
        i = r.start
        while n > 0:
            if self._string[i * self._size] != self.SENTINEL:
                for j in range(self._size):
                    self._string[i * self._size + j] = self.SENTINEL
                n -= 1
            i += 1

    def index(self, sub: str, start: int = 0) -> int:
        """Returns the index of the first occurrence of sub in s.

        Raises ValueError if the substring is not found.

        The start index includes tombstones; it is different from str() output.
        """

        # substring, serialized
        sub_ser = np.frombuffer(
            BytesIO(sub.encode(self._codec)).getbuffer()[self._strip :],
            dtype=np.uint8,
        )
        assert len(sub_ser) == len(sub) * self._size

        if start + len(sub_ser) > len(self._string):
            sub_ser = sub_ser[: len(self._string) - start]
        return self._index1(sub_ser, start * self._size)

    def _index1(self, sub_ser: np.ndarray[Any, dtype[np.uint8]], start_ser: int) -> int:
        for i in range(start_ser, len(self._string)):
            if self._string[i] == self.SENTINEL:
                continue
            if self._index2(i, sub_ser):
                return i // self._size
        raise ValueError(f"{sub_ser} not found")

    def _index2(self, i: int, sub_ser: np.ndarray[Any, dtype[np.uint8]]) -> bool:
        for j, ch in enumerate(sub_ser):
            if self._string[i + j] == self.SENTINEL:
                continue
            if self._string[i + j] != ch:
                return False
        return True


def lorem_ipsum_article(
    *, size: int = 1_000_000, bad_word: str = "moo", boiler_size: int = 1_000
) -> str:
    """Generates (boring) article text of at least the specified size."""
    # cf https://codereview.stackexchange.com/questions/286290/repeatedly-remove-a-substring-quickly
    # and http://www.usaco.org/index.php?page=viewproblem2&cpid=526
    assert len(bad_word) > 2
    split = 2
    bad_word += bad_word[:split] + bad_word + bad_word[split:]
    assert "moomomooo" == bad_word, bad_word
    boilerplate = "a" * boiler_size  # Yup, even more boring than "lorem ipsum dolor".
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

    def censor(self, bad_word: str) -> int:
        """Deletes all occurrences of bad_word from the article, per USACO olympiad rules."""
        n = i = 0
        try:
            while True:
                # We back up by len(bad_word) for cases like "momooo", while avoiding negatives.
                i = max(0, self._article.delete_word(bad_word, i) - len(bad_word))
                n += 1

        except ValueError:
            return n
