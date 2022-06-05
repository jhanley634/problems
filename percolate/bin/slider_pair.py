#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2022 John Hanley. MIT licensed.
from uszipcode import SearchEngine
import pandas as pd
import streamlit as st


@st.cache(hash_funcs={SearchEngine: lambda x: str(x)})  # fixes "weakref" diagnostic
def _get_search_engine():
    """Returns a zipcode search engine offering "comprehensive" details, connected to sqlite backend.
    """
    comp = SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive
    se = SearchEngine(simple_or_comprehensive=comp)

    menlo_park = se.by_zipcode(94025)  # just checking...
    assert menlo_park.population == 40_526

    return se


def main():
    lo = st.slider('low', min_value=1, max_value=120)
    hi = st.slider('high', min_value=1, max_value=120, value=114)
    se = _get_search_engine()

    scale = 1000
    df = pd.DataFrame([dict(city=z.major_city,
                            zip=z.zipcode,
                            pop=int(z.population / scale) * scale)
                       for z in se.by_population(lo * scale, hi * scale, returns=12)])
    st.write(df)


if __name__ == '__main__':
    main()
