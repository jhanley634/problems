#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
import cv2
import streamlit as st

from vision.find_shape.find_ngons import urls
from vision.find_shape.web_image import WebImage


@st.cache
def _read_image(img_idx: int, new_width=700):
    img = cv2.imread(WebImage(urls[img_idx]).image())
    height, width, depth = img.shape
    assert depth == 3  # color RGB
    assert width > height
    new_height = int(height * new_width / width)  # preserve aspect ratio
    return cv2.resize(img, (new_width, new_height))


def main():
    img_idx = st.slider('image #', 0, len(urls) - 1)
    st.write(urls[img_idx])

    ksize = st.slider('kernel_size', 1, 19, step=2)
    sigma = st.slider('sigma', 1, 1 + ksize)

    # We want an odd number here.
    if ksize % 2 == 0:
        ksize += 1

    img = _read_image(img_idx)
    blur = cv2.GaussianBlur(img, ksize=(ksize, ksize), sigmaX=sigma)
    disp_img = blur
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    if st.checkbox('gray?'):
        disp_img = gray
    st.image(disp_img)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)


if __name__ == '__main__':
    main()
