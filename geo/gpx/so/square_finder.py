#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

# based on https://stackoverflow.com/questions/77902878/problem-with-opencv-to-recognize-numbers-and-digits-on-video
from pathlib import Path
from pprint import pp
import io

from beartype import beartype
from PIL import Image, ImageEnhance, ImageOps
from requests_cache import CachedSession
import cv2
import numpy as np
import pandas as pd
import pytesseract


@beartype
def get_image(url: str = "https://i.stack.imgur.com/bhrAt.png") -> Image.Image:
    cache_dir = Path("/tmp/k/url")
    session = CachedSession(cache_name=f"{cache_dir}/requests_cache", expire_after=7200)
    buf = io.BytesIO(session.get(url).content)
    return Image.open(buf)


@beartype
def main() -> None:
    img = ImageOps.grayscale(get_image())
    assert (1671, 928) == img.size
    assert "L" == img.mode

    a = np.array(img.getdata())
    print(a.shape, a.dtype, a.min(), a.max())

    CreateImageHeader(img.size, IPL_DEPTH_8U, 3)

    # img.show()


if __name__ == "__main__":
    main()
