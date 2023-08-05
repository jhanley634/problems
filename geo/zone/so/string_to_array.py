# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO
from operator import itemgetter
from typing import Generator, Iterator
import struct

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


def string_to_array(s: str) -> np.ndarray:
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
        """

        # each char has size of 1, 2, or 4 bytes
        self._size, _, self._codec = _get_codec(s)

        self._string = string_to_array(s)

    def _slice_chars(self, r: range) -> Iterator[tuple[str, ...]]:
        sz = self._size
        fmt = "BHLL"[sz - 1]
        buf = self._string[r.start * sz : r.stop * sz].tobytes()
        u = struct.iter_unpack(fmt, buf)
        yield from map(chr, map(itemgetter(0), u))

    def _slice_chars_orig(self, r: range) -> Generator[str, None, None]:
        for i in r:
            yield self._get_char(i)

    def _get_char(self, i: int) -> str:
        acc = 0
        for j in range(self._size):
            acc = (acc << 8) | self._string[i * self._size + j]
        return chr(acc)

    def __str__(self) -> str:
        a = np.array([v for v in self._string if v != self.SENTINEL], dtype=np.uint8)
        return a.tobytes().decode(self._codec)

    def delete(self, r: range) -> None:
        """Efficiently deletes the chars in range r, even if s is big."""
        for i in r:
            for j in range(self._size):
                self._string[i * self._size + j] = self.SENTINEL
