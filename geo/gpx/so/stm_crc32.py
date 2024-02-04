#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.


# from https://codereview.stackexchange.com/questions/176032/python-code-to-calculate-stm-crc32


custom_crc_table = {}
poly = 0x04C11DB7


def generate_crc32_table(_poly):
    global custom_crc_table

    for i in range(256):
        c = i << 24

        for j in range(8):
            c = (c << 1) ^ _poly if (c & 0x80000000) else c << 1

        custom_crc_table[i] = c & 0xFFFFFFFF


def crc32_stm(bytes_arr):
    length = len(bytes_arr)
    crc = 0xFFFFFFFF

    k = 0
    while length >= 4:
        v = (
            ((bytes_arr[k] << 24) & 0xFF000000)
            | ((bytes_arr[k + 1] << 16) & 0xFF0000)
            | ((bytes_arr[k + 2] << 8) & 0xFF00)
            | (bytes_arr[k + 3] & 0xFF)
        )

        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[0xFF & ((crc >> 24) ^ v)]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 8))
        ]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 16))
        ]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 24))
        ]

        k += 4
        length -= 4

    if length > 0:
        v = 0

        for i in range(length):
            v |= bytes_arr[k + i] << 24 - i * 8

        if length == 1:
            v &= 0xFF000000

        elif length == 2:
            v &= 0xFFFF0000

        elif length == 3:
            v &= 0xFFFFFF00

        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[0xFF & ((crc >> 24) ^ (v))]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 8))
        ]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 16))
        ]
        crc = ((crc << 8) & 0xFFFFFFFF) ^ custom_crc_table[
            0xFF & ((crc >> 24) ^ (v >> 24))
        ]

    return crc
