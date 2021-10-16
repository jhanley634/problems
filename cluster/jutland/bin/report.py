#! /usr/bin/env python
from autoPyTorch import AutoNetClassification
from jutland.dataset import Dataset
from numpy import nan
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sklearn.datasets
import sklearn.metrics
import sklearn.model_selection


def _get_northern_subset() -> pd.DataFrame:
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

    X = ground_truth.copy().drop(columns=['osm_id'])
    y = ground_truth.copy()[['osm_id']]

    X_train, X_test, y_train, y_test = (
        sklearn.model_selection.train_test_split(X, y, random_state=1))

    autonet = AutoNetClassification(
        'tiny_cs', budget_type='epochs', min_budget=1, max_budget=9, num_iterations=1,
        log_level='debug', use_pynisher=False)

    res = autonet.fit(X_train=X_train, Y_train=y_train,
                      cross_validator='k_fold', cross_validator_args={'n_splits': 3})

    print(res)
    print('Score:', autonet.score(X_test=X_train, Y_test=y_train))


if __name__ == '__main__':
    find_clusters()
