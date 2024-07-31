#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from io import StringIO
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
import requests


def parse_out_proxies(soup: BeautifulSoup) -> pd.DataFrame:
    table = soup.find_all("table")[0]
    return pd.read_html(StringIO(str(table)))[0]


def proxy_report(url: str = "https://free-proxy-list.net/") -> None:
    countries = r"^(US|CA)$"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    prox = parse_out_proxies(soup)
    prox = prox[prox.Anonymity == "elite proxy"]
    prox = prox[prox.Https == "yes"]
    prox = prox[prox.Code.str.fullmatch(countries)]
    print(prox)
    out_file = Path("/tmp/proxies.csv")
    prox.drop(columns=["Last Checked"]).to_csv(out_file, index=False)


if __name__ == "__main__":
    proxy_report()
