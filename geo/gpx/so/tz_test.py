# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/289635/goal-writing-effective-unit-tests-to-ensure-a-datetime-conversion-to-from-local/289643

from datetime import timezone as tz
import datetime as dt
import unittest

from dateutil.tz import UTC, gettz, tz, tzutc


class TzTest(unittest.TestCase):
    def test_verify_dst_behavior(self):
        lax = gettz("America/Los_Angeles")
        den = gettz("America/Denver")
        phx = gettz("America/Phoenix")
        fmt = "%Y-%m-%dT%H:%M"
        before = "2024-03-10T12:30"  # half-hour before start of DST
        after = "2024-03-10T04:30"  # half-hour after start of DST
        t1 = dt.datetime.strptime(before, fmt)
        self.assertEqual("2024-03-10 12:30:00", str(t1))  # naïve
        t1 = t1.replace(tzinfo=lax)  # now it is TZ aware
        self.assertEqual("2024-03-10 12:30:00-07:00", str(t1))
        self.assertEqual("2024-03-10 12:30:00-07:00", str(t1.astimezone(lax)))
        self.assertEqual("2024-03-10 19:30:00+00:00", str(t1.astimezone(UTC)))
        utc = dt.datetime(2023, 12, 7, 22, 20, 2, tzinfo=UTC)
        local = utc.astimezone(dt.timezone(dt.timedelta(hours=-8)))
        self.assertEqual(
            local,
            dt.datetime(
                2023, 12, 7, 14, 20, 2, tzinfo=dt.timezone(dt.timedelta(hours=-8))
            ),
        )
