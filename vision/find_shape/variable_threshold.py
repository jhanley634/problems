#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
import cv2
import streamlit as st

from vision.find_shape.find_ngons import urls
from vision.find_shape.web_image import WebImage


@st.cache
def _read_image(img_idx: int):
    return cv2.imread(WebImage(urls[img_idx]).image())


def main():
    img_idx = st.slider('image #', 0, len(urls) - 1)
    st.write(urls[img_idx])

    ksize = st.slider('kernel_size', 1, 20)
    sigma = st.slider('sigma', 1, 90)

    # We want an odd number here.
    if ksize % 2 == 0:
        ksize += 1

    img = _read_image(img_idx)
    blur = cv2.GaussianBlur(img, ksize=(ksize, ksize), sigmaX=sigma)
    st.image(blur)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)


if __name__ == '__main__':
    main()
