# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO

import numpy as np


def _get_codec(s: str) -> (int, str):
    """Returns (bom_bytes_to_strip, codec)"""
    if s == "" or (max_val := max(map(ord, s))) < 128:
        return (0, "ascii")

    match 1 + max_val.bit_length() // 8:
        case 1:
            return 0, "latin-1"
        case 2:
            return 2, "utf-16"
        case 3 | 4:
            return 4, "utf-32"
        case _:
            raise ValueError(f"max_val {max_val} not supported")


def string_to_array(s: str) -> np.ndarray:
    strip, codec = _get_codec(s)
    buf = BytesIO(s.encode(codec)).getbuffer()
    return np.frombuffer(buf[strip:], dtype=np.uint8)
