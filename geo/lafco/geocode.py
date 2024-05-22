# Copyright 2024 John Hanley. MIT licensed.

from collections import namedtuple
import json
import re

from geopy import ArcGIS
from sqlalchemy.orm import Session
import sqlalchemy as sa

from geo.lafco.model import Location
from geo.lafco.nominatim_facade import NominatimCached

LocTuple = namedtuple("LocTuple", "house_num street city county state zip country")


class Geocoder:

    menlo = "Menlo Park CA 94025"
    epa = "East Palo Alto CA 94033"

    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    # df['location'] = df['name'].apply(geocode)

    def __init__(self) -> None:
        # self.geolocator = NominatimCached()
        self.geolocator = ArcGIS()
        self.engine = sa.create_engine("sqlite:////tmp/geocode.db")
        metadata = sa.MetaData()
        metadata.create_all(self.engine, tables=[Location.__table__])

    @staticmethod
    def round5(n: float) -> float:
        return round(n, 5)

    @classmethod
    def canonical(cls, addr: str) -> str:
        loc = cls.get_loc_tuple(addr)
        return f"{loc.house_num} {loc.street}, {loc.city} {loc.state}"

    @classmethod
    def get_loc_tuple(cls, addr: str) -> LocTuple:
        addr = cls.upper(addr)
        # addr = addr.replace(", SAN MATEO COUNTY, ", " ")
        addr = addr.replace(", CALIFORNIA", ", CA")
        # addr = addr.removesuffix(", UNITED STATES")
        return LocTuple(*addr.split(", "))

    @staticmethod
    def upper(addr: str) -> str:
        return addr.replace("'", "").upper()

    valid_addr_re = re.compile(r" CA (\d{5})$")

    def get_location(self, addr: str) -> Location | None:
        addr = self.upper(addr)
        m = self.valid_addr_re.search(addr)
        assert m, addr
        with Session(self.engine) as sess:
            loc = sess.get(Location, addr)
            if not loc:
                result = self.geolocator.geocode(addr)
                loc = Location(
                    addr_upper=self.upper(addr),
                    addr=addr,
                    lat=self.round5(result.latitude),
                    lon=self.round5(result.longitude),
                )
                sess.add(loc)
                sess.commit()

            return sess.get(Location, addr)

    def get_nominatim_location(self, addr: str) -> Location | None:
        addr = self.upper(addr)
        m = self.valid_addr_re.search(addr)
        assert m, addr
        with Session(self.engine) as sess:
            loc = sess.get(Location, addr)
            if not loc:
                self._deal_with(sess, addr)
            return sess.get(Location, addr)

    def _deal_with(self, sess: Session, addr: str) -> None:
        def clean_street(street: str) -> str:
            return re.sub(r" STREET$", " ST", street)

        def clean_state(state: str) -> str:
            return re.sub(r"^CALIFORNIA$", "CA", state)

        geo_loc = self.geolocator.geocode(addr)
        if not geo_loc:
            print(f"Could not geocode {addr}")
            return None

        m = re.search(r"^(\d+) ([\w -]+), ([\w ]+) (\w{2,}) (\d{5})$", addr)
        assert m, addr
        j = json.loads(geo_loc.json_result)
        tup = LocTuple(*(self.upper(j["display_name"]).split(", ")))
        addr = f"{tup.house_num} {clean_street(tup.street)}, {tup.city} {clean_state(tup.state)} {tup.zip}"
        loc = Location(
            addr_upper=self.upper(addr),
            addr=addr,
            zipcode=tup.zip,
            lat=self.round5(float(j["lat"])),
            lon=self.round5(float(j["lon"])),
        )
        sess.add(loc)
        sess.commit()
