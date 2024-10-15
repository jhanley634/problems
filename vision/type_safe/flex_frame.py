#! /usr/bin/env python

# Copyright 2023 John Hanley. MIT licensed.
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import pandas as pd
import pyspark.context as pc
import pyspark.pandas as sp

if TYPE_CHECKING:
    from pyspark.sql.connect.proto import Unknown


class Delegator(ABC):

    @abstractmethod
    def get_delegated_obj(self) -> Any:
        msg = "Implementor must delegate to an object"
        raise ValueError(msg)

    def __getattr__(self, called_method: Any) -> Any:
        def _wrapper(*args: Any, **kwargs: Any) -> Any:
            return getattr(self.get_delegated_obj(), called_method)(*args, **kwargs)

        return _wrapper

    def __getitem__(self, item: Any) -> Any:
        return self.get_delegated_obj()[item]


class FlexFrame(Delegator):
    def __init__(self, arg: Any, **kwargs: Any) -> None:
        rec = arg.to_records(index=False)
        self.pd = None
        self.sp: sp.DataFrame[Unknown] | None = None
        if isinstance(arg, pd.DataFrame):
            self.pd = pd.DataFrame(rec, **kwargs)
        elif isinstance(arg, sp.DataFrame):
            self.sp = sp.DataFrame(rec, **kwargs)  # type: ignore [no-untyped-call]
            assert isinstance(self.sp, sp.DataFrame)
        else:
            msg = f"Unexpected type: {type(arg)}"
            raise TypeError(msg)

    def get_delegated_obj(self) -> Any:
        # We're either delegating to pandas or to spark.
        return self.pd if self.pd is not None else self.sp


def format_table(df: FlexFrame) -> Any:
    assert isinstance(df, FlexFrame)

    df = df.copy()[["id", "code"]]
    return df.rename(columns={"id": "new_id", "code": "new_code"})


def get_pandas_example() -> FlexFrame:
    return FlexFrame(pd.DataFrame({"id": [1, 2, 3], "code": ["a", "b", "c"]}))


def get_pyspark_example() -> FlexFrame:
    df: Any = sp.DataFrame({"id": [4, 5, 6], "code": ["d", "e", "f"]})  # type: ignore [no-untyped-call]
    assert isinstance(df, sp.DataFrame)
    return FlexFrame(df)


if __name__ == "__main__":
    pc.SparkContext().setLogLevel("ERROR")

    print(format_table(get_pandas_example()))
    print(format_table(get_pyspark_example()))
