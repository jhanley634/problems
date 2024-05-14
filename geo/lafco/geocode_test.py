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
        loc = g.get_location(f"101 Donohoe St, {g.menlo}")
        # loc = g.get_location(f"217 O'Connor St, {g.menlo}")
        print(loc)

        self.assertEqual(37.453, round(loc.lat, 3))
