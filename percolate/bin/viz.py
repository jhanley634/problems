#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2021 John Hanley. MIT licensed.
import networkit as nk
import streamlit as st

from percolate.two_d_percolation import Perc


def main():
    st.write('Hi!')
    p = Perc(3, 2)
    st.write(p.g.numberOfNodes(), p.g.numberOfEdges())
    print('')
    nk.overview(p.g)


if __name__ == '__main__':
    main()
