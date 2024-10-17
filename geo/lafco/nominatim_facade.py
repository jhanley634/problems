# Copyright 2024 John Hanley. MIT licensed.
"""
This module is a facade for the Nominatim geocoder, enforcing some pre-conditions.
1. Cache results, that is, never send the geocoder the same address twice.
2. Rate limit requests to one per second, to avoid being banned.
"""
from pathlib import Path
from time import sleep, time
from typing import TYPE_CHECKING
import json
import logging
import re

from geopy.geocoders import Nominatim
from sqlalchemy import JSON, Text
from sqlalchemy.orm import Session, declarative_base, mapped_column
import sqlalchemy as sa

if TYPE_CHECKING:
    from geopy.location import Location

Base = declarative_base()

console = logging.StreamHandler()
logging.basicConfig(
    format="%(asctime)s %(levelname)s:  %(message)s",
    level=logging.INFO,
    handlers=[console],
)
logger = logging.getLogger(__name__)
logger.addHandler(console)


class NominatimQuery(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "nominatim_query"

    addr = mapped_column(Text, primary_key=True)
    json_result = mapped_column(JSON)


class NominatimCached:

    lafco_dir = Path("~/Desktop/lafco").expanduser()
    db_cache_file = lafco_dir / "nominatim.db"
    UA = "SMClafco"

    def __init__(self, user_agent: str = UA) -> None:
        assert self.lafco_dir.is_dir()
        self.queried_at = time()
        self.query_count = 0  # cumulative number of API requests
        self.engine = sa.create_engine(f"sqlite:///{self.db_cache_file}")
        self._geolocator = Nominatim(user_agent=user_agent)
        metadata = sa.MetaData()
        metadata.create_all(self.engine, tables=[NominatimQuery.__table__])

    @staticmethod
    def canonical(addr: str) -> str:
        return addr.replace("'", "").upper()

    query_delay_secs = 1.1  # Nominatim's rate limit is 1 per second
    addr_re = re.compile(r"^\d[\wA-Z ,]+ \d{5}$")

    def geocode(self, addr: str) -> NominatimQuery | None:
        addr = self.canonical(addr)
        assert self.addr_re.match(addr), addr
        with Session(self.engine) as sess:
            result = sess.get(NominatimQuery, addr)
            if not result:  # pragma: no cover
                logger.info("sending query for %s", addr)
                sleep(max(0.0, self.query_delay_secs - (time() - self.queried_at)))
                self.query_count += 1
                geo_result: Location = self._geolocator.geocode(addr)
                logger.info("received: %s", geo_result)
                self.queried_at = time()
                if geo_result:
                    # lat, lon = geo_result.raw["lat"], geo_result.raw["lon"]
                    sess.add(
                        NominatimQuery(
                            addr=addr,
                            json_result=json.dumps(geo_result.raw),
                        )
                    )
                    sess.commit()
            return sess.get(NominatimQuery, addr)
