#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pprint import pp

from sqlalchemy import text
from sqlalchemy.orm import aliased
from uszipcode import SearchEngine
from uszipcode import SimpleZipcode as Zip


def nearest_post_office() -> None:
    # z1 = aliased(Zip)
    # z2 = aliased
    select = """
    SELECT z1.zipcode, z2.zipcode, z1.major_city, z1.state
    FROM simple_zipcode AS z1
    JOIN simple_zipcode AS z2
    ON z1.zipcode < z2.zipcode
    WHERE z2.zipcode <= '01009'
    AND z1.state not in ('PR', 'VI')
    AND z2.state not in ('PR', 'VI')
    """
    query = (
        SearchEngine().ses.execute(text(select))
        # .join(z2, z2.zipcode <= "10010")
        # .where(z1.zipcode < z2.zipcode)
        # .where(z2.zipcode <= "10010")
    )
    print(text(select))
    for result in query.all():
        print(result._asdict())


if __name__ == "__main__":
    nearest_post_office()
