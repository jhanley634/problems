# Copyright 2024 John Hanley. MIT licensed.
import json
import random
import unittest

from geo.lafco.nominatim_facade import NominatimCached


class NominatimFacadeTest(unittest.TestCase):
    @staticmethod
    def get_random_test_addr() -> str:
        house_num = random.randint(100, int(1e6))
        return f"{house_num} O'Connor St, Menlo Park CA 94025"

    def unused_test_get_random_test_addr(self) -> None:
        geo = NominatimCached()
        c = geo.query_count
        print(geo.geocode(self.get_random_test_addr()))
        self.assertEqual(c + 1, geo.query_count)

    def test_query(self) -> None:
        geo = NominatimCached()
        c = geo.query_count

        row = geo.geocode("500 West Elm Street, Carbondale, IL 62901")
        assert row
        self.assertEqual(
            (
                "500, West Elm Street, Carbondale,"
                " Jackson County, Illinois, 62901, United States"
            ),
            json.loads(row.json_result)["display_name"],
        )
        self.assertEqual(c + 0, geo.query_count)  # local db cache hit
