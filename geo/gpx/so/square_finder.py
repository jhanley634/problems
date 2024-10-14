#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


# based on https://stackoverflow.com/questions/77902878/problem-with-opencv-to-recognize-numbers-and-digits-on-video
from pathlib import Path
import io

from beartype import beartype
from PIL import Image, ImageOps
from requests_cache import CachedSession
import cv2
import numpy as np

temp = Path("/tmp")


@beartype
def get_image(url: str = "https://i.stack.imgur.com/bhrAt.png") -> Image.Image:
    cache_dir = temp / "url"
    session = CachedSession(cache_name=f"{cache_dir}/requests_cache", expire_after=7200)
    buf = io.BytesIO(session.get(url).content)
    return Image.open(buf)


@beartype
def main() -> None:
    img = ImageOps.grayscale(get_image())
    assert (1671, 928) == img.size
    assert "L" == img.mode

    a = np.array(img.getdata(), dtype=np.uint8).reshape(tuple(reversed(img.size)))
    print(a.shape, a.dtype, a.min(), a.max())

    thresh = np.array(
        cv2.threshold(a, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    )
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )[-2:]
    for idx, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        roi = thresh[y : y + h, x : x + w]
        h = h if h > 0 else 1
        aspect = round(w / h, 4)
        if w * h > 8_000 and 1.81 < aspect < 1.85:
            print(idx, roi.shape, aspect)
            cv2.imwrite(temp / f"{idx}.jpg", roi)

    cv2.imshow("img", thresh)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
