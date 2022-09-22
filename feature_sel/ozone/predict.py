#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from sklearn.linear_model import LinearRegression

from feature_sel.ozone.ozone import get_df


def _get_train_test(train_through='1976-06-30'):
    df = get_df()
    assert 366 == len(df)

    y_train = df[df.stamp <= train_through].ozone
    y_test = df[df.stamp > train_through].ozone
    del df['ozone']

    x_train = df[df.stamp <= train_through]
    x_test = df[df.stamp > train_through]
    del x_train['stamp']
    del x_test['stamp']

    return (x_train, y_train,
            x_test, y_test)


def testmain():
    x_train, y_train, x_test, y_test = _get_train_test()
    assert 182 == len(x_train)
    assert 184 == len(x_test)
    assert len(y_train) == len(x_train)
    assert len(y_test) == len(x_test)

    lr = LinearRegression()
    lr.fit(x_train, y_train)
    print(lr.score(x_test, y_test))


if __name__ == '__main__':
    main()
