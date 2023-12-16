#! /usr/bin/env SQLALCHEMY_WARN_20=1 python
# Copyright 2023 John Hanley. MIT licensed.

# from https://softwareengineering.stackexchange.com/questions/450146/designing-a-graph-database-structure

from hashlib import sha3_224
from pathlib import Path
from time import time
from typing import Any, Callable

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
import pandas as pd
import sqlalchemy as sa


def timed(
    func: Callable[[Any], Any], reporting_threshold_sec: float = 0.1
) -> Callable[[Any], Any]:
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        t0 = time()
        ret = func(*args, **kwargs)
        elapsed = time() - t0
        if elapsed > reporting_threshold_sec and func.__name__ != "wrapped":
            print(f"  Elapsed time of {elapsed:.3f} seconds for {func.__name__}")
        return ret

    return wrapped


def insert_with_orm():
    with Session(engine) as session:
        for i in range(NUM_FACTS):
            name = sha3_224(f"Earth {i}".encode()).hexdigest()
            session.add(WorldFact(name=name, details=f"lorem ipsum {i}"))
        session.commit()


Base = declarative_base()


class WorldFact(Base):
    __tablename__ = "world_fact"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # , unique=True)
    details = Column(String)


def create_engine():
    DB_FILE = Path("/tmp/article.db")
    DB_URL = f"sqlite:///{DB_FILE}"
    engine = sa.create_engine(DB_URL)
    return engine


engine = create_engine()

NUM_FACTS = 188_000  # It takes 1 second to INSERT this many rows.


def get_df():
    return pd.DataFrame(
        {
            "name": [
                sha3_224(f"Earth {i}".encode()).hexdigest() for i in range(NUM_FACTS)
            ],
            "details": [f"lorem ipsum {i}" for i in range(NUM_FACTS)],
        }
    )


@timed
def main(df: pd.DataFrame) -> None:
    df.to_sql("world_fact", engine, index=False, if_exists="append")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main(get_df())
