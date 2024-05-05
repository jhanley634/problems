#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class ApnAddress(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "apn_address"

    apn = mapped_column(Text, primary_key=True)
    situs_addr = mapped_column(Text, index=True, nullable=False)
