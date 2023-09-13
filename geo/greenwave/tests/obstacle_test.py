from operator import attrgetter
import unittest

from sortedcontainers import SortedKeyList

from geo.greenwave.demo import Car, City


class ObstacleTest(unittest.TestCase):
    def test_sorted_obstacles(self) -> None:
        seg = City(2, 1).blocks[0].road_segments[0]

        cars = SortedKeyList(key=attrgetter("position"))
        for i in range(7):
            cars.add(Car(seg, float(i)))
            cars[-1].update(1.0)
        self.assertEqual(7, len(cars))
        self.assertEqual(
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            list(map(attrgetter("position"), cars)),
        )

        idx = cars.bisect_key_left(3.0)
        self.assertEqual(7, idx)
