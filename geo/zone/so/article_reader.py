#! /usr/bin/env SQLALCHEMY_WARN_20=1 python
# Copyright 2023 John Hanley. MIT licensed.
# from https://softwareengineering.stackexchange.com/questions/450146/designing-a-graph-database-structure
from collections.abc import Generator, Iterable
from random import randrange

from sqlalchemy import text
from sqlalchemy.orm import Session
from tqdm import tqdm

from geo.zone.so.article_db import NUM_FACTS, NUM_USERS, Fact, WorldFact, create_engine


def fact_details_for(user_id: int) -> Generator[Iterable[str]]:
    with Session(engine) as session:
        yield from session.query(WorldFact.details).join(Fact).filter(
            Fact.user_id == user_id
        )


def num_facts_for(user_id: int) -> Generator[Iterable[int]]:
    select = "count(*)"  # or "sum(fact_id)"
    with Session(engine) as session:
        yield from session.query(text(select)).filter(Fact.user_id == user_id)


def main(num_queries: int = 1_000) -> None:
    for _ in tqdm(range(num_queries), smoothing=1e-4):
        user_id = randrange(NUM_USERS)
        (n,) = next(num_facts_for(user_id))
        assert NUM_FACTS / 2 == n


if __name__ == "__main__":
    engine = create_engine()
    main()
