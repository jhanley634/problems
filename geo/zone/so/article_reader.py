#! /usr/bin/env SQLALCHEMY_WARN_20=1 python
# Copyright 2023 John Hanley. MIT licensed.

# from https://softwareengineering.stackexchange.com/questions/450146/designing-a-graph-database-structure

from random import randrange

from sqlalchemy import text
from sqlalchemy.orm import Session
from tqdm import tqdm
import pandas as pd

from geo.zone.so.article_db import NUM_FACTS, NUM_USERS, Fact, create_engine

engine = create_engine()


def num_facts_for(user_id: int, slow: bool = False):
    if slow:
        select = f"SELECT fact_id  FROM fact  WHERE user_id = {user_id}"
        df = pd.read_sql(select, engine)
        assert NUM_FACTS / 2 == len(df)

    select = "count(*)"  # or "sum(fact_id)"
    with Session(engine) as session:
        yield from session.query(text(select)).filter(Fact.user_id == user_id)


def main():
    for _ in tqdm(range(1000), smoothing=1e-4):
        user_id = randrange(NUM_USERS)
        (n,) = next(num_facts_for(user_id))
        # assert NUM_FACTS / 2 == n, n
        assert n > 0


if __name__ == "__main__":
    main()
