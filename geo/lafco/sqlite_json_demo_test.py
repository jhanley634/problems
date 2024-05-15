# Copyright 2024 John Hanley. MIT licensed.
import unittest

from sqlalchemy import JSON, Text, text
from sqlalchemy.orm import Session, declarative_base, mapped_column
import requests
import sqlalchemy as sa

Base = declarative_base()


class JsonDemo(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "json_demo"

    st_city = mapped_column(Text, primary_key=True)
    json_result = mapped_column(JSON)


class Demo:
    def __init__(self) -> None:
        self.engine = sa.create_engine("sqlite:////tmp/k/json_demo.db")
        metadata = sa.MetaData()
        metadata.create_all(self.engine, tables=[JsonDemo.__table__])
        self.base_url = "https://api.zippopotam.us"

    def fetch_and_store_city(self, st_city: str = "ca/belmont") -> JsonDemo:
        st_city = st_city.upper()
        url = self.base_url + "/us/" + st_city
        resp = requests.get(url)
        with Session(self.engine) as sess:
            existing = sess.get(JsonDemo, st_city)
            if existing:
                sess.delete(existing)
            sess.add(
                JsonDemo(
                    st_city=st_city,
                    json_result=resp.json(),
                )
            )
            sess.commit()
            row = sess.get(JsonDemo, st_city)
            assert row
            return row


class JsonDemoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.demo = Demo()

    def test_city_data(self) -> None:
        r = self.demo.fetch_and_store_city()
        self.assertEqual("CA/BELMONT", r.st_city)
        self.assertEqual("Belmont", r.json_result["place name"])
        places = r.json_result["places"]
        self.assertEqual(2, len(places))
        self.assertEqual("94002", places[0]["post code"])
        self.assertEqual("94003", places[1]["post code"])
        self.assertEqual(
            ["latitude", "longitude", "place name", "post code"],
            sorted(places[0].keys()),
        )

    def test_city_with_spaces(self) -> None:
        r = self.demo.fetch_and_store_city("ca/menlo park")
        self.assertEqual("CA/MENLO PARK", r.st_city)
        self.assertEqual("Menlo Park", r.json_result["place name"])
        places = r.json_result["places"]
        self.assertEqual(3, len(places))
        self.assertEqual("94025", places[0]["post code"])
        self.assertEqual("94026", places[1]["post code"])
        self.assertEqual("94029", places[2]["post code"])

    def test_json_deref_operator(self) -> None:
        self.demo.fetch_and_store_city()

        select = (
            "SELECT json_result ->> 'place name'"
            " FROM json_demo"
            " WHERE st_city = 'CA/BELMONT'"
        )
        with Session(self.demo.engine) as sess:
            self.assertEqual(
                ("Belmont",),
                sess.execute(text(select)).fetchone(),
            )
            self.assertEqual(
                ('"Belmont"',),
                sess.execute(text(select.replace(">>", ">"))).fetchone(),
            )

            q = sa.select(JsonDemo.json_result["place name"]).filter(
                JsonDemo.st_city == "CA/BELMONT"
            )
            self.assertEqual(
                ("Belmont",),
                sess.execute(q).fetchone(),
            )

    def test_api_json_content(self) -> None:
        resp = requests.get("https://api.zippopotam.us/us/CA/BELMONT")
        resp.raise_for_status()
        self.assertEqual("application/json", resp.headers["Content-Type"])
        self.assertEqual("utf-8", resp.encoding)
        self.assertEqual("Belmont", resp.json()["place name"])

        d = {
            "country abbreviation": "US",
            "places": [
                {
                    "place name": "Belmont",
                    "longitude": "-122.2927",
                    "post code": "94002",
                    "latitude": "37.5174",
                },
                {
                    "place name": "Belmont",
                    "longitude": "-122.3348",
                    "post code": "94003",
                    "latitude": "37.3811",
                },
            ],
            "country": "United States",
            "place name": "Belmont",
            "state": "California",
            "state abbreviation": "CA",
        }
        self.assertEqual(d, resp.json())
