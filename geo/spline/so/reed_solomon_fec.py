#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from decimal import Decimal
from pprint import pp
import decimal
import json

from reedsolo import RSCodec


def get_msg_chunks(msg: str, size: int = 12) -> bytes:
    chunks = [(i // size, msg[i : i + size]) for i in range(0, len(msg), size)]
    return json.dumps(chunks).encode()


def demo(num_ecc_syms: int = 24) -> None:
    msg = get_msg_chunks(str(get_pi()))
    rsc = RSCodec(num_ecc_syms)
    xmit = rsc.encode(msg)
    assert len(xmit) == len(msg) + num_ecc_syms
    xmit = xmit.replace(b"751058209749", b" " * 12)  # corrupted transmission

    repaired, *_ = rsc.decode(xmit)
    receive(repaired.decode())


def receive(received_json: str) -> None:
    d = dict(json.loads(received_json))
    pp(d)
    received_pi = "".join(d.values())
    assert received_pi == str(get_pi())


# from https://en.wikipedia.org/wiki/Chudnovsky_algorithm
def binary_split(a: int, b: int) -> tuple[int, int, int]:
    if b == a + 1:
        Pab = -(6 * a - 5) * (2 * a - 1) * (6 * a - 1)
        Qab = 10939058860032000 * a**3
        Rab = Pab * (545140134 * a + 13591409)
    else:
        m = (a + b) // 2
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)

        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb
    return Pab, Qab, Rab


def chudnovsky(n: int) -> Decimal:
    _P1n, Q1n, R1n = binary_split(1, n)
    return (426880 * Decimal(10005).sqrt() * Q1n) / (13591409 * Q1n + R1n)


def get_pi() -> Decimal:
    decimal.getcontext().prec = 100
    return chudnovsky(8)  # enough terms for all 100 digits to be accurate


if __name__ == "__main__":
    assert get_pi() == Decimal(
        "3.1415926535897932384626433832795028841971693993751"
        "05820974944592307816406286208998628034825342117068"
    )
    assert 101 == len(str(get_pi()))

    demo()
