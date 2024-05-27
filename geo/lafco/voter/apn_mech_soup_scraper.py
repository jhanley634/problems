#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Downloads 4-digit APN prefixes from San Mateo County's assessor website.
This gives us an APN --> address mapping.
"""


import mechanicalsoup

PROPERTY_MAPS_PORTAL = "https://gis.smcgov.org/Html5Viewer/?viewer=raster"

# (Pdb) p browser.session.headers
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"


def step1_find_by_apn() -> None:
    """Click on "Find Parcels by APN"."""
    browser = mechanicalsoup.StatefulBrowser(user_agent=UA, raise_on_404=True)
    browser.open(PROPERTY_MAPS_PORTAL)
    assert browser.url == PROPERTY_MAPS_PORTAL

    post_url = "https://gis.smcgov.org/Geocortex/Essentials/REST/sites/RASTER_SQLMK2/workflows/SearchParcelsByAPN/run"
    browser.request("POST", post_url)
    # Enter a complete, or partial
    # base64 from 2nd request has file type of OpenPGP Public Key

    apn0631_url = (
        "https://gis.smcgov.org/Geocortex/Essentials/REST/TempFiles/Export.csv"
    )
    headers = {
        "guid": "e9c6d324-83c3-4ba1-bfd9-47f536499a01",
        "contentType": "text/csv",
        "Referer": "https://gis.smcgov.org/Html5Viewer/?viewer=raster",
    }
    cookies = {
        "Cookie-E": "1147539628.47873.0000",
    }
    params: dict[str, str] = {}
    browser.open(apn0631_url, headers=headers, cookies=cookies, params=params)
    print(browser.page)
    # breakpoint()


if __name__ == "__main__":
    step1_find_by_apn()
