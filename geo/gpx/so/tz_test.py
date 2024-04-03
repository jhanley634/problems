# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/289635/goal-writing-effective-unit-tests-for-a-datetime-conversion


import datetime as dt
import unittest

from dateutil.tz import gettz


class TzTest(unittest.TestCase):
    def test_verify_dst_behavior(self) -> None:
        lax = gettz("America/Los_Angeles")
        den = gettz("America/Denver")
        phx = gettz("America/Phoenix")

        # half-hour before start of any DST transitions, PHX matches DEN
        t1 = dt.datetime.fromisoformat("2024-03-10T07:30Z")
        self.assertEqual("2024-03-10 07:30:00+00:00", str(t1))
        self.assertEqual("2024-03-10 00:30:00-07:00", str(t1.astimezone(den)))
        self.assertEqual("2024-03-10 00:30:00-07:00", str(t1.astimezone(phx)))
        self.assertEqual("2024-03-09 23:30:00-08:00", str(t1.astimezone(lax)))

        # after all DST transitions have happened, PHX matches LAX
        t2 = t1 + dt.timedelta(hours=3)
        self.assertEqual("2024-03-10 10:30:00+00:00", str(t2))
        self.assertEqual("2024-03-10 04:30:00-06:00", str(t2.astimezone(den)))
        self.assertEqual("2024-03-10 03:30:00-07:00", str(t2.astimezone(phx)))
        self.assertEqual("2024-03-10 03:30:00-07:00", str(t2.astimezone(lax)))
