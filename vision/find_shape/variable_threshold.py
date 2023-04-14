#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
import cv2
import numpy as np
import numpy.typing as npt
import streamlit as st

from vision.find_shape.find_ngons import BLACK, urls
from vision.find_shape.web_image import WebImage


@st.cache
def _read_image(img_idx: int, new_width: int = 700) -> npt.NDArray[np.int_]:
    img = cv2.imread(WebImage(urls[img_idx]).image())
    height, width, depth = img.shape
    assert depth == 3  # color RGB
    new_height = int(height * new_width / width)  # preserve aspect ratio
    return cv2.resize(img, (new_width, new_height))  # type: ignore [no-any-return]


def main() -> None:
    img_idx = st.slider("image #", 0, len(urls) - 1)
    st.write(urls[img_idx])

    ksize = st.slider("kernel_size", 1, 19, step=2)  # We require the size to be odd.
    sigma = st.slider("sigma", 1, 16)

    img = _read_image(img_idx)
    assert len(img.shape) == 3  # (width, height, depth)
    assert img.shape[2] == 3

    blur = cv2.GaussianBlur(img, ksize=(ksize, ksize), sigmaX=sigma)
    disp_img = blur
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    if st.checkbox("gray?"):
        disp_img = gray
    st.image(disp_img)

    thresh_type = cv2.THRESH_OTSU if st.checkbox("Otsu?") else cv2.THRESH_TRIANGLE
    _, threshold = cv2.threshold(gray, 127, 255, thresh_type)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(gray, contours[1:], -1, BLACK, thickness=5)

    st.image(gray)


if __name__ == "__main__":
    main()
