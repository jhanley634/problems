#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from pprint import pp
from time import sleep
from typing import Any
import datetime as dt
import json
import os

import requests

TRANSIT = "http://api.511.org/transit"


def query_transit(url: str) -> dict[str, Any]:
    """Given a URL with no credential, returns an API result."""
    assert "?" in url, url
    api_key = os.environ["KEY511"]
    url += f"&api_key={api_key}"
    resp = requests.get(url)
    resp.raise_for_status()
    bom = "\ufeff"
    hdr = resp.headers
    assert hdr["Content-Type"] == "application/json; charset=utf-8"
    assert hdr["Server"] == "Microsoft-IIS/10.0"
    assert resp.text.startswith(bom)  # Grrr. Gee, thanks, μsoft!
    d = json.loads(resp.text.lstrip(bom))
    assert isinstance(d, dict), d
    return d


def query_stop(agency: str = "SC", polling_delay_sec: float = 20.0) -> None:
    while True:
        d = query_transit(f"{TRANSIT}/StopMonitoring?agency={agency}")
        assert 1 == len(d), d
        assert d["ServiceDelivery"]["Status"], d
        assert agency == d["ServiceDelivery"]["ProducerRef"], d

        deliv = d["ServiceDelivery"]["StopMonitoringDelivery"]
        assert len(deliv) >= 4, deliv.keys()
        assert "1.4" == deliv["version"], deliv
        assert deliv["Status"], deliv

        msgs = []
        visits = deliv["MonitoredStopVisit"]
        for visit in visits:
            if visit["RecordedAtTime"] < "1971-":  # invalid
                continue

            journey = visit["MonitoredVehicleJourney"]
            assert 16 == len(journey.keys()), journey.keys()
            assert None is journey["InCongestion"], journey
            msgs.append(_fmt_msg(journey))

            call = journey["MonitoredCall"]
            assert 10 == len(call.keys()), call.keys()
            if not call["AimedArrivalTime"]:
                continue
            aimed = dt.datetime.fromisoformat(call["AimedArrivalTime"])
            if call["ExpectedArrivalTime"] is None:
                continue
            expected = dt.datetime.fromisoformat(call["ExpectedArrivalTime"])
            # print("aimed:   ", aimed)
            # print("expected:", expected, "  ", expected - aimed)
            assert expected - aimed < dt.timedelta(days=1), call

        pp(journey["VehicleLocation"])
        print("\n".join(sorted(msgs)), "\n")
        sleep(polling_delay_sec)


def fmt_lat_lng(location: dict[str, str]) -> str:
    latitude = location["Latitude"] or "0.0"
    longitude = location["Longitude"] or "0.0"
    lat, lng = map(float, (latitude, longitude))
    return f"{lat:.6f}, {lng:.6f}"


def query_vehicle(agency: str = "SC", polling_delay_sec: float = 20.0) -> None:
    d = query_transit(f"{TRANSIT}/VehicleMonitoring?agency={agency}")
    assert 1 == len(d), d
    assert 1 == len(d["Siri"]), d

    svc = d["Siri"]["ServiceDelivery"]
    keys = ["ProducerRef", "ResponseTimestamp", "Status", "VehicleMonitoringDelivery"]
    assert keys == sorted(svc.keys()), svc.keys()
    assert svc["Status"]
    assert agency == svc["ProducerRef"]

    deliv = svc["VehicleMonitoringDelivery"]
    assert 3 == len(deliv.keys()), deliv.keys()
    assert "1.4" == deliv["version"]

    msgs = [
        _fmt_msg(record["MonitoredVehicleJourney"])
        for record in deliv["VehicleActivity"]
        if record["MonitoredVehicleJourney"].get("MonitoredCall")
    ]
    assert sorted(msgs) == msgs, msgs
    print("\n".join(msgs))


def _fmt_msg(journey: dict[str, Any], width: int = 38) -> str:
    pad = " " * width
    call = journey["MonitoredCall"]
    return " ".join(
        [
            journey["VehicleRef"],
            (journey["DirectionRef"] or "-"),
            call["StopPointRef"],  # cf StopPointName
            (journey.get("LineRef") or "-").ljust(10),
            ((journey.get("PublishedLineName") or "-") + pad)[:width],
            (journey["DestinationName"] or "-").ljust(46),
            fmt_lat_lng(journey["VehicleLocation"]),
        ]
    )


if __name__ == "__main__":
    query_vehicle()
