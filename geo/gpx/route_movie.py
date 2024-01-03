#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.


from geo.gpx.route_viz import _display, _get_chosen_gpx_path, _get_df
from geo.ski.dwell import get_breadcrumbs


def main() -> None:
    _display(_get_df(_get_chosen_gpx_path()))


if __name__ == "__main__":
    main()
