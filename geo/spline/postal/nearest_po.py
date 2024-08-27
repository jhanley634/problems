#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pathlib import PosixPath

from sqlalchemy.orm import aliased
from uszipcode import SearchEngine
from uszipcode import SimpleZipcode as Zip


def nearest_post_office() -> None:
    db_file = f"{SearchEngine().db_file_path}"
    assert f"{PosixPath("~/.uszipcode/simple_db.sqlite").expanduser()}" == db_file

    z1 = aliased(Zip)
    z2 = aliased(Zip)
    query = (
        SearchEngine()
        .ses.query(z1.zipcode, z2.zipcode, z1.major_city, z1.state)
        .where(z1.zipcode < z2.zipcode)
        .where(z2.zipcode <= "01009")
    )
    print(query)
    for result in query.all():
        print(result._asdict())


if __name__ == "__main__":
    nearest_post_office()
