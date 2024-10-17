# Copyright 2023 John Hanley. MIT licensed.

from operator import attrgetter
import unittest

from geo.greenwave.demo import Car, City, Obstacle


class ObstacleTest(unittest.TestCase):
    def test_sorted_obstacles(self) -> None:
        seg = City(2, 1).blocks[0].road_segments[0]
        one_second = 1.0

        for i in range(7):
            car = Car(seg, speed_px_per_sec=7.0 - i)
            car.update(one_second, seg)  # update will need a 2nd arg
        self.assertEqual(7, len(Obstacle.fleet))
        self.assertEqual(7, len(seg.obstacles))
        self.assertEqual(
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            list(map(attrgetter("position"), seg.obstacles)),
        )

        idx = seg.obstacles.bisect_left(3.0)
        self.assertEqual(2, idx)
