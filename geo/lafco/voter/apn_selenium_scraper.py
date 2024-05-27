#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Downloads 4-digit APN prefixes from San Mateo County's assessor website.
This gives us an APN --> address mapping.
"""


import selenium

PROPERTY_MAPS_PORTAL = "https://gis.smcgov.org/Html5Viewer/?viewer=raster"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"


def step1_find_by_apn() -> None:
    """Click on "Find Parcels by APN"."""
    assert "4.21.0" == selenium.__version__, selenium.__version__


if __name__ == "__main__":
    step1_find_by_apn()
