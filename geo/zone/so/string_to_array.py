# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO

import numpy as np


def _get_codec(s: str) -> str:
    if s == "" or (max_val := max(map(ord, s))) < 128:
        return "ascii"

    match 1 + max_val.bit_length() // 8:
        case 1:
            return "latin-1"
        case 2:
            return "utf-16"
        case 3 | 4:
            return "utf-32"
        case _:
            raise ValueError(f"max_val {max_val} not supported")


def string_to_array(s: str) -> np.ndarray:
    a = np.frombuffer(BytesIO(s.encode(_get_codec(s))).getbuffer(), dtype=np.uint8)
    return a
