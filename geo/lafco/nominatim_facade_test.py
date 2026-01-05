# Copyright 2024 John Hanley. MIT licensed.
import json
import random
import unittest

from geo.lafco.nominatim_facade import TEMP, NominatimCached


class NominatimFacadeTest(unittest.TestCase):
    @staticmethod
    def get_random_test_addr() -> str:
        house_num = random.randint(10_000, int(1e6))
        return f"{house_num} O'Connor St, Menlo Park CA 94025"

    def setUp(self) -> None:
        self.geo = NominatimCached()
        self.assertTrue(self.geo.db_cache_file.exists())
        self.assertEqual(TEMP / "lafco/nominatim.db", self.geo.db_cache_file)

    def test_query(self) -> None:
        self.get_random_test_addr()

        c = self.geo.query_count
        row = self.geo.geocode("500 West Elm Street, Carbondale, IL 62901")
        assert row
        self.assertEqual(
            (
                "500, West Elm Street, Carbondale,"
                " Jackson County, Illinois, 62901, United States"
            ),
            json.loads(row.json_result)["display_name"],
        )
        # local db cache hit
        self.assertIn(self.geo.query_count, {c, c + 1})
