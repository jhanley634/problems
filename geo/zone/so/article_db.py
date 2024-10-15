#! /usr/bin/env SQLALCHEMY_WARN_20=1 python
# Copyright 2023 John Hanley. MIT licensed.
# from https://softwareengineering.stackexchange.com/questions/450146/designing-a-graph-database-structure
from array import array
from collections.abc import Callable
from hashlib import sha3_224
from pathlib import Path
from random import shuffle
from time import time
from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.schema import PrimaryKeyConstraint
from tqdm import tqdm
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


def insert_with_orm() -> None:
    with Session(engine) as session:
        for i in range(NUM_FACTS):
            name = sha3_224(f"Earth {i}".encode()).hexdigest()
            session.add(WorldFact(name=name, details=f"lorem ipsum {i}"))
        session.commit()


class Base(DeclarativeBase):
    # sqlalchemy.exc.InvalidRequestError:
    # Cannot use 'DeclarativeBase' directly as a declarative base class.
    # Create a Base by creating a subclass of it.
    pass


class WorldFact(Base):
    __tablename__ = "world_fact"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # , unique=True)
    details = Column(String)


class Fact(Base):
    __tablename__ = "fact"
    user_id = Column(Integer)
    fact_id = Column(Integer, ForeignKey("world_fact.id"))
    PrimaryKeyConstraint(user_id, fact_id)


def create_engine() -> Engine:
    DB_FILE = Path("/tmp/article.db")
    DB_URL = f"sqlite:///{DB_FILE}"
    return sa.create_engine(DB_URL)


# It takes 1 second to INSERT 188_000 rows into world_facts.
NUM_FACTS = 40_000
NUM_USERS = 10_000


def get_fact_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [
                sha3_224(f"Earth {i}".encode()).hexdigest() for i in range(NUM_FACTS)
            ],
            "details": [f"Loxodonta africana {i}" for i in range(NUM_FACTS)],
        }
    )


@timed
def insert_world_facts(fact_df: pd.DataFrame) -> None:
    fact_df.to_sql("world_fact", engine, index=False, if_exists="append")


def insert_user_facts(user_df: pd.DataFrame) -> None:
    user_df.to_sql("fact", engine, index=False, if_exists="append")


def main() -> None:
    fact_df = get_fact_df()
    insert_world_facts(fact_df)

    with Session(engine) as session:
        fact_ids = array("I", [row.id for row in session.query(WorldFact.id)])

    for userid in tqdm(range(NUM_USERS), smoothing=1e-4):
        shuffle(fact_ids)
        user_df = pd.DataFrame({"fact_id": fact_ids[: NUM_FACTS // 2]})
        user_df["user_id"] = userid
        insert_user_facts(user_df)


if __name__ == "__main__":
    engine = create_engine()
    Base.metadata.create_all(engine)
    main()
