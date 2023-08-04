# Copyright 2023 John Hanley. MIT licensed.

from io import BytesIO

import numpy as np


def string_to_array(s: str) -> np.ndarray:
    a = np.frombuffer(BytesIO(s.encode("utf-8")).getbuffer(), dtype=np.uint8)
    return a
