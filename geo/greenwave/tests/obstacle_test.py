import unittest

from geo.greenwave.demo import Car


class ObstacleTest(unittest.TestCase):
    def test_sorted_obstacles(self) -> None:
        car = Car(None, 1)
