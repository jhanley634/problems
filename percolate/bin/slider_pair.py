#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2022 John Hanley. MIT licensed.
from sqlite3 import Connection

from uszipcode import SearchEngine
import pandas as pd
import streamlit as st

from percolate.bin.slider_pair_state import prev

# Hoped to fix a "weakref" diagnostic with this dict.
# @st.cache(hash_funcs=_hash_funcs)
_hash_funcs = {
    Connection: id,
    SearchEngine: str,
    # SearchEngine: lambda x: str(x),
}


def _get_search_engine() -> SearchEngine:
    """Returns a zipcode search engine offering "comprehensive" details, connected to sqlite backend."""
    comp = SearchEngine.SimpleOrComprehensiveArgEnum.comprehensive
    se = SearchEngine(simple_or_comprehensive=comp)

    menlo_park = se.by_zipcode(94025)  # just checking...
    assert menlo_park.population == 40_526

    return se


def main() -> None:
    prev_lo = prev["lo"]
    prev_delta = min(prev["hi"] - prev["lo"], 50)

    widget = st.empty()
    lo, hi = widget.slider(
        "high",
        min_value=1,
        max_value=120,
        value=(prev["lo"], prev["hi"]),
    )
    print(hi)

    # We assume mouse will only adjust a single slider per refresh interval.
    if lo != prev_lo:
        lo, hi = widget.slider(
            "high",
            min_value=1,
            max_value=120,
            value=(lo, lo + prev_delta),
        )

    st.write(prev_delta)
    prev["lo"] = lo
    prev["hi"] = hi
    return

    se = _get_search_engine()

    scale = 1000
    df = pd.DataFrame(
        [
            {
                "city": z.major_city, "zip": z.zipcode, "pop": int(z.population / scale) * scale
            }
            for z in se.by_population(lo * scale, hi * scale, returns=12)
        ]
    )
    st.write(df)


if __name__ == "__main__":
    main()
