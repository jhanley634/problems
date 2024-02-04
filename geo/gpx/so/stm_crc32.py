#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


# from https://codereview.stackexchange.com/questions/176032/python-code-to-calculate-stm-crc32

from hashlib import sha3_512
from time import time
import unittest


def generate_crc32_table(poly):
    custom_crc_table = {}
    for i in range(256):
        c = i << 24

        for j in range(8):
            c = (c << 1) ^ poly if (c & 0x8000_0000) else c << 1

        custom_crc_table[i] = c & 0xFFFF_FFFF

    return custom_crc_table


poly = 0x04C1_1DB7
custom_crc_table = generate_crc32_table(poly)


def crc32_stm(bytes_arr):
    length = len(bytes_arr)
    crc = 0xFFFF_FFFF

    k = 0
    while length >= 4:
        v = (
            ((bytes_arr[k] << 24) & 0xFF00_0000)
            | ((bytes_arr[k + 1] << 16) & 0xFF_0000)
            | ((bytes_arr[k + 2] << 8) & 0xFF00)
            | (bytes_arr[k + 3] & 0xFF)
        )

        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[0xFF & ((crc >> 24) ^ v)]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 8))
        ]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 16))
        ]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 24))
        ]

        k += 4
        length -= 4

    if length > 0:
        v = 0

        for i in range(length):
            v |= bytes_arr[k + i] << 24 - i * 8

        if length == 1:
            v &= 0xFF00_0000

        elif length == 2:
            v &= 0xFFFF_0000

        elif length == 3:
            v &= 0xFFFF_FF00

        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[0xFF & ((crc >> 24) ^ (v))]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 8))
        ]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 16))
        ]
        crc = ((crc << 8) & 0xFFFF_FFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 24))
        ]

    return crc


class StmCrc32Test(unittest.TestCase):
    def setUp(self):
        h = sha3_512(b"hello")
        assert h.hexdigest().startswith("75d527c3")
        assert 64 == len(h.digest())
        self.buf = b"".join([h.digest()] * 80)
        assert 5120 == len(self.buf)

    def test_original(self):
        t0 = time()
        self.assertEqual(0xAB30_8DE0, crc32_stm(b"123456788"))
        self.assertEqual(0xAFF1_9057, crc32_stm(b"123456789"))
        for _ in range(10):
            self.assertEqual(0x957C_B03E, crc32_stm(self.buf))
        print(f"\nelapsed: {time() - t0:.6f}")
