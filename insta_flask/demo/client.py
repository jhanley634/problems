#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
import requests


def main():
    assert "Hello!" == requests.get("http://localhost:5000/hello").text.rstrip()


# curl --header "Content-Type:application/json" --data "[1,2,3]" http://localhost:5000/mean

if __name__ == "__main__":
    main()
