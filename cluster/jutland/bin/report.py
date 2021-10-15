#! /usr/bin/env python
from jutland.dataset import Dataset


def report():
    df = Dataset.get_df()
    print(df)


if __name__ == '__main__':
    report()
