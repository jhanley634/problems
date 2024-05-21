# Copyright 2024 John Hanley. MIT licensed.
import unittest

from geo.lafco.geocode import Geocoder


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
        loc = g.get_location(f"101 Donohoe St, {g.menlo}".replace("94025", "94301"))
        # loc = g.get_location(f"173 Oak Ct, {g.menlo}")
        self.assertEqual(
            "101 DONOHOE ST, MENLO PARK CA 94301 (37.46389, -122.15122)",
            str(loc),
        )
        self.assertEqual(37.464, round(loc.lat, 3))

        loc = g.get_location(f"325 Oak Ct, {g.menlo}".replace("94025", "94301"))
        print(loc)
        self.assertEqual(
            "325 OAK CT, MENLO PARK CA 94025 (37.46389, -122.15122)",
            str(loc),
        )
