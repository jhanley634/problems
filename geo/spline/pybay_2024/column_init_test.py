# Copyright 2024 John Hanley. MIT licensed.

from collections.abc import Generator
from contextlib import contextmanager
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import func as fn
import polars as pl

from geo.spline.pybay_2024.podcaster_model import Base, Podcaster

engine = create_engine(url="sqlite:////tmp/podcaster.db")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with sessionmaker(bind=engine)() as sess:
        try:
            yield sess
        finally:
            sess.commit()


def populate_rows() -> None:
    Base.metadata.create_all(engine)
    with get_session() as sess:
        sess.query(Podcaster).delete()

        for name, age in [
            ("Steve", 78),
            ("Martin", 74),
            ("Selena", 32),
        ]:
            sess.add(Podcaster(name=name, age=age))


class ColumnInitTest(unittest.TestCase):
    def test_aggregate_mean_median(self) -> None:
        populate_rows()
        with get_session() as sess:
            q = sess.query(fn.avg(Podcaster.age))
            one_third = 1 / 3
            self.assertEqual(61 + one_third, q.scalar())

            podcaster = pl.read_database("SELECT * FROM podcaster", engine)
            self.assertEqual(61 + one_third, podcaster["age"].mean())
            self.assertEqual(74, podcaster["age"].median())
