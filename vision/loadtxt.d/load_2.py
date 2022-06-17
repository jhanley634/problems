#! /usr/bin/env python
import ctypes

# http://saidvandeklundert.net/learn/2021-11-06-calling-rust-from-python

rust = ctypes.CDLL('target/release/librust_lib.so')


if __name__ == '__main__':
    SOME_BYTES = 'Python says hi inside Rust!'.encode('utf-8')
    rust.print_string(SOME_BYTES)
