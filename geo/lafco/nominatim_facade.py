# Copyright 2024 John Hanley. MIT licensed.
"""
This module is a facade for the Nominatim geocoder, enforcing some pre-conditions.
1. Cache results, that is, never send the geocoder the same address twice.
2. Rate limit requests to one per second, to avoid being banned.
"""
from collections import namedtuple
from pathlib import Path
import json
import random
import re
import unittest

from geopy.geocoders import Nominatim
from geopy.location import Location
from sqlalchemy import Float, Integer, Text
from sqlalchemy.orm import Session, declarative_base, mapped_column
import sqlalchemy as sa

Base = declarative_base()


class NominatimQuery(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "nominatim_query"

    query = mapped_column(Text, primary_key=True)
    display_name = mapped_column(Text, index=True)
    lat = mapped_column(Float, index=True)
    lon = mapped_column(Float, index=True)
    json_result = mapped_column(Text)


class NominatimGeocoder:

    lafco_dir = Path("~/Desktop/lafco").expanduser()
    UA = "SMClafco"

    def __init__(self) -> None:
        assert self.lafco_dir.is_dir()
        self.engine = sa.create_engine(f"sqlite:///{self.lafco_dir}/nominatim.db")
        self.geolocator = Nominatim(user_agent=self.UA)
        metadata = sa.MetaData()
        metadata.create_all(self.engine, tables=[NominatimQuery.__table__])

    @staticmethod
    def canonical(addr: str) -> str:
        return addr.replace("'", "").upper()

    def geocode(self, addr: str) -> dict[str, str] | None:
        addr = self.canonical(addr)
        with Session(self.engine) as sess:
            result = sess.get(NominatimQuery, addr)
            if not result:
                geo_result: Location = self.geolocator.geocode(addr)
                if geo_result:
                    lat, lon = geo_result.raw["lat"], geo_result.raw["lon"]
                    j = json.dumps(geo_result.raw)
                    sess.add(
                        NominatimQuery(
                            query=addr,
                            display_name=geo_result.address,
                            lat=lat,
                            lon=lon,
                            json_result=j,
                        )
                    )
            return sess.get(NominatimQuery, addr) or {"": ""}

    def get_random_test_addr(self) -> str:
        house_num = random.randint(100, int(1e6))
        return f"{house_num} O'Connor St, Menlo Park CA 94025"


class TestNominatimFacade(unittest.TestCase):

    def test_get_random_test_addr(self):
        geocoder = NominatimGeocoder()
        addr = geocoder.get_random_test_addr()
        print(addr)
        print(geocoder.geocode(addr))
