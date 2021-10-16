#! /usr/bin/env python
from jutland.dataset import Dataset
from numpy import nan
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def _get_northern_subset():
    cache = Dataset.TMP / 'northern_subset.parquet'
    if not cache.exists():
        df = Dataset.get_df().reset_index(drop=True)
        pq.write_table(pa.Table.from_pandas(df), cache)
    return pq.read_table(cache).to_pandas()


def _train_and_test(ground_truth: pd.DataFrame):
    train = ground_truth.copy()
    train = train[train.index % 2 == 0]
    assert 12716 == len(train)

    test = ground_truth.copy()
    test = test[test.index % 2 == 1]
    test['osm_id'] = nan
    test.osm_id = nan

    return train, test


def find_clusters():
    ground_truth = _get_northern_subset()

    print(_train_and_test(ground_truth))


if __name__ == '__main__':
    find_clusters()
