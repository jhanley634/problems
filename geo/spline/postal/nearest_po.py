#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from sqlalchemy import select
from uszipcode import SearchEngine
from uszipcode import SimpleZipcode as Zip


def nearest_post_office() -> None:
    query = select(Zip).where(Zip.zipcode == "10001")
    results = SearchEngine().ses.scalar(query)
    print(results)


if __name__ == "__main__":
    nearest_post_office()
