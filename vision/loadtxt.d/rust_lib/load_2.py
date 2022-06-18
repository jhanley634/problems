#! /usr/bin/env python
import rust

# http://saidvandeklundert.net/learn/2021-11-18-calling-rust-from-python-using-pyo3


if __name__ == '__main__':
    result = rust.multiply(2, 3)
    print(result)
