# Copyright 2024 John Hanley. MIT licensed.
import math
import unittest

from geopy.geocoders import ArcGIS
from sqlalchemy.orm import Session

from geo.lafco.geocode import Geocoder
from geo.lafco.lafco_util import _with_dashes
from geo.lafco.model import ApnAddress, Owner
from geo.lafco.table_apn_address import create_table_apn_address
from geo.lafco.table_owner import create_table_owner


class GeocodeTest(unittest.TestCase):

    oconnor = "217 O'Connor St, Menlo Park CA"

    # def test_nominatum(self) -> None:
    #     loc = Nominatim(user_agent=UA).geocode(self.oconnor)
    #     self.assertEqual(
    #         "217, O'Connor Street, Menlo Park,"
    #         " San Mateo County, California, 94301, United States",
    #         loc.address,
    #     )
    #     self.assertEqual(37.461, round(loc.latitude, 3))

    def test_arcgis(self) -> None:
        g = ArcGIS()
        loc = g.geocode(self.oconnor)
        self.assertEqual(37.46139, round(loc.latitude, 5))
        self.assertEqual(-122.15031, round(loc.longitude, 5))

    def test_canonical(self) -> None:
        returned_address = (
            "217, OCONNOR STREET, MENLO PARK,"
            " SAN MATEO COUNTY, CALIFORNIA, 94301, UNITED STATES"
        )
        self.assertEqual(
            "217 OCONNOR STREET, MENLO PARK CA",
            Geocoder.canonical(returned_address),
        )

    def test_geocode(self) -> None:
        g = Geocoder()
        loc = g.get_location(f"101 Donohoe St, {g.menlo}")
        # loc = g.get_location(f"173 Oak Ct, {g.menlo}")
        self.assertEqual(
            "101 DONOHOE ST, MENLO PARK CA 94025 (37.46389, -122.1512)",
            str(loc),
        )
        self.assertEqual(37.464, round(loc.lat, 3))

        loc = g.get_location(f"325 Oak Ct, {g.menlo}")
        self.assertEqual(
            "325 OAK CT, MENLO PARK CA 94025 (37.45911, -122.14843)",
            str(loc),
        )
        g.engine.dispose()

    def test_round5(self) -> None:
        self.assertEqual(3.14159, Geocoder.round5(math.pi))

    def unused_test_apn_address(self) -> None:
        engine = create_table_apn_address()
        with Session(engine) as sess:
            aa = sess.get(ApnAddress, "063-090-070")
            self.assertEqual(
                "063-090-070 1423 BAY RD, EAST PALO ALTO",
                repr(aa),
            )
        engine.dispose()

    def unused_test_owner(self) -> None:
        self.assertEqual("063-492-490", _with_dashes("063492490"))

        engine = create_table_owner()
        with Session(engine) as sess:
            owner = sess.get(Owner, "063-090-070")
            self.assertEqual(
                "063-090-070  ARCHDIOCESE OF S F PARISH:  1423 BAY RD, SAN FRANCISCO CA 94109",
                repr(owner),
            )
        engine.dispose()
