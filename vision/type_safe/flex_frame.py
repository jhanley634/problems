#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from abc import ABC
from typing import Never

import pandas as pd
import pyspark.context as pc
import pyspark.pandas as sp


class Delegator(ABC):
    def get_delegated_obj(self) -> Never:
        msg = "Implementor must delegate to an object"
        raise ValueError(msg)

    def __getattr__(self, called_method):
        def _wrapper(*args, **kwargs):
            return getattr(self.get_delegated_obj(), called_method)(*args, **kwargs)

        return _wrapper

    def __getitem__(self, item):
        return self.get_delegated_obj()[item]


class FlexFrame(Delegator):
    def __init__(self, arg, **kwargs) -> None:
        rec = arg.to_records(index=False)
        self.pd = self.sp = None
        if isinstance(arg, pd.DataFrame):
            self.pd = pd.DataFrame(rec, **kwargs)
        elif isinstance(arg, sp.DataFrame):
            self.sp = sp.DataFrame(rec, **kwargs)
        else:
            msg = f"Unexpected type: {type(arg)}"
            raise TypeError(msg)

    def get_delegated_obj(self):
        # We're either delegating to pandas or to spark.
        return self.pd if self.pd is not None else self.sp


def format_table(df: FlexFrame) -> FlexFrame:
    assert isinstance(df, FlexFrame)

    df = df.copy()[["id", "code"]]
    return df.rename(columns={"id": "new_id", "code": "new_code"})


def get_pandas_example() -> FlexFrame:
    return FlexFrame(pd.DataFrame({"id": [1, 2, 3], "code": ["a", "b", "c"]}))


def get_pyspark_example() -> FlexFrame:
    return FlexFrame(sp.DataFrame({"id": [4, 5, 6], "code": ["d", "e", "f"]}))


if __name__ == "__main__":
    pc.SparkContext().setLogLevel("ERROR")

    print(format_table(get_pandas_example()))
    print(format_table(get_pyspark_example()))
