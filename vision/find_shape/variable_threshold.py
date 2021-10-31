#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
import streamlit as st

from vision.find_shape.find_ngons import urls


def main():
    st.text('Please choose an image:')
    n = st.slider('image #', 0, len(urls) - 1)
    st.write(urls[n])


if __name__ == '__main__':
    main()
