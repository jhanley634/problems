# Copyright 2024 John Hanley. MIT licensed.


from collections import namedtuple
import re

# from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session
import sqlalchemy as sa

from geo.lafco.model import Location

LocTuple = namedtuple("LocTuple", "house_num street city county state zip country")
UA = "SMClafco2"


class Geocoder:

    menlo = "Menlo Park CA 94025"
    epa = "East Palo Alto CA 94033"

    valid_addr_re = re.compile(r" CA (\d{5})$")

    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    # df['location'] = df['name'].apply(geocode)

    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent=UA)
        self.engine = sa.create_engine("sqlite:////tmp/geocode.db")
        metadata = sa.MetaData()
        metadata.create_all(self.engine, tables=[Location.__table__])

    @staticmethod
    def round(n: float) -> float:
        return round(n, 5)

    @staticmethod
    def get_loc_tuple(addr: str) -> LocTuple:
        addr = addr.replace("'", "").replace(", CALIFORNIA", ", CA")
        return LocTuple(*addr.split(", "))

    @classmethod
    def canonical(cls, addr: str) -> str:
        loc = cls.get_loc_tuple(addr)
        return f"{loc.house_num} {loc.street}, {loc.city} {loc.state}"

    @staticmethod
    def _upper(addr: str) -> str:
        return addr.replace("'", "").upper()

    def get_location(self, addr: str) -> Location | None:
        addr = addr.replace("'", "")
        m = self.valid_addr_re.search(addr)
        assert m, addr
        with Session(self.engine) as sess:
            loc = sess.get(Location, self._upper(addr))
            if not loc:
                self._deal_with(sess, addr)
            return sess.get(Location, addr)

    def _deal_with(self, sess: Session, addr: str) -> None:
        geo_loc = self.geolocator.geocode(addr, timeout=3)
        if not geo_loc:
            print(f"Could not geocode {addr}")
            return None

        m = re.search(r"^(\d+) ([\w-]+), (\w+) (\w{2,}) (\d{5})$", addr)
        assert m, addr
        # LocTuple = namedtuple("LocTuple", "house_num street city county state zip country")
        tup = LocTuple(*self.canonical(geo_loc.address).split(", "))
        addr = f"{tup.house_num} {tup.street}, {tup.city} {tup.state} {tup.zip}"
        print(addr)
        loc = Location(
            addr_upper=self.canonical(geo_loc.address).upper(),
            addr=addr,
            zipcode=tup.zip,
            lat=self.round(geo_loc.latitude),
            lon=self.round(geo_loc.longitude),
        )
        sess.add(loc)
        sess.commit()
