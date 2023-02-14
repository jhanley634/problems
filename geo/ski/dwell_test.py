import unittest

from geopy import Point
from geopy.distance import great_circle


class DwellTest(unittest.TestCase):
    def test_distance(self):
        menlo_park = Point(37.453, -122.181)
        san_francisco = Point(37.774, -122.419)
        san_diego = Point(32.715, -117.161)
        self.assertAlmostEqual(0.0, great_circle(menlo_park, menlo_park).miles)
        self.assertAlmostEqual(25.721, great_circle(menlo_park, san_francisco).miles, 3)
        self.assertAlmostEqual(433.124, great_circle(menlo_park, san_diego).miles, 3)
